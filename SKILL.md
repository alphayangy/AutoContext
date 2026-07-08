---
name: auto-context
description: Use before starting, onboarding, or recalibrating any project. Scans the workspace or interviews the user, identifies the project scenario, composes guideline atoms, and generates a reviewable CLAUDE.md, AGENTS.md, or .claude/rules/ context pack.
---

# Auto Context

Project onboarding skill + Context Compiler。开工前或项目进行中，识别项目场景，组合准则原子，生成最小但有效的上下文文件。

## 何时使用

- 初始化一个新项目
- 给已有项目补上下文
- 觉得现有 `CLAUDE.md` 不准/太旧，想重新校准

## 核心流程

```text
检测 -> 定 Profile ->（必要时）问问题 -> 召回 atom -> 组合 -> 渲染 proposal -> 自审 Review -> 写入
```

执行时严格遵守 [`references/meta-rules.md`](references/meta-rules.md)（AutoContext 自己守的元规则），尤其 M7「每行问删了会犯错吗」和 M8「CLAUDE.md < 200 行」。

---

## Step 1: 检测项目（Detect）

扫描高信号文件，输出结构化检测结果。**先用 tree 快速拿到目录骨架，再挑关键文件读前 30 行，不要逐个目录 ls、不要全文读取。**

### 1.1 快速扫描步骤

1. **一次拿到目录结构**
   ```bash
   tree -L 2 -I 'node_modules|.git|.venv|venv|__pycache__|dist|build|target|.next|.nuxt|coverage|*.pyc'
   ```
   如果 `tree` 不可用，用等价的 `find` 命令，但只取两层。

