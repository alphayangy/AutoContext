# Auto Context 设计文档

## 一句话定位

Auto Context 是一个 project onboarding skill，也是一个 Context Compiler：在任何项目开始前或项目进行中，自动识别当前项目/任务场景，匹配合适的 Context Profile，组合准则原子，并生成最小但有效的 `CLAUDE.md`、`AGENTS.md` 或 `.claude/rules/` 配置。

更短的产品表达：

> `/init` for every kind of work, not just code repos.

## 背景判断

现在已经有三类相邻能力，但缺一个中间层：

- Claude Code `/init`：能扫描代码仓库并生成项目级 `CLAUDE.md`，但主要面向代码项目。
- `AGENTS.md`：提供跨 coding agent 的项目说明格式，但仍然偏代码仓库说明。
- Agent Skills / Claude Skills：解决具体流程的按需加载，但 skill 更像动作层，不是“项目场景画像层”。

Auto Context 要补的是：

```text
项目状态识别
  -> 场景 Profile 选择
  -> 少量问题补全
  -> 准则原子组合
  -> 生成上下文文件
  -> 项目进行中维护/拆分
```

它不是再做一个模板库，而是做“agent 开工前校准”和“上下文准则编译”。

## 调研摘要

### 现有机制

Claude Code 文档将 `CLAUDE.md` 定义为持久项目指令文件，用来记录项目架构、构建命令、约定和工作流等上下文。官方建议项目级文件可以放在 `./CLAUDE.md` 或 `./.claude/CLAUDE.md`，并且 `/init` 会分析代码库、生成起始版本；如果已有文件，则建议改进而不是覆盖。来源：[Claude Code memory docs](https://code.claude.com/docs/en/memory)

同一文档还给出关键约束：`CLAUDE.md` 会进入启动上下文，建议保持具体、简洁、结构化，目标长度小于 200 行；如果内容变成多步骤流程或只影响部分代码，应移动到 skill 或 path-scoped rules。来源：[Claude Code memory docs](https://code.claude.com/docs/en/memory)

Claude Skills / Agent Skills 的核心是渐进加载：启动时只加载 skill 名称和描述，任务匹配后才加载完整 `SKILL.md`，必要时再读取脚本、参考资料或模板。来源：[Claude Code skills](https://code.claude.com/docs/en/skills)、[Agent Skills](https://agentskills.io/)

`AGENTS.md` 被定义为 “README for agents”，适合放 setup commands、test commands、style、security considerations 等内容，并被很多 coding agents 支持。来源：[AGENTS.md](https://agents.md/)

### 实证研究启发

一项关于 Claude Code manifests 的实证研究分析了 253 个 `Claude.md` 文件，发现常见内容集中在 operational commands、technical implementation notes 和 high-level architecture。来源：[On the Use of Agentic Coding Manifests](https://arxiv.org/abs/2509.14744)

另一项关于 `AGENTS.md` / `CLAUDE.md` 配置质量问题的研究指出，常见问题包括 Lint Leakage、Context Bloat、Skill Leakage、Conflicting Instructions，其中 Lint Leakage、Context Bloat、Skill Leakage 的出现比例分别达到 62%、42%、35%。来源：[Configuration Smells in AGENTS.md Files](https://arxiv.org/abs/2606.15828)

这些结论说明：Auto Context 不能只生成更多内容，而要主动控制上下文质量。

## 核心产品准则

1. 少生成，而不是多生成。
2. 先推荐和预览，再写入文件。
3. `CLAUDE.md` 只放稳定事实和长期准则（不写一次性任务、不塞多步流程），流程做 Skill 按需加载。
4. 对已有项目优先扫描证据，对空项目优先问最少的问题。
5. 不覆盖用户已有文件，默认生成 proposal 或 patch。
6. 能拆就拆：全局指令、项目指令、路径规则、技能流程不要混在一个大文件里。
7. 用户只回答“当前要做什么”和“最不想重复解释什么”，不要让用户理解内部 Profile 或 artifact 选择。
8. 准则要原子化：一个准则一个文件，最终由项目证据和用户回答组合成上下文。

## 概念分层

AutoContext 严格区分两类概念：**产物层**（给 agent 的内容，最终渲染成文件）和**召回维度**（AutoContext 内部用来决定选哪些 atom 的分类依据）。两者不是并列关系：召回维度驱动产物层的内容选择，Profile 本身不是产物，不直接渲染给 agent。

### 产物层（给 agent 的内容）

按文件分，不是按内容类型分：

```text
~/.claude/CLAUDE.md（全局）
  用户跨项目偏好，用户自己维护
  AutoContext 不生成、不干扰；生成项目 CLAUDE.md 时排除和全局矛盾的准则

./CLAUDE.md（项目级）
  项目事实（检测：技术栈、命令、目录）+ 准则（召回的 atom）
  一个文件，两类内容，都由 AutoContext 组合生成

.claude/rules/
  路径局部规则（只对某些目录/文件生效）

.claude/skills/
  多步流程（按需加载，不进 CLAUDE.md）
  AutoContext 不生成 skill 文件；skills 由用户或第三方提供
```

AutoContext 生成 `./CLAUDE.md` 和 `.claude/rules/`；不生成 `~/.claude/CLAUDE.md`（全局，用户维护）和 `.claude/skills/`（流程，用户或第三方提供）。

AutoContext 的 atom 库只收稳定准则（一个准则一个文件，有核心句 + 展开 + 验收），不收多步流程（多步骤的该做 skill，不进 atom 库）。所以生成 CLAUDE.md 时不会塞流程。如果用户现有 CLAUDE.md 里塞了流程（skill leakage），更新模式（v0.4）会建议拆出去做 skill。

通用 atom（profiles: [all]）是跨项目通用准则，渲染进项目 CLAUDE.md，不是全局文件。全局 `~/.claude/CLAUDE.md` 归用户，AutoContext 只尊重、不写入，且排除和它矛盾的准则。

### 召回维度（AutoContext 内部用）

```text
Context Profile
  当前场景的工作方式分类：代码、产品、研究、写作、数据、创意
  用来从 atom 库召回对应准则，不是产物，不直接渲染

文件信号
  扫描项目文件（package.json、*.tex、references/ 等）得到的证据

用户意图
  用户回答“做哪类工作”“最不想重复解释什么”
```

Auto Context 的主要工作是：用召回维度（Profile + 文件信号 + 用户意图）从 Guideline Atoms 中选择、排序、去重，渲染进产物层（CLAUDE.md / .claude/rules/），并在需要时建议 Skills。

### 三类内容分离

AutoContext 涉及三类内容，各有归属，不混在一个文件里：

| 内容 | 受众 | 归属 | 机制 |
| --- | --- | --- | --- |
| 准则原子（atom） | agent（在项目里守） | `guidelines/` + `techniques-overview.md`（候选） | 渲染进 CLAUDE.md/rules |
| 元规则 | AutoContext 自己 | `meta-rules.md`（M1-M10） | 生成/组合/维护时守，不输出给用户 |
| 操作技巧 | 人（用 agent 时） | `tips.md`（25 条，触发 + 转述） | agent 检测场景后主动转述给人 |

原则：同一条只在一处，维护改一处。给 agent 的不写进元规则，给人的不写进 atom，元规则不渲染给用户。

## 准则原子化设计

准则原子是 Auto Context 的核心素材，不是最终文件。每个准则只表达一条稳定约束，并带有适用条件、输出位置和冲突关系。

### 准则原子结构

```yaml
id: do-not-guess-schema
title: Do not guess schema
profiles:
  - data-analysis
scopes:
  - claude
  - rules
priority: high
triggers:
  files:
    - "*.sql"
    - "dbt_project.yml"
    - "*.ipynb"
  user_intents:
    - data-analysis
conflicts: []
renders:
  claude: |
    - Do not guess schemas when they can be inspected.
    - Confirm join keys and metric definitions before writing final SQL.
  rule: |
    Check table names, column names, aliases, and aggregation grain before finalizing SQL.
```

### 准则原子分类

| 类型 | 解决的问题 | 示例 |
| --- | --- | --- |
| `project-fact` | 项目稳定事实 | 技术栈、目录、入口、命令、数据源 |
| `working-standard` | agent 工作方式 | 小步修改、先读再改、不要覆盖用户工作 |
| `verification` | 如何确认结果 | 运行测试、截图验证、schema 检查、引用核对 |
| `output-format` | 输出长什么样 | 文档结构、SQL 表字段、研究引用格式 |
| `safety` | 不该做什么 | 不运行破坏性命令、不写密钥、不覆盖上下文 |
| `context-quality` | 上下文本身质量 | 小于 200 行、避免 Skill Leakage、避免重复 README |

### 组合流程

```text
workspace signals
  + user intent
  + existing context files
  -> candidate guideline atoms
  -> rank by relevance and priority
  -> remove duplicates
  -> resolve conflicts
  -> choose artifact target
  -> render CLAUDE.md / AGENTS.md / .claude/rules
  -> lint generated context
```

### 组合准则

- Profile 只负责召回候选准则，不直接决定最终文件。
- 用户回答只用于消除歧义，不作为固定模板变量。
- 同一条准则只能在一个最合适的位置出现，避免 `CLAUDE.md`、`AGENTS.md` 和 rules 重复。
- 低置信度时宁可少写，也不要为了完整而填充泛化规则。
- 如果准则是多步骤流程，输出为 skill 建议，不塞进 `CLAUDE.md`。

## 支持场景

MVP 支持 7 个一级 Profile：

| Profile | 适用场景 | 生成重点 |
| --- | --- | --- |
| `coding` | 代码开发、修 bug、重构、测试 | 技术栈、目录、命令、小步修改、测试策略 |
| `frontend-product` | 前端产品、Web app、交互工具 | 用户流、UI 约束、视觉质量、运行验证 |
| `product-design` | 产品定义、PRD、用户旅程、功能设计 | 用户、场景、取舍、体验完整性 |
| `research` | 论文、竞品、技术调研、资料总结 | 来源、证据/推断区分、引用格式 |
| `writing-docs` | 文档、教程、方案、商业材料 | 读者、结构、语气、输出标准 |
| `data-analysis` | SQL、数据分析、指标口径 | 表结构、字段口径、可复用查询、不要猜 schema |
| `creative-media` | 视频、脚本、动画、内容创作 | 风格、节奏、资产、输出格式 |

后续可增加：

- `agent-workflow`
- `business-strategy`
- `education-course`
- `voice-ai-product`
- `mobile-app`
- `infra-ops`

## Auto Context 的输出策略

### 默认文件选择

```text
Claude Code first:
  CLAUDE.md

Cross-agent coding repo:
  AGENTS.md + CLAUDE.md importing AGENTS.md

Large or mixed project:
  CLAUDE.md + .claude/rules/*.md

Personal local preference:
  CLAUDE.local.md

Reusable procedure:
  .claude/skills/<name>/SKILL.md
```

### 推荐规则

- 单一小项目：生成一个 `CLAUDE.md`。
- 代码项目且用户使用多个 agent：生成 `AGENTS.md`，再生成一个 `CLAUDE.md` 引用它。
- 大型项目/monorepo：生成 `.claude/CLAUDE.md` + `.claude/rules/`。
- 空项目：先问问题，再生成 `CLAUDE.md`。
- 已有 `CLAUDE.md`：不覆盖，生成 review 和 patch。
- 已有 `AGENTS.md`：建议 `CLAUDE.md` import `AGENTS.md`，避免重复。

## MVP 交互流程

交互目标不是让用户配置系统，而是在最少问题下补足会影响准则组合的关键信息。默认先扫描，只有检测结果不足以决定准则组合时才问。

### 默认问题策略

最多问 2 个问题，每个问题最多 3 个选项。第一版可以先用粗粒度问题，后续再根据准则原子库反推更精准的问题。

```text
问题 1：你接下来主要想让 agent 做哪类工作？
A. 改项目
B. 理清项目
C. 产出材料

问题 2：你最不想反复解释哪类信息？
A. 项目事实
B. 工作标准
C. 输出格式
```

问题含义：

- `改项目`：偏 coding、frontend-product、data-analysis、creative-media。
- `理清项目`：偏 research、product-design、architecture-review、context-update。
- `产出材料`：偏 writing-docs、product-design、research、creative-media。
- `项目事实`：目标、目录、技术栈、命令、数据表、关键资料。
- `工作标准`：代码规则、产品判断、UI 质量、研究证据、数据口径。
- `输出格式`：文档结构、引用格式、SQL 输出、设计报告口径。

如果扫描信号强，只问问题 2；如果已有上下文文件，先做 review，再问用户最想减少哪类重复说明。

### 已有项目

```text
User: 使用 auto-context 初始化这个项目

1. 扫描高信号文件
   - README*
   - package.json / pyproject.toml / go.mod / Cargo.toml / pom.xml
   - Makefile / justfile / docker-compose.yml
   - src/ app/ docs/ tests/
   - existing CLAUDE.md / AGENTS.md / .cursor/rules / .windsurfrules

2. 输出判断
   - workspace_state
   - detected_profiles
   - confidence
   - evidence

3. 低置信度时最多问 2 个问题
   - 你接下来主要想让 agent 做哪类工作？
   - 你最不想反复解释哪类信息？

4. 组合准则原子
   - project facts
   - working standards
   - verification rules
   - output format rules
   - context-quality rules

5. 生成 proposal
   - files_to_create
   - files_to_update
   - selected_guidelines
   - risk_notes

6. 用户确认后写入
```

### 空项目

```text
User: 初始化一个新项目的上下文

1. 检测为空目录
2. 问最多 2 个问题
   - 你接下来主要想让 agent 做哪类工作？
   - 你最不想反复解释哪类信息？
3. 选择 Profile
4. 组合最少准则原子
5. 生成最小 CLAUDE.md
6. 推荐下一步可选规则或 skills
```

### 项目进行中

```text
User: 这个项目的 CLAUDE.md 好像不太合适，帮我更新

1. 读取现有上下文文件
2. 扫描最近项目结构和关键文件
3. 检测配置质量问题
4. 识别已有准则和缺失准则
5. 给出 review
6. 生成 patch
```

## 检测算法

### 信号模型

```json
{
  "workspace_state": "empty | existing | partial",
  "project_kinds": [
    {
      "profile": "frontend-product",
      "score": 0.82,
      "evidence": ["package.json", "src/App.tsx", "tailwind.config.ts"]
    }
  ],
  "detected_stack": ["typescript", "react", "vite"],
  "context_files": ["CLAUDE.md", "AGENTS.md"],
  "user_intent": "change-project | understand-project | produce-material | unknown",
  "repetition_pain": "project-facts | working-standards | output-format | unknown",
  "candidate_guidelines": ["small-scoped-changes", "verify-rendered-ui"],
  "recommended_outputs": ["CLAUDE.md", ".claude/rules/frontend.md"],
  "questions": []
}
```

### 基础规则

| Signal                                                 | Profile                            |
| ------------------------------------------------------ | ---------------------------------- |
| `package.json` + `app/`/`pages/` + `components/`       | `frontend-product`                 |
| `pyproject.toml` + `src/` + `tests/`                   | `coding`                           |
| `.ipynb` / `*.sql` / `dbt_project.yml`                 | `data-analysis`                    |
| `papers/` / `references/` / many PDFs / Markdown notes | `research`                         |
| `PRD.md` / `docs/` / `requirements/`                   | `product-design` or `writing-docs` |
| `remotion.config.*` / media assets / scripts           | `creative-media`                   |
| empty directory                                        | ask questions                      |

### 置信度

```text
0.80 - 1.00: 直接推荐，允许用户确认
0.50 - 0.79: 推荐 + 问 1-2 个问题
0.00 - 0.49: 进入空项目/不确定项目问答流
```

### 避免误判

- 文件数量很少时，不要过度自信。
- `README` 和依赖文件冲突时，优先问用户项目目标。
- 一个项目可有主 Profile 和次 Profile，但 MVP 最多使用 1 主 + 1 次。
- 不因为有 `docs/` 就判断为写作项目；代码仓库也常有 docs。
- 不因为有 `package.json` 就判断为前端产品；也可能是 CLI、库或脚本。

## 技术实现

### 推荐目录结构

```text
AutoContext/
  auto-context设计文档.md          # 本文档
  guidelines/                      # 准则原子库（46 atom / 94 文件含中文）
    working-standard/              # 12 atom
    verification/                  # 13 atom
    output-format/                 # 7 atom
    safety/                        # 8 atom
  references/                      # 参考素材库
    techniques-overview.md         # 给 agent 的候选素材库
    meta-rules.md                  # AutoContext 元规则
    tips.md                        # 给人的操作技巧
    REVIEW_CRITERIA.md             # 参考样本审核标准
    claude-md-reference/           # 39 份核心样本
    reviewed-out/                  # 淘汰留痕
  SKILL.md                         # （待做）skill 入口
  scripts/                         # （v0.2）检测/组合/渲染脚本
  assets/                          # （v0.2）CLAUDE.md 骨架模板
```

### `SKILL.md` 职责

只写流程：

```md
---
name: auto-context
description: Use this before starting, onboarding, or recalibrating any project. It inspects the workspace or interviews the user, identifies the project scenario, and generates reviewable CLAUDE.md, AGENTS.md, or .claude/rules context files.
---

# Auto Context

1. Run project detection.
2. Classify the project profile.
3. Ask up to 2 questions only when detection cannot decide the guideline set.
4. Compose the smallest useful guideline atom set.
5. Select the smallest context artifact set.
6. Render a proposal with selected guidelines and evidence.
7. Write files only after user confirmation.
8. Never overwrite existing context files without showing a diff.
```

### `detect_project.py`

职责：确定性扫描，输出 JSON。

伪代码：

```python
def detect(root):
    files = scan_high_signal_files(root)
    state = classify_state(files)
    signals = collect_signals(files)
    profile_scores = score_profiles(signals)
    return {
        "workspace_state": state,
        "detected_stack": detect_stack(files),
        "profile_scores": profile_scores,
        "existing_context": find_context_files(files),
        "questions": suggest_questions(profile_scores, state),
    }
```

### `compose_guidelines.py`

职责：根据检测结果和用户回答，从准则原子库中选择、排序、去重，并决定渲染目标。

伪代码：

```python
def compose(detection, answers, atoms):
    candidates = select_by_profile(atoms, detection["profile_scores"])
    candidates += select_by_signals(atoms, detection["signals"])
    candidates += select_by_answers(atoms, answers)
    ranked = rank_by_priority_and_evidence(candidates)
    deduped = remove_duplicates(ranked)
    resolved = resolve_conflicts(deduped)
    return {
        "selected_guidelines": resolved,
        "artifact_targets": choose_targets(resolved, detection),
        "omitted_guidelines": explain_omissions(candidates, resolved),
    }
```

第一版可以由 agent 手动执行这个流程；脚本在 v0.2 后固化。

### `render_context.py`

职责：把检测结果 + 用户回答 + 准则原子渲染为上下文文件。

MVP 不需要复杂模板引擎，Python 标准库字符串替换即可。准则原子本身提供 `renders.claude`、`renders.agents`、`renders.rule` 等片段，渲染器只负责分组、排序和去重。

### `lint_context.py`

职责：检查生成结果是否有上下文质量问题。

第一版规则：

- 文件超过 200 行：提示 Context Bloat。
- 包含大量格式化规则：提示 Lint Leakage。
- 包含多步骤任务流程：提示 Skill Leakage。
- 同时出现相互冲突的强规则：提示 Conflicting Instructions。
- 包含未填占位符：阻止写入。
- 包含密钥/Token 风险词：阻止写入。

## 生成策略

### Existing Project

1. 先抽取事实准则：
   - detected stack
   - important directories
   - commands
   - context files
2. 再组合工作准则：
   - working style
   - output expectations
   - verification rules
3. 最后生成维护准则：
   - when to update this file
   - when to move content to rules/skills

### Empty Project

1. 不伪造技术栈。
2. 不生成 build/test commands。
3. 只写用户已回答的信息。
4. 把未知项标为 `TBD`，但控制数量。
5. 只组合通用准则和用户意图强相关准则。
6. 给出下一步建议，例如“当项目生成代码后重新运行 auto-context”。

### Existing Context File

如果已有 `CLAUDE.md` 或 `AGENTS.md`：

```text
Do:
  - summarize current content
  - detect smells
  - propose minimal patch
  - preserve user-specific wording where useful

Don't:
  - overwrite
  - duplicate AGENTS.md into CLAUDE.md
  - expand a short useful file into a long generic one
```

## 典型输出示例

### 检测报告

```md
## Auto Context Proposal

Detected state: existing project
Primary profile: frontend-product
Secondary profile: coding
Confidence: 0.84

Evidence:
- package.json includes vite, react, typescript
- src/ and components/ exist
- README contains local dev command

Recommended files:
- Create CLAUDE.md
- Create .claude/rules/frontend.md

Selected guidelines:
- detected-stack
- small-scoped-changes
- verify-rendered-ui
- keep-under-200-lines
- avoid-skill-leakage

Reason:
- Project needs both implementation guardrails and UI-quality expectations.
- Frontend-specific rules should be scoped separately to avoid bloating CLAUDE.md.
```

### 写入后的文件

```text
CLAUDE.md
.claude/rules/frontend.md
```

## 用户体验细节

### 默认交互文案

```text
我判断这是一个 [profile] 项目，置信度 [score]。
依据是：[evidence]。

我建议生成：
- [file 1]
- [file 2]

我不会覆盖已有文件。要我继续生成预览吗？
```

### 低置信度问题

最多问 2 个：

1. 你接下来主要想让 agent 做哪类工作？
2. 你最不想反复解释哪类信息？

### 写入确认

```text
我已经生成了预览。确认后我会写入这些文件：
- CLAUDE.md
- .claude/rules/frontend.md

如果你只想要 CLAUDE.md，我可以只写一个文件。
```

## MVP 范围

### 已完成

- 准则原子库：46 个 atom（中英双份），覆盖 7 个 MVP profile + security
- 参考素材库：techniques-overview（候选）、meta-rules（元规则）、tips（给人的技巧）
- 核心样本池：39 份真实 CLAUDE.md / AGENTS.md
- 三类内容分离：给 agent / 给 AutoContext / 给人

### 必做（MVP 剩余）

- `SKILL.md`：AutoContext 的 skill 入口，定义检测→定 profile→召回→组合→渲染流程
- 作为 Agent Skill 可被调用
- 支持空项目问答
- 支持已有项目扫描（agent 手动扫，无脚本）
- 基于 profile 召回 atom（通用 + 对应 profile）
- 组合 atom 渲染 CLAUDE.md
- 不覆盖已有上下文文件
- 输出检测报告、选中的准则和写入理由

### 可选

- 生成 `.claude/rules/`（超 200 行时拆分）
- 生成 `AGENTS.md`
- 已有 `AGENTS.md` 时生成 `CLAUDE.md` import 建议
- 检测 Context Smells

### 暂不做

- GUI
- 长期自动监控
- 自动提交 git
- marketplace
- 多 agent 并行评审
- 复杂模型微调或 embedding 检索
- 检测/组合脚本（v0.2 固化）

## 版本路线

### v0.1：Prompt-only Skill + Guideline Atoms

已完成：
- ✓ 第一批准则原子（46 个，远超预期，覆盖 7 profile + security）
- ✓ 参考素材库（techniques-overview / meta-rules / tips 三文档）
- ✓ 核心样本池（39 份）
- ✓ 三类内容分离设计

待做：
- `SKILL.md`（skill 入口，定义检测→组合→渲染流程）
- profile 选择说明（部分在 techniques-overview）
- 手动扫描 + 生成 proposal（agent 跑流程）
- 无脚本（v0.1 纯 prompt）

目标：一天内可用。当前素材已就绪，写完 `SKILL.md` 即可跑通。

### v0.2：Deterministic Detector + Composer

- 增加 `detect_project.py`
- 增加 `compose_guidelines.py`
- 输出 JSON 检测结果
- 准则组合和模板渲染更稳定

目标：减少 agent 每次重新判断的漂移。

### v0.3：Context Linter

- 增加 `lint_context.py`
- 检测 Context Bloat、Skill Leakage、Lint Leakage、Conflicting Instructions
- 检查准则重复、准则冲突、未解释的高优先级准则遗漏

目标：从模板生成器升级为上下文质量工具。

### v0.4：Update Mode

- 支持项目进行中重扫。
- 对现有 `CLAUDE.md` 生成 patch。
- 识别应该拆到 `.claude/rules/` 或 `.claude/skills/` 的内容。

目标：解决上下文文件长期腐烂。

### v1.0：Cross-agent Context Pack

- 同时支持 `CLAUDE.md`、`AGENTS.md`、Cursor rules、Windsurf rules。
- 可导出 profile pack。
- 可导出 guideline pack。
- 支持团队共享模板。

目标：成为跨 agent 的项目上下文初始化层。

## 成功标准

### 用户价值指标

- 用户不用从零写 `CLAUDE.md`。
- 生成内容能明显减少后续重复提醒。
- 用户能理解为什么推荐这个 Profile。
- 用户能看到哪些准则被选中，以及为什么没选其他准则。
- 生成文件短、准、可维护。

### 工程指标

- `CLAUDE.md` 默认小于 200 行。
- 默认最多问 2 个问题。
- 已有项目扫描不读取大文件全文。
- 已有上下文文件默认不覆盖。
- 检测结果包含证据和置信度。
- proposal 包含 selected_guidelines。

### 质量指标

- 不把一次性任务写进长期上下文。
- 不重复 README 中的大段内容。
- 不把 lint/format 规则写成大段自然语言。
- 不把具体 skill 流程塞进 `CLAUDE.md`。
- 不生成互相冲突的规则。

## 关键风险

### 风险 1：变成模板堆砌器

缓解：所有输出都由准则原子组合产生，并经过 profile selection、guideline composition 和 context lint。没有检测依据，不填项目事实。

### 风险 2：生成过长

缓解：默认限制 200 行，超出时拆到 `.claude/rules/` 或提示不要写入。

### 风险 3：误判项目类型

缓解：置信度低就问问题；永远显示 evidence；允许用户改主 Profile。

### 风险 4：覆盖用户已有上下文

缓解：默认只生成 proposal；写入前必须确认；已有文件走 patch。

### 风险 5：Profile 和 Skill 混淆

缓解：文档和生成逻辑中固定区分产物层和召回维度：

```text
召回维度（不渲染给 agent）：
Profile = 场景分类，用来从 atom 库召回候选准则

产物层（渲染给 agent）：
Guideline = 稳定上下文准则（进 CLAUDE.md / .claude/rules/）
Skill = 多步流程（进 .claude/skills/，不进 CLAUDE.md）
Rule = 路径/文件约束（进 .claude/rules/）
CLAUDE.md = 稳定项目事实
```

Profile 是召回手段，不是产物。不要把 Profile 和 CLAUDE.md/Skill 当成并列的层。

### 风险 6：准则原子过碎导致组合不可控

缓解：准则原子必须有明确触发条件、优先级、冲突关系和渲染目标。MVP 先维护少量高价值准则，不追求覆盖所有场景。

## 当前进展与下一步

### 已完成（v0.1）

**准则原子库（guidelines/）**
- 46 个 atom（中英双份，共 94 文件），分布在 working-standard / verification / output-format / safety 四个目录
- 通用 atom 22 条（profiles: [all]），profile 级 24 条（coding 6、security 5、research 4、writing-docs 3、frontend-product 2、data-analysis 2、product-design 1、creative-media 1）
- 每个 atom 卡帕西式正文（加粗核心句 + 展开 + 验收），frontmatter 含 name + description（Use when...）+ profiles + scopes + priority + triggers + conflicts

**参考素材库（references/）**
- `techniques-overview.md`：给 agent 的候选素材库（49 条 + 反例 + 不收），S 级 7 条已抽成正式 atom
- `meta-rules.md`：AutoContext 元规则（M1-M10），不输出给用户
- `tips.md`：给人的操作技巧（25 条，触发 + 转述）
- `claude-md-reference/`：39 份核心样本（universal 5 + 12 场景，中英双份）

### 下一步

写 `SKILL.md`（AutoContext 的 skill 入口），定义检测→定 profile→召回→组合→渲染→lint 的流程。第一版不写检测脚本，让 agent 根据 skill 流程手动扫描项目、组合 atom、生成 proposal。等真实使用几次后，再把重复判断固化成 `detect_project.py` 和 `compose_guidelines.py`。

目标：写完 `SKILL.md` 即可在真实项目上跑通"生成 CLAUDE.md"，验证用户是否愿意在开工前运行一次 Auto Context。

---

## 附录:好的 CLAUDE.md 模式收集

### 通用 Project CLAUDE.md

适合任何项目，尤其是空项目或不确定项目：

```md
# Project Context

## Goal
- [What this project is trying to accomplish]

## Working Style
- Start by reading existing context before acting.
- Prefer small, reversible changes.
- Ask only when missing information blocks progress.
- Do not overwrite user work.

## Project Facts
- Main audience: [detected/asked]
- Current stage: [idea/prototype/building/maintenance]
- Important files: [detected]

## Output Expectations
- Default language: [asked/detected]
- Preferred format: [concise explanation / design doc / implementation diff]
```

特点：只放稳定背景，不放具体任务步骤。

### 代码项目 CLAUDE.md

```md
# Project Instructions

## Project Overview
- Stack: [detected stack]
- Main entry points: [detected files]
- Important directories: [detected directories]

## Commands
- Install: `[detected]`
- Run: `[detected]`
- Test: `[detected]`
- Lint/typecheck: `[detected]`

## Coding Rules
- Read relevant files before editing.
- Follow existing patterns and naming.
- Prefer small scoped changes.
- Avoid unrelated refactors.
- Preserve public behavior unless the task asks otherwise.

## Verification
- Run the smallest relevant test first.
- If tests cannot run, explain why and what was checked instead.

## Safety
- Do not run destructive git commands unless explicitly requested.
- Do not modify generated files unless the generator is part of the change.
```

适合来源：Claude `/init`、AGENTS.md、公开 coding manifest 实践。

### 前端产品项目 CLAUDE.md

```md
# Frontend Product Context

## Product Surface
- Target user: [asked/detected]
- Core workflow: [asked/detected]
- Primary screen: [detected/asked]

## UX Guidelines
- Build the usable experience first, not a marketing placeholder.
- Prioritize complete workflows over isolated components.
- Keep controls familiar and predictable.
- Verify responsive layout on desktop and mobile.

## Engineering Rules
- Follow the existing component and styling system.
- Use real assets or generated bitmap assets when visual inspection matters.
- Avoid decorative UI that does not support the task.

## Verification
- Start the app when needed.
- Check the rendered UI, not only the code.
```

适合：Web app、dashboard、工具型产品、landing page 以外的真实交互页面。

### 产品设计项目 CLAUDE.md

```md
# Product Design Context

## Product Frame
- Target user: [asked]
- Job to be done: [asked]
- Current stage: [idea/spec/prototype/iteration]

## Working Style
- Give a stance first.
- Make tradeoffs explicit.
- Prefer concrete user flows over abstract feature lists.
- Separate user-visible experience from backend/protocol details.
- Do not overbuild early concepts.

## Output Standards
- Use crisp product language.
- Avoid repeated scenario templates.
- Keep docs shippable, not scratchpad-like.
```

适合：PRD、产品方向判断、交互方案、用户旅程。

### 研究/论文项目 CLAUDE.md

```md
# Research Context

## Research Goal
- Topic: [asked/detected]
- Desired depth: [quick scan / deep read / literature review]
- Output: [notes / summary / comparison / implementation plan]

## Research Rules
- Separate evidence from inference.
- Preserve important technical terms.
- Prefer primary sources when accuracy matters.
- Include citations or source links for external claims.
- Mark uncertainty explicitly.

## Output Style
- Start with the high-level answer.
- Then provide structured findings.
- End with open questions or next reading steps when useful.
```

适合：论文阅读、技术调研、竞品研究。

### 文档写作项目 CLAUDE.md

```md
# Writing Context

## Audience
- Reader: [asked]
- Purpose: [inform / persuade / teach / align]
- Tone: [asked]

## Writing Rules
- Outline before drafting when structure is unclear.
- Write final prose, not process notes.
- Prefer concrete claims and examples.
- Remove repeated sections and template filler.
- Keep terminology consistent.

## Output Standards
- Use headings only when they help scanning.
- Keep the first version usable.
```

适合：方案、教程、商业文档、内部说明、README。

### 数据分析项目 CLAUDE.md

```md
# Data Analysis Context

## Data Goal
- Business question: [asked]
- Key entities: [asked/detected]
- Expected output: [SQL / table / chart / explanation]

## Data Rules
- Do not guess schema when it can be inspected.
- Confirm join keys and metric definitions.
- Keep outputs minimal and aligned with the request.
- Prefer reusable SQL over one-off fragments.
- Call out assumptions and data quality risks.

## Verification
- Check column names, aliases, and aggregation grain.
- Explain mismatches in plain language.
```

适合：SQL、指标分析、特征工程、数据口径梳理。

### 创意媒体项目 CLAUDE.md

```md
# Creative Media Context

## Creative Brief
- Format: [video / animation / script / image / presentation]
- Audience: [asked]
- Style references: [asked]
- Deliverable: [asked]

## Creative Rules
- Preserve the intended mood and pacing.
- Offer a strong first direction before variants.
- Use concrete visual/audio references.
- Do not force engineering constraints into early ideation.

## Production Rules
- Track source assets and output paths.
- Verify rendered artifacts when possible.
```

适合：短视频、动画、脚本、视觉稿、演示型 HTML。

