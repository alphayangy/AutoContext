# CLAUDE.md

本文件为 Claude Code（claude.ai/code）处理本仓库代码时提供指导。

## 概述

**mdflow**（`md`）是一个将 AI agent 定义为 markdown 文件并执行的 CLI 工具。它解析 YAML frontmatter 中的配置，并将键直接作为 CLI 标志传递给指定命令（claude、codex、gemini、copilot 或其他 CLI 工具）。

## CLI 子命令

```bash
md <file.md> [flags]     # 运行一个 flow
md init [-e <eng>] [-y]  # 初始化 flow 清单（由 agent CLI 引导；-y 直接生成脚手架）
md create [name]         # 创建新的 flow 文件
md explain <flow.md>     # 显示解析后的配置，不执行（免费）
md eval <flow.md>        # 运行 flow 的评估套件（消耗 engine 调用次数）
md complain <flow.md> "msg"  # 记录演进证据（免费）
md evolve <flow.md>      # 基于证据的提示词演进（--check 免费）
md install <url|gh:...>  # 将 flow 安装到注册表（参见 src/registry.ts）
md remove <name>         # 移除已安装的注册表 flow
md list                  # 列出已安装的注册表 flow
md setup                 # 配置 shell（PATH、别名）
md logs                  # 显示 flow 日志目录
md help                  # 显示帮助
```

## 开发命令

```bash
# 运行测试（首个失败即停止）
bun test --bail=1

# 运行单个测试文件
bun test src/cli.test.ts

# 按名称运行特定测试
bun test --test-name-pattern "parses command"

# 直接执行 CLI
bun run src/index.ts task.claude.md

# 或使用别名
bun run md task.claude.md
```

## 网站（`site/`）

mdflow.dev 落地页位于 `site/`（Vite + React，通过 Vercel 部署，Root Directory 设为 `site`）。规则：

- `site/src/facts.json` 由 `scripts/generate-facts.ts` 从 adapter 注册表、`DEFAULT_ENGINE`、`cli-runner.ts` 子命令以及 package.json **生成** —— 切勿手动编辑。`bun run facts` 重新生成；`bun run facts:check` 在 CI 中运行，若发生漂移则失败。向 `cli-runner.ts` 添加子命令时，需在生成器中补充对应的 `COMMAND_DOCS` 条目。
- 仅涉及网站的提交使用 `chore(site):` / `docs(site):` 范围，避免 semantic-release 因视觉改动而发布 CLI 版本。
- 网站中的事实性文案应从 facts.json 渲染；艺术性文案（标题、着色器、彩蛋）可手写。详见 `docs/SITE-SYNC.md`。

## 架构

### 核心流程（`src/index.ts`）
```
.md file → parseFrontmatter() → resolveEngine(ladder, 见下文)
        → loadFullConfig() → applyDefaults()
        → applyInteractiveMode() → expandImports()
        → substituteTemplateVars() → buildArgs() → runCommand()
```

### 关键模块

- **`command.ts`** - 引擎解析与执行
  - `parseCommandFromFilename()`：从 `task.claude.md` 推断引擎为 `claude`
  - `hasInteractiveMarker()`：检测文件名中的 `.i.`（例如 `task.i.claude.md`）
  - `resolveEngine()`：v3 解析阶梯（见下文“引擎解析”）；引擎缺失时绝不抛出异常 —— 使用 `DEFAULT_ENGINE`（pi）
  - `buildArgs()`：将 frontmatter 转换为 CLI 标志
  - `extractPositionalMappings()`：提取 `$1`、`$2` 等映射
  - `runCommand()`：启动引擎；调用 adapter 可选的 `prepareEnv()` 钩子（pi 用它连接授权目录）
  - 注意：command.ts 导出了自己的 `getAdapter`（可移植 key 层）；注册表查找以 `getEngineAdapter` 导入

- **`evals.ts`** - `md eval <flow.md>`：行为评估套件
  （`<flow>.eval.ts`，默认导出 `EvalCase[]`）在隔离的临时目录中运行；信任账本位于 `~/.mdflow/eval-results.json`；运行前打印成本；评估运行会重定向 `MDFLOW_RUNS_FILE`，避免污染遥测数据

