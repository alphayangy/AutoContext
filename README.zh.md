# Auto Context

> [English](README.md) | 中文

面向 AI coding agent 的项目接入 skill + 上下文编译器。

扫描工作区、识别项目画像、召回 guideline atoms，并生成精简而有效的 `CLAUDE.md`、`AGENTS.md` 或各 agent 专属的上下文包。

## 为什么需要它

每次新开 agent 会话都要重复一遍：解释项目背景、重申约定、纠正同样的错误。现有工具只解决了其中一部分：

- **覆盖太窄。** Claude Code `/init` 和 `AGENTS.md` 主要仍是面向代码仓库的。研究报告、产品文档、数据分析、写作项目、创意内容等非代码工作被排除在外 —— 用户只能为纯工程以外的项目从零手写上下文。
- **质量太脆。** 手写的 `AGENTS.md` / `CLAUDE.md` 很快就会堆积上下文质量问题：大段复制 README、把多步流程泄漏进去、把 lint 规则写成散文、指令互相矛盾。结果是 agent 漏掉约束、自相矛盾，或者在噪声里浪费 token。
- **缺少可信的"怎么做"层。** `/init` 告诉 agent 项目**是什么**，skills 告诉 agent 怎么跑某个具体流程。但两者之间缺少稳定、可复用的工作标准 —— "先读再改"、"跑最小相关测试"、"不要猜 schema" 这类准则，agent 每次都要重新学习。

Auto Context 是一个带有**精选工作准则库**的**上下文编译器**：

- **覆盖广**：通过 Context Profile 同时支持代码和非代码工作。
- **控质量**：选择、排序、确定性渲染准则 —— LLM 不会简化规则、不会复制 README、不会泄漏流程。
- **来源可信**：准则来自对全网大量真实 `CLAUDE.md` / `AGENTS.md` 的抓取、review 和提炼，以及对 agent manifests 的实证研究。这是从大量项目里提取出的可复用工作标准，不是为某一次会话临时编造的。
- **关注点分离**：项目事实和长期准则进 `CLAUDE.md` / `AGENTS.md`，多步流程建议拆成 `.claude/skills/`，路径规则进 `.claude/rules/`。

> `/init` for every kind of work，不只是代码仓库。

## 支持的 Agent

| Agent | 输出文件 | 安装路径 |
|-------|---------|---------|
| Claude Code | `CLAUDE.md` + `AGENTS.md` | `~/.claude/skills/auto-context/` 或 `.claude/skills/auto-context/` |
| Cursor | `AGENTS.md` + `.cursor/rules/`（可选） | `.cursor/skills/auto-context/` |
| Kimi Code | `AGENTS.md` | 项目根目录或 `.kimi-code/` |
| Windsurf / Cline / Trae | `AGENTS.md` + 原生规则 | `.windsurfrules` / `.clinerules` / `.trae/rules/` |

## 安装

### 通过 install 脚本

```bash
git clone https://github.com/alphayangy/AutoContext.git
cd AutoContext
bash install.sh
```

默认会为 Claude Code 安装全局 skill，并为当前项目的 Cursor 安装 skill。可用参数自定义：

```bash
bash install.sh --claude-global    # Claude Code 全局 skill
bash install.sh --claude-project   # Claude Code 项目级 skill
bash install.sh --cursor-project   # Cursor 项目级 skill
bash install.sh --kimi-project     # Kimi Code 项目级 AGENTS.md
bash install.sh --all              # 全部安装
```

### 手动安装

```bash
# Claude Code（全局）
cp -r AutoContext ~/.claude/skills/auto-context

# Claude Code（项目级）
cp -r AutoContext .claude/skills/auto-context

# Cursor（项目级）
cp -r AutoContext .cursor/skills/auto-context
```

## 使用

### 在 Claude Code 中

在任意项目中运行：

```
/auto-context
```

它会自动：
1. 扫描项目。
2. 识别画像和 agent。
3. 选择 guideline atoms。
4. 通过 `tools/render-atoms.py` 渲染规则。
5. 自动写入 `AGENTS.md` 和/或 `CLAUDE.md`。

### 独立使用 atom 渲染器

你也可以单独使用确定性渲染器，而不跑完整 skill：

```bash
python3 tools/render-atoms.py \
  --working-standard read-before-editing,surgical-changes \
  --verification ensure-runs-before-claiming-done \
  --safety no-secrets \
  --output /tmp/rules.md
```

## 项目结构

```
auto-context/
├── SKILL.md                  # Claude Code / Cursor 的 skill 入口
├── README.md                 # 英文文档
├── README.zh.md              # 中文文档
├── LICENSE                   # MIT
├── install.sh                # 多 agent 安装脚本
├── .gitignore
├── guidelines/               # Guideline atoms
│   ├── working-standard/     # 工作规则
│   ├── verification/         # 验证规则
│   ├── safety/               # 安全规则
│   └── output-format/        # 输出风格规则
├── references/               # 参考文档（元规则等）
│   └── meta-rules.md
└── tools/
    ├── render-atoms.py       # 确定性 atom 渲染器
    └── verify-context.py     # 校验 CLAUDE.md / AGENTS.md 引用方向
```

## Guideline Atoms

每个 atom 是一个带 YAML frontmatter 的 markdown 文件：

```yaml
---
name: read-before-editing
description: Read before modifying any file.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Read Before Editing

**Understand the context before changing it.**

Before modifying a file:
- Read the target file and its immediate context.
- Trace how the code is called and what depends on it.
- Check existing patterns, naming, and conventions in the same area.
- If unsure how something works, read it first. Don't guess.

**This is working if:** edits match existing patterns and don't break callers the author didn't check.
```

Atoms 按 `working-standard`、`verification`、`safety`、`output-format` 分组。

## 自定义

添加你自己的 atoms：

1. 在 `guidelines/<section>/` 下新建 `.md` 文件。
2. 添加 frontmatter：`name`、`profiles`、`priority`，可选 `triggers`/`conflicts`。
3. 写一句加粗的核心句、展开 bullets、以及验收句。
4. 重新安装或 symlink skill 到你的 agent。

## License

MIT
