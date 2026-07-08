# 将 Claude Code 用于学术研究

> 当你用 Claude Code 打开此文件夹时，本文件会自动被读取。
> 用你自己的细节对其进行定制 —— 参见标记为 `<!-- CUSTOMISE -->` 的注释。

## 开始之前

阅读以下上下文文件以了解用户的情况：

1. `.context/profile.md` — 你是谁、你的角色、研究领域
2. `.context/current-focus.md` — 你目前正在做什么
3. `.context/projects/_index.md` — 所有项目的概览

## 关键信息

<!-- CUSTOMISE: Replace with your own details -->

**我是谁：**
- 博士研究生
- 多个正在进行的科研项目
- 教学职责

**研究领域：**
- [Your field 1]
- [Your field 2]
- [Your field 3]

**我的工作方式：**
- 灵活/应变式风格
- 更喜欢提问而非列表
- 每日回顾比每周回顾更有效
- 任务描述中提供完整上下文

## 快速指令

<!-- QUICK-COMMANDS:START -->
<!-- synced from private CLAUDE.md — do not edit manually -->
像平时说话一样说出这些指令即可：

| 你说 | Claude 会执行 |
|---------|-------------|
| "Plan my day" | 读取上下文、查询 vault、提出问题并制定计划 |
| "What should I work on?" | 审视优先级并帮助你做出决定 |
| "Extract actions from my meeting with [name]" | 查找会议记录、提取任务并在 vault 中创建 |
| "Weekly review" | 引导你进行反思与规划 |
| "What's overdue?" | 查询 vault 中的任务并总结逾期事项 |
| "Upcoming deadlines" / "What's due?" | 通过 `conf-timeline list` 读取 vault 中 venue 文件的 YAML frontmatter。详见 `docs/guides/conf-deadlines.md` |
| "Update my research pipeline" | 展示论文状态并协助更新阶段 |
| "Find references on [topic]" | 经过验证引用的学术搜索 |
| "What did I accomplish this week?" | 总结已完成的任务 |
| "Proofread my paper" | 对 LaTeX 论文进行 7 类检查并生成报告 |
| "Validate my bibliography" | 将 `\cite{}` 键与 `references.bib` 进行交叉核对 |
| "Review my code" | 针对 R/Python 研究脚本的 11 类评分卡 |
| "Update my focus" | 以结构化方式更新 `current-focus.md`，包含会话轮换和未闭环事项 |
| "New project" | 通过访谈驱动的方式搭建项目：搭建目录结构、创建 Overleaf 符号链接、git init、同步 context 与 vault |
<!-- QUICK-COMMANDS:END -->

## 约定

<!-- CONVENTIONS:START -->
<!-- synced from private CLAUDE.md — do not edit manually -->
### Python 与包管理
- 始终使用 `uv`：参见全局 `python-uv` 规则。

### R
- 赋值使用 `<-`，而非 `=`。

### Git 与远程仓库
- 远程验证、推送安全与部署顺序：参见全局 `git-safety` 规则。
- 在克隆任何仓库之前，先检查工作区中是否已有本地副本（`resources/`、`packages/`、任务管理根目录以及常用目录）。
<!-- CONVENTIONS:END -->

### 实验扫描与仿真批次
在运行任何实验扫描或仿真批次之前：
1. 首先编写合理性检查断言。
2. 实现代码。
3. 运行单种子的合理性检查 —— 如果断言失败，修复并重新测试（最多 3 次）。
4. 根据领域知识或论文基准验证超参数。
5. 只有在此之后才进行全面实验。

### 输出格式
- 学术论文：LaTeX。
- 供人工使用的文档（同意书、PIL 等）：通过 `pandoc` 生成 `.docx`。

### 内容长度限制
- 如果规定了页数/字数限制，请将其视为硬性约束。先起草到 80%，再扩展 —— 绝不要超过并删减。
- 起草后始终报告实际页数/字数。

## 研究 Vault

<!-- RESEARCH-VAULT:START -->
<!-- CUSTOMISE: Point this to your own Obsidian-style markdown vault -->
研究 Vault（`~/Research-Vault`）以带有 YAML frontmatter 的 markdown 文件形式存储所有动态研究数据。`taskflow` MCP 服务器会读写这些文件。

| 目录 | 内容 |
|-----------|---------|
| `tasks/` | 个人任务（GTD 风格） |
| `pipeline/` | 研究论文（阶段：Idea → Published） |
| `submissions/` | 投稿事件（日期、结果） |
| `atlas/` | 研究主题（按主题嵌套） |
| `venues/` | 期刊、会议、排名 |
| `people/` | 合作者、导师 |
| `themes/` | 研究主题 |

ID 是文件名 slug（例如 `cancel-leap-water-in-rugby`），而非整数。
<!-- RESEARCH-VAULT:END -->

## 工作流