- **`init.ts`** - `md init`：项目引导。默认路径会交互式启动已安装的引擎 CLI，并预加载 `assets/init/guide.md`（原样传递，绝不经过 import/template 管道）；飞行后检查验证会话写入的内容。`--yes`/无 TTY 时按确定性规则生成 `assets/init/catalog/` 脚手架。`bin/mdflow.mjs` 是面向 npx 的纯 Node 启动器，负责桥接到 bun。

- **`evolve.ts`** - `md evolve` / `md complain`：将投诉与粗糙运行转化为维护者起草的提示词 BODY 修订，仅当完整评估套件通过且得分不低于祖先基线时才应用；失败则逐字节回退到 `<flow>.pending.md`。触发规则是纯函数 `decideEvolve`，无评估套件或新证据时直接拒绝；评估运行永远不能触发它（语料隔离）。`evolve: auto` frontmatter 让 flow 加入运行后自动演进（快速重跑将隐式视为投诉），并由信任账本 `lastCleanAt` 严格把关。投诉仅用于演进；粗糙运行也会被干净的评估消费。通过 `<flow>.md.evolve-backup` 实现崩溃安全。在 `evolve.test.ts` 中验证。

- **`adapters/pi-auth.ts`** - pi 引擎的 Codex 订阅授权桥（`~/.mdflow/pi-agent`，通过 `PI_CODING_AGENT_DIR` 指向）；绝不写入用户真实凭据文件

- **`compat.ts`** - 自动 frontmatter 版本/兼容性戳记：`md create`/`md init` 写入 `_mdflow_version`（创建时版本），成功本地运行后戳记/升级 `_compat`（验证通过的最新版本）；采用外科式行级 frontmatter 编辑，遵循 semver，主版本不匹配时仅打印暗淡的 stderr 提示，从不阻塞执行

- **`config.ts`** - 全局配置
  - 从 `~/.mdflow/config.yaml` 加载默认值
  - 内置默认值：所有命令默认处于 print 模式
  - `getCommandDefaults()`：获取某命令的默认值
  - `applyDefaults()`：将默认值与 frontmatter 合并
  - `applyInteractiveMode()`：按命令将 print 默认值转换为 interactive 模式

- **`types.ts`** - 核心 TypeScript 接口
  - `AgentFrontmatter`：简单接口，包含系统键 + 透传键
  - 系统键：`_varname`（模板变量）、`env`、`$1`/`$2`/等等

- **`schema.ts`** - 最小化 Zod 校验（仅系统键，其余透传）

- **`imports.ts`** - 文件导入，支持高级特性：
  - 基础：`@./path.md` - 内联文件内容
  - 通配：`@./src/**/*.ts` - 多个文件（遵守 .gitignore）
  - 行范围：`@./file.ts:10-50` - 提取指定行
  - 符号：`@./file.ts#InterfaceName` - 提取 TypeScript 符号
  - 命令：`` !`cmd` `` - 内联命令输出
  - URL：`@https://example.com/file.md` - 获取远程内容

- **`env.ts`** - 从 .env 文件加载环境变量

- **`template.ts`** - 基于 LiquidJS 的模板引擎，用于变量替换

- **`logger.ts`** - 使用 pino 的结构化日志（写入 `~/.mdflow/logs/<agent>/`）

- **`history.ts`** - Frecency 跟踪与变量持久化
  - `recordUsage()`：跟踪 agent 文件使用，用于 frecency 排序
  - `getFrecencyScore()`：计算路径的 frecency 得分
  - `getVariableHistory()`：获取 agent 的历史变量值
  - `saveVariableValues()`：保存提示输入的变量值供未来运行使用
  - `getPreviousVariableValue()`：获取某个变量的上一次值

### 引擎解析（v3）

