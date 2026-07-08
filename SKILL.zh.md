---
name: auto-context
description: 在任何项目开始前、接入时或重新校准时使用。扫描工作区、识别项目场景、组合 guideline atoms，并生成可 review 的 CLAUDE.md、AGENTS.md 或 .claude/rules/ 上下文包。
---

# Auto Context

Project onboarding skill + Context Compiler。生成精简而有效的 agent 上下文文件。

## 何时使用

- 初始化一个新项目
- 给已有项目补上下文
- 重新校准过时的 `CLAUDE.md` / `AGENTS.md`

## 核心流程

```text
检测 → 定 Profile → 提问 → 召回 → 组合 → 渲染 → 自审 → 写入
```

---

## 硬规则

1. `Working Rules` / `Verification` / `Safety` **必须调用 `tools/render-atoms.py`** 渲染，禁止手写，禁止占位符。
2. **禁止改写 atom 原文**，原样粘贴脚本输出。
3. **每条规则末尾必须标注 `[atom-name]`**。
4. **未征得用户明确确认，不得覆盖已有的 `CLAUDE.md` / `AGENTS.md`**。
5. **上下文文件中不写多步流程**。流程应放到 `.claude/skills/` 或 `Reference Docs` 指针。
6. **每个生成文件控制在 200 行以内**，超出时拆到 `.claude/rules/`。
7. **项目事实与 atoms 必须分离**：事实 → `Project Overview` / `Commands` / `Reference Docs`；atoms → `Working Rules` / `Verification` / `Safety`。

---

## Step 1: 检测项目

扫描高信号文件，输出结构化摘要。

**扫描方法：**

- 一次性运行 `tree -L 2` 获取目录骨架。
- 读取以下文件的前 30 行：`README*`、`package.json`、`pyproject.toml`、`go.mod`、`Cargo.toml`、`Makefile`、`docker-compose.yml`、入口脚本。
- 仅按文件名/路径统计信号，不看内容。

**输出摘要必须包含：**

- `workspace_state`：`empty` | `existing` | `partial`
- `detected_stack`：推断出的技术栈
- `profile_scores`：前 1–2 个 profile 及分数、证据
- `detected_agents`：根据已有配置文件推断的 agent
- `confidence`：主 profile 置信度
- `questions`：需要向用户确认的问题

详见 `@skill-docs-zh/detection-guide.md`：完整 agent 文件映射表和输出字段说明。

---

## Step 2: 确定 Profile

选择一个主 profile，可选一个次 profile。

**Profile 列表：**

- `coding`：软件开发、测试、脚本
- `frontend-product`：带 UI 组件的 Web 应用
- `product-design`：PRD、用户旅程、功能设计
- `research`：论文、技术调研
- `writing-docs`：文档、教程、方案
- `data-analysis`：SQL、Notebook、指标分析
- `creative-media`：视频、脚本、内容创作

**置信度规则：**

- `≥ 0.80`：直接推荐
- `0.50–0.79`：问 1–2 个问题
- `< 0.50`：进入空项目/不确定流

**避免误判：**

- 文件少时不过度自信。
- 可执行脚本优先于数据文件。
- 仅有 `docs/` 不代表 `writing-docs`。
- 仅有 `package.json` 不代表 `frontend-product`。

详见 `@skill-docs-zh/profile-guide.md`：完整信号表。

---

## Step 3: 提问

最多问 2 个问题，每个最多 3 个选项。置信度高时跳过。

**问题 1：接下来主要想让 agent 做什么？**

- **A. 改项目** → coding / frontend / data / creative
- **B. 理清项目** → research / product-design / architecture
- **C. 产出材料** → writing / product-design / research / creative

**问题 2：最不想反复解释哪类信息？**

- **A. 项目事实** → 技术栈、目录、命令
- **B. 工作标准** → 代码规则、质量门槛
- **C. 输出格式** → 文档结构、引用格式

---

## Step 4: 召回 Guideline Atoms

读取 `guidelines/index.yaml` 列出可用 atoms，再按 profile 和用户意图筛选。

**召回规则：**