2. **挑高信号文件读前 30 行**
   按优先级读取以下文件，不确定时跳过，不读大文件：
   - `README*`, `README.md`, `README.zh.md`
   - `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `requirements.txt`
   - `Makefile`, `justfile`, `docker-compose.yml`, `Dockerfile`
   - 入口脚本：`run.sh`, `main.py`, `batch_infer.py`, `src/main.*` 等
   - 已有 agent 配置文件：`CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.cursor/rules/*.mdc`, `.windsurfrules` 等

3. **统计信号（只看文件名和路径，不看内容）**
   - 可执行代码：`*.py`, `*.go`, `*.rs`, `*.ts`, `*.js`, `*.sh`, `Makefile`, `Snakefile`
   - 数据文件：`*.sql`, `*.ipynb`, `*.parquet`, `*.csv`, `*.xlsx`, `dbt_project.yml`
   - 配置文件：`*.toml`, `*.yaml`, `*.yml`, `*.json`
   - 文档/资料：`docs/`, `references/`, `papers/`, `*.md`

### 1.2 输出字段

```json
{
  "workspace_state": "empty | existing | partial",
  "detected_stack": ["typescript", "react", "vite"],
  "important_dirs": ["src", "tests", "docs"],
  "commands": {
    "install": "npm install",
    "run": "npm run dev",
    "test": "npm test",
    "build": "npm run build"
  },
  "existing_context": ["CLAUDE.md", "AGENTS.md"],
  "detected_agents": ["claude-code", "cursor"],
  "profile_scores": [
    {"profile": "frontend-product", "score": 0.84, "evidence": ["package.json", "src/App.tsx", "vite.config.ts"]}
  ],
  "confidence": 0.84,
  "questions": []
}
```

- `workspace_state`: 空目录/已有项目/部分项目（只有少量文件）。
- `detected_stack`: 从依赖和文件推断的技术栈，不确定时不填。
- `commands`: 从 `package.json` scripts、`Makefile`、`README` 提取，不确定时标 `TBD`。
- `existing_context`: 已存在的 agent 上下文文件。
- `detected_agents`: 根据已有配置文件推断的用户 Agent 列表，例如 `["claude-code", "cursor"]`。
- `confidence`: 主 Profile 的置信度。

### 1.3 检测用户使用的 Agent 产品

除了扫描项目里的上下文文件，还要把文件映射到具体 Agent，输出 `detected_agents`：

| 检测到的文件 | 推断的 Agent |
|-------------|-------------|
| `CLAUDE.md` / `.claude/CLAUDE.md` | Claude Code |
| `.cursorrules` / `.cursor/rules/*.mdc` | Cursor |
| `.windsurfrules` / `.windsurf/rules/*.md` | Windsurf |
| `.clinerules` / `.clinerules/*.md` | Cline / Roo Code |
| `.trae/rules/*.md` | Trae |
| `GEMINI.md` / `.idx/airules.md` | Gemini CLI / Firebase Studio |
| `.github/copilot-instructions.md` / `.github/agents/*.agent.md` | GitHub Copilot |
| `AGENTS.md` | 通用标准（Codex / Copilot / Devin / Kimi Code / Zed / Aider 等） |
| `.kimi-code/` 或 `~/.kimi-code/AGENTS.md` | Kimi Code |

#### 检测规则

1. **强信号优先**：项目里存在某 Agent 专属文件，就直接判定该 Agent 被使用。
2. **AGENTS.md 是跨工具信号**：单独存在 `AGENTS.md` 时，视为“多 agent / 通用标准”场景。
3. **多 Agent 共存**：如果同时检测到 `CLAUDE.md` + `AGENTS.md` + `.cursorrules`，`detected_agents` 应包含多个，走多 agent 产物策略。
4. **无信号时直接问**：如果项目没有任何 agent 配置文件，把 Agent 选择合并进问题 1 或单独问：

   > 你主要用哪个 AI coding 工具？
   > - A. Claude Code
   > - B. Cursor / Windsurf / Cline / Trae 等 IDE 内置 Agent
   > - C. GitHub Copilot / OpenAI Codex / Kimi Code 等 CLI Agent
   > - D. 多个工具混用

5. **默认回退**：用户未回答且无信号时，默认生成 `AGENTS.md`（通用性最好）；如果环境能识别当前运行的是 Claude Code，可默认 `CLAUDE.md`。

---

## Step 2: 定 Profile（Classify）

基于扫描信号判断项目类型。MVP 只支持一个主 Profile，可选一个次 Profile。

### 2.1 Profile 信号表

| Profile | 强信号 | 弱信号 |
|---------|--------|--------|
| `coding` | `pyproject.toml` + `src/` + `tests/`；`go.mod` + `main.go`；`Cargo.toml`；**大量可执行脚本**（`*.py`, `*.sh`, `Makefile`, `Snakefile`）+ inference/pipeline 语义文件名（如 `batch_infer.py`, `run.sh`, `inference/`, `pipeline/`） | `package.json` + CLI/库结构；少量 Python 脚本 + 无标准结构 |
| `frontend-product` | `package.json` + `app/`/`pages/` + `components/` + UI 框架 | 纯 `package.json` 但无 UI 目录 |
| `product-design` | `PRD.md`, `docs/PRD*`, 大量产品文档 | 有 `docs/` 但无 PRD |
| `research` | `papers/`, `references/`, 大量 PDF/Markdown 笔记, `*.tex` | 少量参考资料 |
| `writing-docs` | 以 `docs/` 为主且无代码依赖，或明确写作目标 | 代码仓库附带 docs |
| `data-analysis` | `*.ipynb`, `dbt_project.yml`, `.dbt/`, 明显分析性 README | 单独的 `*.sql`, `*.parquet`, `*.csv`, `*.xlsx`（这些只是数据输入，不是分析目的） |
| `creative-media` | `remotion.config.*`, 媒体资产, 脚本目录 | 零散媒体文件 |

### 2.2 置信度规则

- `0.80 - 1.00`: 直接推荐，可跳过问题 1。
- `0.50 - 0.79`: 推荐 + 问 1-2 个问题。
- `0.00 - 0.49`: 进入空项目/不确定问答流。

### 2.3 避免误判

- 文件少时不过度自信。
- `README` 和依赖冲突时，优先问用户目标。
- 有 `docs/` 不一定是写作项目；有 `package.json` 不一定是前端。
- **可执行脚本优先于数据文件**：如果项目里有大量 `*.py` / `*.sh` / `Makefile` / `Snakefile` / `batch_infer*` / `run.sh` / `inference*` 等执行或 pipeline 文件，即使同时有很多 `.sql` / `.parquet` / `.csv`，也优先判为 `coding`，数据相关 atom 作为辅助召回。
- **SQL 文件本身不是分析目的**：`.sql` 在 inference pipeline 里通常只是数据提取步骤，单独存在不足以把主 profile 拉成 `data-analysis`。

---

## Step 3: 问问题（Ask，仅在低置信度时）

最多问 2 个问题，每个最多 3 个选项。高置信度不问。

### 问题 1：你接下来主要想让 agent 做哪类工作？

- **A. 改项目**（偏 coding / frontend-product / data-analysis / creative-media）
- **B. 理清项目**（偏 research / product-design / architecture-review / context-update）
- **C. 产出材料**（偏 writing-docs / product-design / research / creative-media）

### 问题 2：你最不想反复解释哪类信息？

- **A. 项目事实**（目标、目录、技术栈、命令、数据表、关键资料）
- **B. 工作标准**（代码规则、产品判断、UI 质量、研究证据、数据口径）
- **C. 输出格式**（文档结构、引用格式、SQL 输出、设计报告口径）

如果扫描信号强，只问问题 2；如果已有上下文文件，先做 review，再问用户最想减少哪类重复说明。

---

## Step 4: 召回 Guideline Atoms

读取 `guidelines/**/*.md`，按 frontmatter 筛选。**选定 atom 后，必须实际调用 `tools/render-atoms.py` 渲染规则 section，并把脚本的完整输出粘贴进 proposal。禁止用占位符代替。**

### 4.0 使用渲染脚本（必须执行）

为避免 LLM 无意识改写、压缩或丢失 atom 原文，规则部分（`Working Rules` / `Verification` / `Safety`）**必须**由 `tools/render-atoms.py` 确定性生成。你不可以直接写规则内容，也不可以用 `[渲染内容]`、`<!-- 待渲染 -->` 之类的占位符。

执行命令：

```bash
python3 tools/render-atoms.py \
  --working-standard <atom1>,<atom2> \
  --verification <atom3>,<atom4> \
  --safety <atom5> \
  --output /tmp/rendered-rules.md