引擎按以下阶梯解析，从最显式到最隐式：
1. `--engine` CLI 标志（废弃别名：`--_command`/`-_c`、`--tool`）
2. `MDFLOW_ENGINE` 环境变量
3. 文件名模式：`task.claude.md` → `claude`
4. Frontmatter `engine:`（废弃别名 `tool:`/`_tool:` 会发出警告）
5. 配置 `engine:`（项目配置优先于 `~/.mdflow/config.yaml`）
6. 内置默认值：`pi`

隐式解析（环境变量/配置/默认值）会在 stderr 打印一行暗淡说明。没有 frontmatter 且仅依赖隐式引擎的文件被视为文档并打印，不会执行。

### Frontmatter 键

**系统键**（由 md 消费，不会传给命令）：
- `_varname`：模板变量（例如 `_name: "default"` → 在正文中使用 `{{ _name }}` → 生成 `--_name` CLI 标志）
- `_stdin`：自动注入的模板变量，包含管道输入
- `_1`、`_2` 等：自动注入的位置 CLI 参数（例如 `md task.md "foo"` → `{{ _1 }}` = "foo"）
- `_args`：自动注入的所有位置参数编号列表
- `_inputs`：从 CLI 消费的有名位置参数（例如 `_inputs: [_message]`）
- `_env`：在执行前设置 process.env
- `$1`、`$2` 等：将位置参数映射为标志
- `_interactive`：启用 interactive 模式（覆盖 print 模式默认值）
- `_subcommand`：向 CLI 参数前置子命令（例如 `_subcommand: exec`）
- `_cwd`：覆盖内联命令（`` !`cmd` ``）的工作目录
- `_mdflow_version` / `_compat`：自动兼容性戳记（见下文）—— 切勿手动设置

**兼容性戳记（`src/compat.ts`）：** 每个 flow 都跟踪其适用的 mdflow 版本，无需用户参与。`md create`/`md init` 会盖上 `_mdflow_version`（创建时的版本）；任何成功本地运行后，mdflow 会通过外科式 frontmatter 编辑戳记/升级 `_compat`（验证通过的最新版本），并逐字节保留文件其余内容。仅当主版本/次版本发生偏移时才升级 —— 补丁和预发布版本不会重写 flow（避免每次发布都产生 git 变更）。
远程 flow 和评估运行（`MDFLOW_EVAL_RUN=1`）永远不会被戳记。记录版本与运行中 mdflow 的主版本不匹配时，仅打印暗淡的 stderr 提示，不会阻塞。仅包含这些键的 frontmatter 在“文档 vs flow”规则中仍视为“无 frontmatter”。

**注意：** `--_varname` 类 CLI 标志无需 frontmatter 声明即可工作。如果正文中使用了 `_` 前缀变量但未提供，系统会提示输入。

**变量历史：** 提示输入缺失变量时，会以上次值作为默认值显示（存储在 `~/.mdflow/variable-history.json`）。按 Enter 接受上次值，或输入新值覆盖。使用 `--_no-history` 可跳过变量历史的加载/保存。

**其余所有键**都会直接作为 CLI 标志传递：

```yaml
---
model: opus                  # → --model opus
dangerously-skip-permissions: true  # → --dangerously-skip-permissions
add-dir:                     # → --add-dir ./src --add-dir ./tests
  - ./src
  - ./tests
_env:                        # 设置 process.env（下划线前缀 = 系统键）
  API_KEY: secret
---
```

### 位置映射（$N）

将正文或位置参数映射到特定标志：

```yaml
---
$1: prompt    # 正文作为 --prompt <body> 传递，而非位置参数
---
```

### Print 与 Interactive 模式

所有命令默认处于 **print 模式**（非交互）。使用 `.i.` 文件名标记或 `_interactive: true` 进入 interactive 模式。