1. 召回所有 `profiles: [all]` 的 atoms。
2. 召回 `profiles` 包含主/次 profile 的 atoms。
3. 若 atom 声明了 `triggers.files`，仅当项目存在对应文件时才召回。
4. 若 atom 声明了 `triggers.user_intents`，仅当用户答案匹配时才召回。

**使用脚本渲染：**

```bash
python3 tools/render-atoms.py \
  --working-standard <atom1>,<atom2> \
  --verification <atom3> \
  --safety <atom4> \
  --output /tmp/rendered-rules.md
```

**硬规则：**

- 完整粘贴脚本输出，禁止占位符。
- 禁止改写、压缩或重新表述 atom 内容。
- 若 atom 不合适，应 omit 而非编辑。

---

## Step 5: 组合

组合检测事实、用户回答和选中的 atoms。

**组合规则：**

- 项目事实 → `Project Overview` / `Commands` / `Reference Docs`
- Atoms → `Working Rules` / `Verification` / `Safety`
- 按 priority 排序：high → medium → low
- 同义 atom 去重
- 按相关性/优先级解决声明的冲突
- `priority: high` 和 `profiles: [all]` 的 atom 仅在提供具体证据时才 omit
- 全局 `~/.claude/CLAUDE.md` 永远不构成省略项目 atoms 的理由
- 上下文文件中不写多步流程

---

## Step 6: 选择产物并渲染 Proposal

**产物选择原则：**

- 只用 Claude Code → `CLAUDE.md`
- Cursor / Windsurf / Cline / Trae → `AGENTS.md` + 可选原生规则文件
- 多 agent → 以 `AGENTS.md` 为单源，`CLAUDE.md` import 它
- 大型/混合项目 → `AGENTS.md` + `CLAUDE.md` + `.claude/rules/`
- 迁移已有 `CLAUDE.md` → 通用规则提取到 `AGENTS.md`，Claude 专属指针留在 `CLAUDE.md`

**文件结构：**

```md
# Project Context

## Project Overview
- Workspace state, profile, stack, dirs, existing configs

## Commands
- Install / run / test / build

## Working Rules
- [rendered atoms]

## Verification
- [rendered atoms]

## Safety
- [rendered atoms]

## Reference Docs
- Pointers to relevant project docs

## When to Update This File
```

详见 `@skill-docs-zh/artifact-guide.md`：完整映射表、proposal 模板和迁移步骤。

---

## Step 7: 自审

写入前必须执行，不得跳过。

**关键检查项：**

- 是否实际调用了 `tools/render-atoms.py`
- 每条规则是否以 `[atom-name]` 结尾
- 是否存在 atom 改写
- 是否泄漏多步流程
- 项目事实是否混入规则 section
- 是否存在 `[TBD]` 等占位符
- 文件长度是否 ≤ 200 行
- `CLAUDE.md` 是否引用 `AGENTS.md`（而非反向）

详见 `@skill-docs-zh/review-checklist.md`：完整 15 项 checklist 和抽查程序。

---

## Step 8: 写入

**写入规则：**

- 自审通过后**默认直接写入**，不需要等用户说「写」或「确认」。
- 自审不通过时不写入。
- 不覆盖已有文件，除非用户确认。
- 多 agent 场景以 `AGENTS.md` 为单源。
- 若同时生成 `CLAUDE.md` 和 `AGENTS.md`，运行 `tools/verify-context.py`。

**写入后的提示必须包含：**

- 写入或更新了哪些文件。
- 写入的 atom 数量和标题，同时给出英文和中文。例如：
  - "6 working rules, 2 verification rules, 1 safety rule / 6 条工作准则、2 条验证准则、1 条安全准则"
  - "Working Rules: read-before-editing, surgical-changes, simplicity-first, ... / 工作准则：改前阅读、精准修改、先简后繁……"
- 建议何时更新该文件。
- 是否有 `.claude/rules/` 或 `.claude/skills/` 的下一步建议。

---

## 元规则

执行本 skill 时遵循 `@skill-docs-zh/meta-rules.md`。