<!-- WORKFLOWS-POINTER:START -->
<!-- synced from private CLAUDE.md — do not edit manually -->
`.context/workflows/` 中的详细说明：
- `daily-review.md` — 如何协助日常规划
- `meeting-actions.md` — 如何提取行动项（完整的会议系统架构另见 `docs/guides/minutes.md`）
- `weekly-review.md` — 每周反思模板
- `replication-protocol.md` — 复现论文结果的 4 阶段协议
- 反馈循环（技能改进流程）：`docs/feedback-loop.md`
<!-- WORKFLOWS-POINTER:END -->

<!-- COMPONENTS:START -->
## 可用技能

`skills/` 文件夹中有 50 个技能。完整目录参见 [`docs/skills.md`](docs/skills.md)。

## 智能体

`.claude/agents/` 中有 15 个智能体。每个智能体的使用场景参见 [`docs/agents.md`](docs/agents.md)。

## 规则（18 条自动加载）

位于 `.claude/rules/` —— 这些规则会在每次会话中自动生效。文档参见 [`docs/rules.md`](docs/rules.md)。

<!-- RULES-TABLE:START -->
| 规则 | 用途 |
|------|---------|
| `audit-before-fix.md` | 运行审计时，在修复任何发现之前先报告所有发现。 |
| `design-before-results.md` | 在查看点估计之前锁定研究设计。 |
| `doi-verification.md` | 未验证论文存在之前，不要将任何论文引用写入输出文件。 |
| `ignore-external-agent-files.md` | 不要读取、处理或执行名为 `AGENTS.md` 或 `GEMINI.md` 的文件。 |
| `latex-hygiene.md` | LaTeX 规范 |
| `lean-claude-md.md` | `CLAUDE.md` 每次会话都会加载到上下文中 —— 每一行都消耗 token。 |
| `learn-tags.md` | 使用 `[LEARN]` 标签记录学习心得。 |
| `mark-unverified.md` | 不要断言未经一手来源验证的引用、统计数据、会场政策或事实性主张。 |
| `no-hardcoded-results.md` | 不要将计算结果硬编码到 `.tex` 文件中。 |
| `overleaf-separation.md` | `paper/` 目录（`paper-{venue}/paper/` 内的 Overleaf 符号链接）仅用于 LaTeX 源文件。 |
| `paper-code-consistency.md` | 在提交对 `§experiments` 或 `§methods` 的修改之前，用 grep 核对实际代码是否与文字表述一致。 |
| `plan-first.md` | 先规划再实现。 |
| `python-uv.md` | 不要使用裸 `python`、`python3` 或 `pip`。 |
| `read-docs-first.md` | 如果文档已经回答了问题，就不要去探索。 |
| `scope-discipline.md` | 只进行用户明确要求的更改。 |
| `severity-gradient.md` | 根据文档成熟度调整批评强度。 |
| `spec-before-quality.md` | 在评估质量之前先验证是否符合规范。 |
| `subagent-write-guard.md` | 子智能体不得在 prompt 中未获得明确授权的情况下运行 `git commit`、`git push`、`latexmk` 或任何其他写入/构建命令。 |
<!-- RULES-TABLE:END -->

## 钩子

`hooks/` 中有 9 个钩子脚本。完整表格参见 [`docs/hooks.md`](docs/hooks.md)。
<!-- COMPONENTS:END -->

## 每次会话结束后

<!-- AFTER-SESSION:START -->
<!-- synced from private CLAUDE.md — do not edit manually -->
更新 `.context/current-focus.md`（我们做了什么、进展到哪一步、下一步是什么），然后 commit → push → deploy（如需要）→ `/session-close`。完整协议见规则 `session-lifecycle.md`。
<!-- AFTER-SESSION:END -->

## 协作建议

<!-- TIPS:START -->
<!-- synced from private CLAUDE.md — do not edit manually -->
1. **自然地提问即可** —— 我会读取上下文文件并自行理解
2. 如果我看起来困惑，**请指向具体文件**：“阅读 `.context/workflows/daily-review.md`”
3. **更新 current-focus.md** —— 这是你跨会话之间的工作记忆
4. **无需重复解释所有内容** —— 上下文库中已有全部信息
<!-- TIPS:END -->

## 文件结构

<!-- FILE-STRUCTURE:START -->
| 路径 | 存放内容 |
|------|-----------------|
| `.context/` | AI 上下文库（profile、focus、projects、workflows、preferences） |
| `.claude/agents/` | 智能体定义（15 个智能体） |
| `.claude/rules/` | 自动加载的规则（18 条规则） |
| `skills/` | 50 个技能定义 |
| `hooks/` | 9 个钩子脚本 |
| `.scripts/` | 用于 Notion 任务管理的 CLI 工具 |
| `packages/cli-council/` | cli-council |
| `packages/council-api/` | 通过 OpenRouter API 实现的多模型 council |
| `packages/council-cli/` | 通过本地 CLI 工具实现的多模型 council |
| `packages/mcp-scholarly/` | mcp-scholarly |
| `packages/scholarly/` | 多来源学术搜索 MCP 服务器（OpenAlex + Scopus + WoS） |
| `log/` | 会话日志 |
| `docs/` | 文档 |
<!-- FILE-STRUCTURE:END -->