```bash
task.claude.md      # Print 模式：claude --print "..."
task.i.claude.md    # Interactive：claude "..."
task.copilot.md     # Print 模式：copilot --silent --prompt "..."
task.i.copilot.md   # Interactive：copilot --silent --interactive "..."
task.codex.md       # Print 模式：codex exec "..."
task.i.codex.md     # Interactive：codex "..."
task.gemini.md      # Print 模式：gemini "..."（一次性）
task.i.gemini.md    # Interactive：gemini --prompt-interactive "..."
task.droid.md       # Print 模式：droid exec "..."
task.i.droid.md     # Interactive：droid "..."
task.opencode.md    # Print 模式：opencode run "..."
task.i.opencode.md  # Interactive：opencode "..."
```

### 各 CLI 支持的模型（2025 年 12 月）

**重要：** 请使用以下精确的模型名称。不要猜测或使用已废弃的模型名称。

> **时效性说明（2026-07）：** 本表为 2025 年 12 月的快照，此后已有新模型发布（例如 mdflow.dev 示例使用 `gpt-5.5-codex-max` 和 `gemini-3.1-pro`）。当模型名称很重要时，请对照引擎 CLI 自身的 `--help`/文档进行验证，而非依赖本表。

#### Claude Code（`claude`）
| 类型 | 取值 |
|------|--------|
| **别名** | `sonnet`、`opus`、`haiku`、`opusplan` |
| **完整名称** | `claude-sonnet-4-5-20250929`、`claude-opus-4-5-20251101`、`claude-haiku-4-5-20251001`、`claude-opus-4-1-20250805` |

别名控制的环境变量：
- `ANTHROPIC_DEFAULT_SONNET_MODEL` - 覆盖 sonnet 别名
- `ANTHROPIC_DEFAULT_OPUS_MODEL` - 覆盖 opus 别名
- `ANTHROPIC_DEFAULT_HAIKU_MODEL` - 覆盖 haiku 别名

#### Codex CLI（`codex`）
| 类型 | 取值 |
|------|--------|
| **默认** | `codex-mini-latest`（针对 CLI 优化的 o4-mini） |
| **推理模型** | `o3`、`o4-mini` |
| **GPT 模型** | `gpt-4.1` |

Codex 兼容任何 OpenAI 模型。示例：`-m o3` 或 `-c model="o3"`

#### Gemini CLI（`gemini`）
| 类型 | 取值 |
|------|--------|
| **默认（免费）** | `gemini-2.5-pro` |
| **预览** | `gemini-3-pro`（需订阅或付费 API key） |

启用 Gemini 3 Pro：运行 `/settings`，将 "Preview features" 设为 true。

#### Copilot CLI（`copilot`）
来自 `copilot --help` 的显式 `--model` 选项：
| 类别 | 模型 |
|----------|--------|
| **Claude** | `claude-sonnet-4.5`、`claude-haiku-4.5`、`claude-opus-4.5`、`claude-sonnet-4` |
| **GPT** | `gpt-5.1-codex-max`、`gpt-5.1-codex`、`gpt-5.2`、`gpt-5.1`、`gpt-5`、`gpt-5.1-codex-mini`、`gpt-5-mini`、`gpt-4.1` |
| **Gemini** | `gemini-3-pro-preview` |

### 全局配置（`~/.mdflow/config.yaml`）

按命令设置默认 frontmatter：

```yaml
commands:
  claude:
    model: sonnet # claude 的默认模型
```

### 模板系统（LiquidJS）

使用 [LiquidJS](https://liquidjs.com/) 实现完整模板支持：

- 变量：`{{ _varname }}`（模板变量使用 `_` 前缀）
- Stdin：`{{ _stdin }}`（自动从管道输入注入）
- 条件：`{% if _force %}--force{% endif %}`
- 过滤器：`{{ _name | upcase }}`、`{{ _value | default: "fallback" }}`
- CLI 覆盖：`--_varname value` 会匹配 frontmatter 中的 `_varname`

## 测试模式

测试使用 Bun 的测试运行器，采用 `describe`/`it` 块：

```typescript
import { describe, it, expect } from "bun:test";

describe("parseCliArgs", () => {
  it("parses command flag", () => {
    const result = parseCliArgs(["node", "script", "file.md"]);
    expect(result.filePath).toBe("file.md");
  });
});
```