```

然后读取 `/tmp/rendered-rules.md` 的内容，**完整粘贴**到 proposal 中。

- 脚本读取 atom 文件，原样输出核心句 + 展开。
- 脚本只生成规则 section；`Project Overview`、`Commands`、`Reference Docs` 仍由你根据 Step 1 检测结果手写。
- 如果找不到 `tools/render-atoms.py`，先定位 skill 根目录：`find ~/.claude/skills/auto-context -name render-atoms.py` 或 `find . -name render-atoms.py`。

**未实际调用脚本就展示 proposal，等同于输出未完成。**

### 4.1 召回规则

1. **通用 atom**: `profiles: [all]` → 全部召回。
2. **Profile atom**: `profiles` 含主 Profile 或次 Profile → 召回。
3. **触发器二次过滤**: `triggers.files` 存在时，项目无对应文件则不召回。
4. **用户意图过滤**: `triggers.user_intents` 存在时，与用户答案不匹配则不召回。

### 4.2 读取内容

每个 atom 文件包含：
- frontmatter: `name`, `description`, `profiles`, `scopes`, `priority`, `triggers`, `conflicts`
- 正文: 加粗核心句 + 展开 + 验收句

**规则部分由 `tools/render-atoms.py` 渲染，不要手工改写。** 脚本会：
- 原样输出核心句
- 原样输出展开部分的所有 bullet 和引导语
- 不输出验收句（`This is working if:` 只用于 Review 验证）

你唯一需要做的是：决定每个 atom 进哪个 section（Working Rules / Verification / Safety），然后把它交给脚本。

### 4.3 禁止改写 atom 原文（硬规则）

`Working Rules` / `Verification` / `Safety` 里的条目**必须直接来自 atom 文件**，规则如下：

- **必须通过 `tools/render-atoms.py` 渲染**，不要手工写、不要复制粘贴后再修改、不要让 LLM 重新表述。
- **允许**：脚本为了格式缩进添加的空格和 bullet 标记。
- **禁止**：
  - 改写核心句的语义
  - 添加 atom 里没有的解释、例子、项目细节
  - 删除或合并展开 bullet
  - 把多条 atom 揉成一条新规则

**如果 atom 的内容不适合直接渲染，说明选错了 atom。** 应该 omit 该 atom 或换一条更合适的，而不是改写它。

Review 阶段会把脚本输出和 atom 原文做 `diff`，任何非空白差异都视为改写。

---

## Step 5: 组合（Compose）

将检测事实、用户回答、召回 atom 组合成候选集，再排序去重。

### 5.1 组合步骤

1. **分离两类内容**（必须分清，不能混）：
   - **项目事实（Project Facts）**: 来自 Step 1 检测，包括技术栈、目录、命令、已有上下文文件、关键文档位置。项目事实只进 `Project Overview`、`Commands`、`Reference Docs` 三个 section。
   - **准则原子（Guideline Atoms）**: 来自 Step 4 召回，只进 `Working Rules`、`Verification`、`Safety` 三个 section。
2. **渲染规则 section**：把选定的 atom 名按 section 分组，调用 `tools/render-atoms.py`，得到确定性的规则 markdown。
3. **按 priority 排序**: `high` > `medium` > `low`。排序在调用脚本前完成；脚本按你给的顺序输出。
4. **去重**: 同义或同目标 atom 只保留一条，记录被合并项。
5. **解决冲突**: 若 atom 声明 `conflicts`，只保留更相关或更高优先级的一条。
6. **限制 omit（严格）**：
   - `priority: high` 的 atom **默认不省略**。
   - `profiles: [all]` 的 atom **默认不省略**。
   - 省略一条 atom 必须给出具体证据："如果删除它，agent 会在 [具体场景] 犯错"，而不是"它看起来不关键"或"全局文件已覆盖"。
   - **全局 `~/.claude/CLAUDE.md` 永远不构成省略理由**。
   - **不能因为两条 atom "看起来重叠"就省略其中一条**；只有 frontmatter 明确声明 `conflicts` 时才解决冲突。
7. **检查元规则**: 确保不违反 M7/M8（每行有价值、< 200 行）。

### 5.2 严格禁止流程泄漏

以下内容是**流程/技能**，**不许**写进 `CLAUDE.md` / `AGENTS.md` / 任何 agent 上下文文件：

- 多步骤操作手册（例如“dry-run → 检查输出 → 再跑生产”）
- Prompt 工程迭代流程
- 实验记录 / 实验报告撰写流程
- Code review 流程
- 部署/发布流程
- 任何需要按顺序执行 3 步以上的操作说明

这些东西如果项目里已有文档（README、Cursor Skill、内部 wiki），**只在 `Reference Docs` 里给一行指针**，例如：

```md
## Reference Docs (read when relevant)
- `docs/deployment.md` — 部署流程
- `.cursor/skills/experiment-logging/` — 实验记录 skill
```

如果项目里**没有**相关文档，不要顺手在上下文文件里写一个。应该建议用户做成 `.claude/skills/` 或 `.cursor/skills/`。

### 5.2 输出

```json
{
  "selected_guidelines": ["read-before-editing", "small-scoped-changes", "run-smallest-relevant-test"],
  "artifact_targets": ["CLAUDE.md"],
  "omitted_guidelines": ["verify-rendered-ui: 无前端文件"]
}
```

---

## Step 6: 选择产物并渲染 Proposal

### 6.1 产物选择

产物选择由 `detected_agents` 和项目规模共同决定：

| 场景 | 产物 |
|------|------|
| 单一小项目 + 只用 Claude Code | `CLAUDE.md` |
| 单一小项目 + 只用 Cursor/Windsurf/Cline/Trae | `AGENTS.md`（通用）+ 该工具原生规则文件（可选） |
| 代码项目 + 多 agent | `AGENTS.md` 为主 + `CLAUDE.md` import `AGENTS.md` |
| 大型/混合项目 | `AGENTS.md` + `CLAUDE.md` + `.claude/rules/*.md` |
| 已有 `AGENTS.md` | `CLAUDE.md` 中写 `@AGENTS.md`，不重复；其他工具文件 import `AGENTS.md` |
| 空项目 | 最小 `AGENTS.md`（通用）或最小 `CLAUDE.md`（若确认只用 Claude） |

#### Agent 与产物映射

| 主要 Agent                     | 首选产物                                                | 备注                                              |
| ---------------------------- | --------------------------------------------------- | ----------------------------------------------- |
| Claude Code                  | `CLAUDE.md`                                         | 若存在其他 agent，加 `AGENTS.md` 并让 `CLAUDE.md` import |
| Cursor                       | `AGENTS.md` + `.cursor/rules/*.mdc`（可选）             | Cursor 也读 `AGENTS.md`，优先通用标准                    |
| Windsurf                     | `AGENTS.md` + `.windsurfrules`（可选）                  | Windsurf 也读 `AGENTS.md`                         |
| Cline / Roo Code             | `AGENTS.md` + `.clinerules`（可选）                     | Cline 生态通常共用 `.clinerules`                      |
| GitHub Copilot               | `AGENTS.md` + `.github/copilot-instructions.md`（可选） | Copilot 官方文件，团队场景优先                             |
| OpenAI Codex                 | `AGENTS.md`                                         | Codex 原生标准                                      |
| Kimi Code                    | `AGENTS.md`                                         | Kimi Code 原生标准                                  |
| Devin                        | `AGENTS.md`                                         | Devin 推荐标准                                      |
| Zed                          | `AGENTS.md`                                         | Zed 原生首选                                        |
| Gemini CLI / Firebase Studio | `AGENTS.md` + `GEMINI.md`（可选）                       | Gemini 也读 `AGENTS.md`                           |
| Trae                         | `AGENTS.md` + `.trae/rules/*.md`（可选）                | Trae 自有规则格式                                     |

原则：**尽量以 `AGENTS.md` 为单源，各工具原生文件只 import 或引用它，不重复内容。**

### 6.2 CLAUDE.md / AGENTS.md 结构

两个文件使用同一套 section 结构。`AGENTS.md` 是单源，`CLAUDE.md` 只 import 它并补充 Claude-specific 的指针。

```md
# Project Context

## Project Overview
- Workspace state: existing project
- Primary profile: frontend-product
- Detected agents: claude-code, cursor
- Detected stack: TypeScript, React, Vite
- Important directories: src/, tests/, docs/
- Existing agent configs: .cursor/skills/, .claude/memory-graph/

## Commands
- Install: npm install
- Run: npm run dev
- Test: npm test
- Build: npm run build

## Working Rules
- **Read relevant files before changing them.** [read-before-editing]
  - Before modifying a file:
  - Read the target file and its immediate context.
  - Trace how the code is called and what depends on it.
  - Check existing patterns, naming, and conventions in the same area.
  - If unsure how something works, read it first. Don't guess.

- **Make the smallest change that solves the problem.** [surgical-changes]
  - When editing existing code:
  - Don't "improve" adjacent code, comments, or formatting.
  - Don't refactor things that aren't broken.
  - Match existing style, even if you'd do it differently.
  - If you notice unrelated dead code, mention it. Don't delete it.
  - When your changes create orphans:
  - Remove imports, variables, or functions that YOUR changes made unused.
  - Don't remove pre-existing dead code unless asked.

## Verification
- **Run the smallest relevant test first.** [run-smallest-relevant-test]
  - Before claiming a change works, run the smallest test that exercises it.
  - Prefer focused unit or integration tests over manual end-to-end runs.
  - If no test exists, create the smallest reproduction before fixing.

## Safety
- **Do not run destructive git commands unless explicitly requested.** [no-destructive-git]
  - No `git reset --hard`, `git clean -fd`, force-push, or branch deletion without confirmation.

## Reference Docs (read when relevant)
- `README.md` — 项目背景
- `docs/architecture.md` — 架构设计

## When to Update This File
- Add new stack/tool after it stabilizes.
- Move path-specific rules to .claude/rules/.
- Move multi-step workflows to .claude/skills/.
```

#### 每个 section 的内容来源

| Section | 来源 | 示例 |
|---------|------|------|
| `Project Overview` | 检测结果 | workspace state、profile、stack、dirs、existing agent configs |
| `Commands` | 检测结果 | install / run / test / build |
| `Working Rules` | **`tools/render-atoms.py` 输出** | `--working-standard read-before-editing,surgical-changes` |
| `Verification` | **`tools/render-atoms.py` 输出** | `--verification run-smallest-relevant-test` |
| `Safety` | **`tools/render-atoms.py` 输出** | `--safety no-destructive-git` |
| `Reference Docs` | 检测到的关键文档指针 | `README.md`、`docs/...`、现有 skill 目录 |
| `When to Update` | 固定模板 | 稳定后更新、路径规则下沉、流程拆 skill |

**Working Rules / Verification / Safety 里的每一条都必须满足：**
1. **来源**: 由 `tools/render-atoms.py` 从 atom 文件直接渲染，不经 LLM 改写。
2. **格式**: 核心句作为一级 bullet，展开作为缩进内容（保留 atom 原结构）。
3. **标注**: 核心句末尾标注 `[atom-name]`。
4. **可反向验证**: Review 阶段把脚本输出和 atom 原文做 `diff`，必须完全一致（除缩进和 bullet 标记外）。

**错误示例（手工改写）**: 
```md
- Touch only what you must. `[surgical-changes]`
```
问题：没有展开，且核心句被改写。

**正确示例（脚本输出）**: 
```md
- **Touch only what you must. Clean up only your own mess.** `[surgical-changes]`
  - When editing existing code:
  - Don't "improve" adjacent code, comments, or formatting.
  - Don't refactor things that aren't broken.
  - Match existing style, even if you'd do it differently.
  - If you notice unrelated dead code, mention it. Don't delete it.
  - When your changes create orphans:
  - Remove imports, variables, or functions that YOUR changes made unused.
  - Don't remove pre-existing dead code unless asked.
```

### 6.3 Proposal 输出格式

生成 proposal 并通过 Step 6.5 Review 后直接写入文件，默认不需要用户确认：

```md
## Auto Context Proposal

Detected state: existing project
Primary profile: frontend-product
Secondary profile: coding
Confidence: 0.84
Detected agents: claude-code, cursor

Evidence:
- package.json includes vite, react, typescript
- src/ and components/ exist
- README contains local dev command
- Existing `.cursorrules` and `CLAUDE.md` found

Recommended files:
- Update AGENTS.md（单源，跨 agent 共享）
- Update CLAUDE.md（import AGENTS.md）
- Create .cursor/rules/frontend.mdc（Cursor 专属 UI 规则）

调用脚本生成规则 section（必须在 proposal 中展示完整输出）：

```bash
python3 tools/render-atoms.py \
  --working-standard read-before-editing,surgical-changes \
  --verification run-smallest-relevant-test \
  --safety no-destructive-git \
  --output /tmp/rendered-rules.md
```

把 `/tmp/rendered-rules.md` 的完整内容直接粘贴到下面的 preview 中，**不要省略、不要用占位符**。

**Working Rules** / **Verification** / **Safety 预览：**
```markdown
## Working Rules
- **Read relevant files before changing them.** [read-before-editing]
  - Before modifying a file:
  - Read the target file and its immediate context.
  - ...

## Verification
- **Run the smallest relevant test first.** [run-smallest-relevant-test]
  - ...

## Safety
- **Do not run destructive git commands unless explicitly requested.** [no-destructive-git]
  - ...
```

Project facts (for Project Overview / Commands / Reference Docs):
- Stack: TypeScript, React, Vite
- Commands: `npm install`, `npm run dev`, `npm test`
- Key docs: `README.md`, `docs/architecture.md`
- Existing agent configs: `.cursorrules`

Omitted guidelines:
- `do-not-guess-schema` — 无 SQL / 数据文件
- `check-data-grain` — 无数据 pipeline 信号

Reason:
- Project needs both implementation guardrails and UI-quality expectations.
- Frontend-specific rules should be scoped separately to avoid bloating CLAUDE.md.
- Detected both Claude Code and Cursor, so use AGENTS.md as single source.
```

---

## Step 6.5: 自审 Review（写入前强制自检）

在把 proposal 写入文件之前，必须先做一次 self-review。**不要跳过。**

### 6.5.1 Review 检查清单

对生成的 `AGENTS.md` / `CLAUDE.md` / `.claude/rules/*.md` 逐项检查：

| # | 检查项 | 通过标准 | 不通过怎么办 |
|---|--------|---------|-------------|
| 1 | **Atom 来源可追溯** | `Working Rules` / `Verification` / `Safety` 每条末尾都有 `[atom-name]` | 删除无来源条目，或补 atom 标注 |
| 2 | **实际调用脚本渲染** | proposal 中 `Working Rules` / `Verification` / `Safety` 是 `tools/render-atoms.py` 的真实输出，没有 `[渲染内容]` / `<!-- 待渲染 -->` / 省略号占位 | 调用脚本并把完整输出粘贴进 proposal |
| 3 | **无 atom 改写** | 脚本输出与 atom 原文做 `diff`，除缩进和 bullet 标记外完全一致 | 改回 atom 原文；若 atom 原文不合适则 omit 该 atom |
| 4 | **展开完整保留** | 每条规则都有核心句 + 缩进展开；没有只剩一句口号 | 补回 atom 展开；调用脚本重新渲染 |
| 5 | **无流程泄漏** | 没有“先 X，再 Y，最后 Z”类的多步流程；没有 numbered steps 1/2/3 | 移到 `Reference Docs` 给指针，或建议做成 skill |
| 6 | **无项目事实混入 Working Rules** | Working Rules 里不出现具体命令、目录路径、文件名、工具参数 | 把项目事实移到 `Project Overview` / `Commands` / `Reference Docs` |
| 7 | **无过度 omit** | `priority: high` 和 `profiles: [all]` 的 atom 未被省略；omit 理由不是"全局已覆盖"或"看起来重叠" | 把不该省略的 atom 加回来 |
| 8 | **长度合规** | 每个文件 ≤ 200 行 | 拆分 `.claude/rules/`，或裁剪低优先级 atom |
| 9 | **无占位符** | 没有 `[TBD]`、`[待填]`、空括号等未填内容 | 删除或补全；无法补全的标 `[UNVERIFIED]` 并说明 |
| 10 | **无冲突规则** | 不存在互相矛盾的指令（例如“总是做 X” vs “绝不做 X”） | 保留更相关/更高优先级的一条，删除另一条 |
| 11 | **Agent 产物匹配** | 生成的文件与 `detected_agents` 一致（Claude → CLAUDE.md，多 agent → AGENTS.md 为主） | 按 Step 6.1 重新选择产物 |
| 12 | **项目事实准确** | `Project Overview` / `Commands` 里的技术栈、目录、命令与扫描到的文件一致 | 回 Step 1 重新检测 |
| 13 | **无重复 README 大段内容** | 没有从 `README.md` 整段复制进上下文文件 | 改成一句话摘要或指针 |
| 14 | **无 lint/format 规则口语化** | 没有把 ESLInt/Prettier/black 等格式规则写成自然语言大段 | 删除，交给项目已有 linter |

#### 反向抽查（必须执行）

抽查由脚本渲染的 atom 输出：

1. 随机抽取 3 个已渲染的 atom。
2. 用 `diff`（或重新调用 `tools/render-atoms.py` 对该 atom 单独渲染）对比脚本输出和 atom 原文。
3. 核心句 + 展开内容必须完全一致，除以下允许项外：
   - 行首缩进空格
   - bullet 标记 `-` / `*`
   - 行尾空白
4. 任何非允许差异 → 判定为 **atom 改写**，Review 不通过。

#### Review 不能全是 ✅

**任何 proposal 都能找到至少一个可改进点。** 如果 Review 表 14 项全是 ✅，说明 Review 做得太松。必须至少找到一项：

- 某条可以删的 atom（M7：删了不会犯错）
- 某条表述可以更贴近 atom 原文
- 某条展开可以补回或压缩得更准确
- 某个项目事实可以改成更简洁的指针
- 某个 section 可以拆到 `.claude/rules/`

把至少一个改进点写进 Review 输出。

### 6.5.2 Review 输出格式

把自审结果附加在 proposal 后面一起展示：

```md
---

## Auto Context Review

| 检查项 | 状态 | 说明 |
|--------|------|------|
| Atom 来源可追溯 | ✅ | 8/8 条已标注 `[atom-name]` |
| 无流程泄漏 | ⚠️ | `Pipeline 操作纪律` 含 4 步流程，需移除 |
| 长度合规 | ✅ | AGENTS.md 约 48 行，CLAUDE.md 约 12 行 |
| 无冲突规则 | ✅ | 未发现冲突 |

### 需修正的问题

1. **流程泄漏**：`## Working Standards` 下的 `Pipeline 操作纪律` 是 4 步操作流程，不是 atom。应改为：
   ```md
   ## Reference Docs (read when relevant)
   - `user_memory_inference/README.md` — 生产推理运行流程
   ```

2. **缺少 atom 来源**：`Prompt 工程` 小节无 `[atom-name]`，且内容来自 README。应删除或改为 Reference Docs 指针。

### 修正后的文件预览

[这里放修正后的 AGENTS.md / CLAUDE.md 预览]
```

### 6.5.3 Review 不通过的处理

- **发现 atom 改写**：必须改回 atom 原文。如果 atom 原文确实不适合本项目，omit 该 atom 而不是改写。
- **发现 1-2 个小问题**（流程泄漏、项目事实位置不对、个别 atom 选错）：直接修正，不重新问用户。
- **发现结构性问题**（产物选择错误、大量流程泄漏、错误 Profile、过度 omit）：修正后重新生成 proposal，并重新 Review。
- **Review 表全 ✅**：退回重审，必须找到至少一个可改进点。
- **不确定是否算泄漏/改写**：按保守原则处理——“这是不是 atom 文件里有的句子？”不是则删或改。

---

## Step 7: 写入（Write，默认自动落盘）

### 7.1 写入规则

- **默认直接写入**：`auto-context` 是确定性工具流程，生成 proposal 并通过 Step 6.5 Review 后直接写入文件，不需要等用户说「写」或「确认」。
- **Review 不通过时不写**：如果 Review 发现 atom 改写、占位符、流程泄漏等问题，先修正，修正后再写；无法修正时向用户报告问题，不写半成品。
- **不覆盖已有文件**：已有 `CLAUDE.md` / `AGENTS.md` 时生成 patch / review，不直接覆盖。
- 多 agent 场景：以 `AGENTS.md` 为单源，`CLAUDE.md` 只 import，不重复内容。
- 写入前做最终 lint（Step 6.5 Review 的子集，最后再过一遍）：
  - 文件是否 > 200 行？
  - 是否包含未填占位符？
  - `Working Rules` / `Verification` / `Safety` 是否实际调用了 `tools/render-atoms.py`？（检查 proposal 中是否有脚本调用记录和完整输出）
  - `Working Rules` / `Verification` / `Safety` 里的每条是否都标注了 `[atom-name]`？
  - 是否把多步流程塞进了 `CLAUDE.md` / `AGENTS.md`？（检查是否有“先 X，再 Y，最后 Z”式的连续步骤）
  - `Working Rules` / `Verification` / `Safety` 里是否混入了项目事实或操作流程？
  - 是否包含相互冲突的规则？

### 7.2 写入后的默认提示

写入完成后，告诉用户：
- 生成了哪些文件
- 建议何时更新
- 如果有 `.claude/rules/` 或 `.claude/skills/` 建议，列出下一步

---

## 元规则（AutoContext 自己守）

执行本 skill 时，必须同时遵守：

1. **少生成，而不是多生成**: 没检测到的项目事实不编；没必要的 atom 不召回。
2. **先审再写**: 默认生成 proposal 并通过 Review 后直接落盘，不需要用户确认；Review 不通过时不写。
3. **不覆盖已有文件**: 已有上下文文件走 review/patch 模式。
4. **CLAUDE.md < 200 行**: 超出时拆分 `.claude/rules/`，而不是把文件写长。
5. **Profile 是召回维度，不是产物**: 不要把 Profile 名称写进最终 `CLAUDE.md`。
6. **流程不进 CLAUDE.md**: 多步骤流程应建议做成 `.claude/skills/`，不塞进项目上下文文件。
7. **同一条准则只在一处**: 不在 `CLAUDE.md` 和 `AGENTS.md` 中重复。
8. **优先检测 Agent 再选产物**: 根据 `detected_agents` 决定输出文件，不默认给所有项目写 `CLAUDE.md`。
9. **多 Agent 以 AGENTS.md 为单源**: 各工具原生文件只 import / 引用 `AGENTS.md`，不复制内容。
10. **项目事实与 atoms 必须分离**: 项目事实只进 `Project Overview` / `Commands` / `Reference Docs`；atoms 只进 `Working Rules` / `Verification` / `Safety`。
11. **全局 CLAUDE.md 不免除项目 atom**: 检测到全局 `~/.claude/CLAUDE.md` 时，不因此省略本项目的通用 atom。全局是用户偏好，项目是项目约束，两者不互斥。
12. **写入前必须自审**: 每次生成 proposal 后，执行 Step 6.5 Review 检查清单。不通过就修正，修正后再写入；不把有问题的文件直接落盘。
13. **禁止改写 atom 原文**: `Working Rules` / `Verification` / `Safety` 必须通过 `tools/render-atoms.py` 渲染，不准许 LLM 手工改写、压缩或重新表述。
14. **高优先级 atom 默认保留**: `priority: high` 和 `profiles: [all]` 的 atom 不随意省略。省略必须给出"不保留会导致什么具体错误"的证据。
15. **Review 必须反向抽查**: 随机抽取 3 个已渲染 atom，用 `diff` 对比脚本输出和 atom 原文。核心句 + 展开必须完全一致（除缩进和 bullet 标记外）。
16. **Review 不能全 ✅**: 任何 proposal 至少存在一个可改进点。全 ✅ 说明 Review 太松，需要重审。
17. **规则必须带展开**: `Working Rules` / `Verification` / `Safety` 不能只写一句口号。每条必须包含 atom 核心句 + 缩进展开，让 agent 知道具体怎么做。
18. **可执行脚本优先于数据文件**: 判定 profile 时，如果项目同时有 `*.py` / `*.sh` / `Makefile` / `Snakefile` / `inference*` / `batch_*` / `run.sh` 等执行或 pipeline 文件，以及 `.sql` / `.parquet` / `.csv` 等数据文件，优先判为 `coding`，数据相关 atom 仅作辅助召回。
19. **扫描要高效**: 项目检测阶段只用 `tree -L 2` 一次拿结构，再挑关键文件读前 30 行。不要逐个目录 `ls`，不要全文读取，不要用 shell 探索 skill 自身文件结构。
20. **规则 section 必须用脚本渲染**: 选定 atom 后，调用 `tools/render-atoms.py` 生成 `Working Rules` / `Verification` / `Safety`，不手工拼接。
21. **禁止占位符代替脚本输出**: proposal 中 `Working Rules` / `Verification` / `Safety` 必须是脚本真实输出，不允许用 `[渲染内容]`、`<!-- 待渲染 -->`、省略号或任何简写占位。

---

## 可选扩展

- 对已有 `CLAUDE.md` 做 Context Smell 检测（bloat / skill leakage / lint leakage / conflicting instructions）。
- 生成 `.claude/rules/` 拆分规则。
- 支持导出 Cursor rules / Windsurf rules（v1.0）。
