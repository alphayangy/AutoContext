# AID - AI 开发方法论

## ⚠️ 基础层：WHY 优先思维

> "人们购买的不是你做什么，而是你为什么要做。" — Simon Sinek

**在发出任何命令、进入任何阶段、采取任何行动之前——先理解 WHY。**

### 提示词分析协议（始终优先运行）

```
┌─────────────────────────────────────────────────────────────┐
│  每个提示词 → WHY 分析 → 阶段检查 → 然后继续                │
└─────────────────────────────────────────────────────────────┘
```

1. **提取明确的 WHY** — 用户陈述的目标是什么？
2. **推断隐含的 WHY** — 他们可能没有表达出来的潜在需求是什么？
3. **验证或询问** — WHY 是否足够清晰？如果不够，在继续之前先询问。
4. **锚定到 WHY** — 每个输出都必须追溯到已确定的 WHY。

### 黄金法则（始终遵守）

| 法则 | 描述 |
|------|-------------|
| 行动前先问 WHY | 即使是简单的请求也有潜在的动机 |
| 用 5 个为什么深入挖掘 | 第一个答案很少是根本原因 |
| 明确陈述 WHY | 让所有输出中的动机清晰可见 |
| 验证理解 | 在继续之前反馈 WHY |
| 连接到目的 | 每个选择都追溯到 WHY |

### 铁律（绝不违反）

| 法则 | 描述 |
|------|-------------|
| 无目的不实现 | "直接做" 是不可接受的 |
| 不理解不复制 | "竞争对手有" 需要 WHY 验证 |
| 评审中绝不跳过 WHY | 每个 PR 都要展示意图，而不仅是变更 |
| 不让紧迫绕过目的 | "很急" 更需要 WHY，而不是更少 |
| 不假设共识 | 隐含的 WHY 会导致不一致 |

### 3 秒 WHY 检查

在任何行动之前：

| ✓ | 问题 |
|---|----------|
| □ | 我为什么要做这件事？ |
| □ | 它创造了什么价值？ |
| □ | 谁受益？ |

3 秒内无法回答 → **停下来澄清。**

### 危险信号 — 停下来询问

| 信号 | 询问 |
|--------|-----|
| "直接做" | "这解决了什么问题？" |
| "大家都想要" | "具体为什么？" |
| "竞争对手有" | "我们的目的是否需要它？" |
| "很急" | "不做的代价是什么？" |
| "让它更好" | "这里的'更好'是什么意思？" |
| "相信我" | "帮我理解一下 reasoning" |

---

## ⚠️ 关键：阶段门控执行

在 WHY 确定后，Claude 必须：
1. 读取 `.aid/state.json` 以确定当前阶段
2. 读取 `.aid/context.json` 以了解当前任务/步骤
3. 验证请求的工作在当前阶段是否被允许
4. **拒绝属于后续阶段的工作**

### 6 阶段生命周期

```
Phase 0 ──► Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──► Phase 5
Discovery     PRD      Tech Spec   Impl Plan     Dev       QA & Ship
```

### 各阶段核心 WHY 问题

| 阶段 | 核心 WHY 问题 |
|-------|-------------------|
| 0 Discovery | "WHY 这个问题值得解决？" |
| 1 PRD | "WHY 用户需要这个？" |
| 2 Tech Spec | "WHY 选择这个架构？" |
| 3a Consolidation | "WHY 存在这个矛盾？WHY 这样解决？" |
| 3b Breakdown | "WHY 这个任务大小？WHY 这些依赖？" |
| 3c Jira Population | "WHY 这些信息是完整的？WHY 仅凭这个开发就能开工？" |
| 4 Development | "WHY 这段代码？WHY 这些连接？" |
| 5 QA & Ship | "WHY 这个测试？WHY 可以发布了？" |

### 阶段权限

| 阶段 | 允许 | 禁止 |
|-------|---------|---------|
| 0 Discovery | 研究、利益相关者、竞品分析 | PRD、架构、代码 |
| 1 PRD | + 需求、范围、用户故事 | 架构、代码、Jira |
| 2 Tech Spec | + 架构、schema、API | 代码、Jira issue |
| 3a Consolidation | + 矛盾解决、整合规范 | Jira issue、代码 |
| 3b Breakdown | + 任务分解、Sprint 规划 | Jira 创建、代码 |
| 3c Jira Population | + Jira epic、story、task（信息完整） | 生产代码 |
| 4 Development | + 代码、测试、组件 | 部署 |
| 5 QA & Ship | 一切 | - |

---

## 🔍 透明质量检查（自动）

每个重要输出在展示给用户之前都必须经过自我反思。
质量检查框始终显示，以建立信任并确保质量一致。

### 核心流程

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Prompt    │ ───► │   Draft     │ ───► │  Reflect    │ ───► │   Output    │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
                      (internal)          (score & revise)    (with QC box)
```

### 何时应用

| 应用质量检查 | 跳过质量检查 |
|---------------------|-------------------|
| ✅ 代码生成 | ❌ 简单问题 |
| ✅ 架构决策 | ❌ 状态检查 |
| ✅ PRD/需求 | ❌ 文件读取 |
| ✅ 技术规范 | ❌ 澄清问题 |
| ✅ 测试编写 | ❌ 命令帮助 |

### 质量检查显示格式

**在重要输出之前始终显示此框：**

```
╭─────────────────────────────────────────────────────────────╮
│ 🔍 Quality Check                                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [✅|⚠️|❌] WHY Alignment     X/10   [brief note]           │
│  [✅|⚠️|❌] Phase Compliance  X/10   [brief note]           │
│  [✅|⚠️|❌] Correctness       X/10   [brief note]           │
│  [✅|⚠️|❌] Security          X/10   [brief note]           │
│  [✅|⚠️|❌] Completeness      X/10   [brief note]           │
│                                                             │
│  ══════════════════════════════════════════════════════    │
│  📊 Overall: X.X/10                                         │
│  [STATUS: ✅ PASSED | 🔄 PASSED after N revision(s) | ⚠️]   │
│                                                             │
│  [If revised: 📝 Improvements made: ...]                    │
│                                                             │
╰─────────────────────────────────────────────────────────────╯
```

### 分数图标

| 分数 | 图标 | 操作 |
|-------|------|--------|
| 8-10 | ✅ | 优秀 - 展示输出 |
| 6-7.9 | ⚠️ | 可接受 - 附带说明展示 |
| 0-5.9 | ❌ | 内部修订（最多 3 次） |

### 评判标准（权重）

1. **WHY Alignment (3)** - 输出是否服务于用户的真实需求？
2. **Phase Compliance (2)** - 是否适合当前阶段？
3. **Correctness (3)** - 是否准确、可运行、无错误？
4. **Security (2)** - 是否存在漏洞或泄露的 secret？
5. **Completeness (2)** - 是否解决了所有需求？

### 修订显示

当分数因修订而提高时，显示：
```
│  ⚠️  Security         5→8/10 Fixed: Added input validation  │
```

### 质量命令

| 命令 | 用途 |
|---------|---------|
| `/reflect` | 展示上次质量检查的详细分解 |
| `/reflect --history` | 展示本次会话的所有质量检查 |
| `/reflect --strict` | 以阈值 8 重新评估 |
| `/reflect --explain <criterion>` | 深入分析特定评分项 |

### 各阶段详细标准

各阶段的详细标准位于：
`.claude/skills/reflection/criteria/phase-{N}-{name}.yaml`

---

## 代码生成标准（阶段 4+）

### 每个函数必须包含 WHY：

```python
# ─────────────────────────────────────────────────
# WHY: [该函数解决的问题]
# WHAT: [它做什么]
# CONNECTION: [谁调用它，它调用谁]
# ─────────────────────────────────────────────────
def function_name(params):
    """
    简要描述。
    
    WHY param_x: [为什么需要这个参数]
    WHY return_type: [为什么调用者需要这个返回值]
    """
```

### 每个组件必须记录连接关系：

```python
"""
ComponentName

WHY THIS EXISTS:
[核心目的和它解决的问题]

CONNECTIONS:
- CALLED BY: [列出调用方及 WHY 调用]
- CALLS: [列出依赖及 WHY 需要它们]

DESIGN DECISIONS:
- WHY [decision]: [reasoning]
"""
```

### 组件关系模式：

```
┌─────────────────┐     WHY: Decouple UI from data fetching
│   UserProfile   │────────────────────────────────────────┐
└────────┬────────┘                                        │
         │ WHY: Single source of truth for user state      │
         ▼                                                 │
┌─────────────────┐     WHY: Cache reduces API calls       │
│   UserStore     │◄───────────────────────────────────────┤
└────────┬────────┘                                        │
         │ WHY: Normalize data once at entry point         │
         ▼                                                 │
┌─────────────────┐     WHY: Abstract API versioning
│   UserAPI       │
└─────────────────┘
```

---

## 测试标准（阶段 4-5）— BDD/TDD 集成

### 每个测试必须说明 WHY：

```python
def test_specific_behavior():
    """
    WHY THIS TEST:
    - PROBLEM: [防止什么失败]
    - COST OF FAILURE: [业务/用户影响]
    - SUCCESS: [通过意味着什么]
    """
```

### BDD - 带 WHY 的 Gherkin：

```gherkin
Feature: Feature Name
  """
  WHY: [业务价值和用户需求]
  IMPACT: [如果失败会怎样]
  """
  
  Scenario: Scenario Name
    """
    WHY: [为什么这个具体场景重要]
    """
    Given [context]
    When [action]
    Then [outcome]
```

### 按 WHY（失败代价）组织测试：

```
tests/
├── critical_failures/      # 高代价 - 优先测试
├── user_experience/        # 中等代价
└── edge_cases/            # 低频率
```

---

## 命令

### 首次设置 🆕
| 命令 | 用途 |
|---------|---------|
| `/setup` | **完整引导设置** - 逐步完成整个安装 |
| `/link-project` | **链接现有项目** - 通过符号链接将项目文件夹连接到 AID |

### 日常工作流 ⭐
| 命令 | 用途 |
|---------|---------|
| `/good-morning` | 早晨启动 - 检查系统、加载上下文、继续工作 |
| `/context` | 展示当前工作上下文（任务 + 步骤） |
| `/context-update` | 手动更新上下文 |
| `/reflect` | 展示上次质量检查的详细分解 |

### 测试
| 命令 | 用途 |
|---------|---------|
| `/aid-test` | 运行完整 AID 测试（阶段 0-4）并带 QA 验证 |
| `/aid-test --phase 0` | 仅测试阶段 0 |
| `/aid-test --quick` | 简略测试（每个阶段 1 个输出） |
| `/aid-test --verbose` | 展示所有反思细节 |
| `/test-reflection` | 测试 reflection-agent 隔离与评分 |
| `/test-qa-validator` | 测试 QA validator 标准检查 |
| `/test-phase-review` | 测试阶段门验证 |
| `/test-all-agents` | 按顺序运行所有 agent 测试 |

### 阶段管理 ⭐
| 命令 | 用途 |
|---------|---------|
| `/aid-init` | 使用 AID 阶段初始化项目 |
| `/aid-start` | 开始工作会话 - 先选择角色 → 再用角色特定术语选择阶段 |
| `/aid-status` | 展示当前状态（阶段 + 会话） |
| `/aid-end` | 结束阶段并提供反馈 |
| `/discovery` | **启动阶段 0** - 研究与验证 |
| `/phase` | 展示当前阶段状态 |
| `/gate-check` | 检查是否准备好推进 |
| `/phase-approve` | 人工签核当前阶段 |
| `/phase-advance` | 进入下一阶段 |

### 开发命令
| 命令 | Skill | 用途 |
|---------|-------|---------|
| `/design-system` | atomic-design | 从 Figma 构建设计系统 |
| `/build-page` | atomic-page-builder | 用组件组合页面 |
| `/architecture` | system-architect | 系统架构设计 |
| `/code-review` | code-review | 代码质量评审 |
| `/write-tests` | test-driven | TDD 测试编写 |
| `/test-review` | test-driven | 测试质量评审 |
| `/qa-ship` | aid-qa-ship | QA 验证与发布 |
| `/prd` | - | 从需求创建 PRD |
| `/tech-spec` | - | 创建技术规范 |
| `/jira-breakdown` | - | 将规范拆分为 Jira issue |
| `/start-project` | - | 初始化新项目 |

---

## 上下文跟踪

Claude 必须在以下情况下更新 `.aid/context.json`：
- 开始新任务
- 完成步骤
- 取得重大进展
- 会话结束

---

## 按阶段加载 Skill

| 阶段 | 加载这些 Skill |
|-------|-------------------|
| ALL | `skills/why-driven-decision/` **（基础 - 优先加载）** |
| ALL | `skills/reflection/` **（质量检查 - 始终激活）** |
| 0 | `skills/pre-prd-research/`, `skills/aid-discovery/`, `skills/nano-banana-visual/` |
| 1 | `skills/aid-prd/` |
| 2 | `skills/system-architect/`, `skills/aid-tech-spec/` |
| 3 | `skills/aid-impl-plan/` **（Consolidation → Breakdown → Jira）** |
| 4 | `skills/atomic-design/`, `skills/atomic-page-builder/` |
| 4-5 | `skills/code-review/`, `skills/test-driven/` |
| All | `skills/phase-enforcement/`, `skills/context-tracking/` |

---

## Agents（子代理）

子代理被派生来执行隔离的、专门的任务。它们不接收任何对话上下文。

| Agent | 用途 | 触发方式 |
|-------|---------|--------------|
| **aid-test-agent** | 验证 AID 方法论实现 | `/aid-test` 命令 |
| **reflection-agent** | 所有输出的质量评估 | 自动（质量检查） |
| **qa-validator-agent** | 任务完成验证 | QA gate hook（阶段 4） |
| **phase-review-agent** | 阶段门验证 | `/gate-check` 命令 |

**位置：** `.claude/agents/`（单一事实来源）

**文档：** `.claude/agents/AGENT-STANDARD.md`

---

## 关键文件

```
# State & Context
.aid/state.json      - Phase state (starts at Phase 0: Discovery)
.aid/context.json    - Work context (current task, step, progress)
.aid/qa/             - QA criteria files for task validation

# Phase Outputs
docs/research/       - Phase 0 outputs (research-report.md, traceability-matrix.md)
docs/prd/            - Phase 1 outputs (Product requirements)
docs/tech-spec/      - Phase 2 outputs (Technical specification)
docs/implementation-plan/ - Phase 3 outputs (Task breakdown)

# Skills & Agents (all in .claude/)
.claude/skills/      - All skill definitions
.claude/agents/      - All sub-agent definitions
.claude/commands/    - Slash commands
.claude/hooks/       - QA gate enforcement (Phase 4 only)
.claude/templates/   - State file templates

# Test Outputs (gitignored)
.aid/test-outputs/   - AID methodology test outputs (from /aid-test)
.aid/agent-tests/    - Individual agent test outputs (from /test-* commands)
```

---

## 快速开始

### 非技术用户（推荐）
```
只需在此文件夹中打开 Claude Code 并输入：
/setup
```
这会逐步引导你完成所有设置。

### 技术用户
```bash
# 运行安装脚本
./install.sh

# 将项目链接到 AID
./link-project.sh /path/to/your-project

# 在你的项目中，每天早晨
/good-morning

# 或手动初始化阶段
/aid-init
```

---

## 文档

- Phase system: `docs/PHASE-GATES.md`
- Context tracking: `docs/WORK-CONTEXT-TRACKER.md`
- Daily workflow: `docs/MORNING-STARTUP.md`
- Components: `skills/atomic-design/references/`
- Testing: `skills/test-driven/references/`
- **WHY Framework: `skills/why-driven-decision/`**

---

## 记忆与学习系统

AID 包含一个学习系统，可随着时间提升 Claude 的辅助能力。

### 学习模式命令

| 命令 | 描述 |
|---------|---------|
| `/aid-improve` | 运行学习周期（每周） |
| `/aid-memory` | 管理 Claude Memory 条目 |
| `/aid-reset` | 重置记忆系统 |
| `/aid-analyze` | 完整质量分析与指标和模式 |
| `/aid-dashboard` | 生成质量仪表板报告 |
| `/aid-recommendations` | 查看/管理 skill 更新建议 |

### 会话流程

1. **Init**：`/aid-init` → 创建项目状态文件
2. **Start**：`/aid-start` → **先选择角色** → 然后用角色特定术语选择阶段 → 加载 skill
3. **WHY Check**：在开工前，自动建立 WHY
4. **Work**：Claude 自动应用已加载的 skill
5. **End**：`/aid-end` → 评分会话（1-5）→ 描述哪些有效/无效
6. **Learn**：`/aid-improve` → 分析反馈 → 更新 skill

### 基于角色的阶段术语

阶段使用**角色特定语言**展示，让每个角色看到熟悉的术语：

| Phase | PM | Tech Lead | Developer | QA |
|-------|-----|-----------|-----------|-----|
| 0 | Market & Competitive Research | Technology & Architecture Research | Technical Spike & Research | Test Strategy Research |
| 1 | Product Requirements (PRD) | Technical Requirements Report | Feature Specification | Test Requirements & Coverage Plan |
| 2 | Solution Review | System Architecture Design | Technical Design | Test Architecture & Framework |
| 3 | Roadmap & Prioritization | Sprint Planning & Task Breakdown | Task Breakdown & Estimation | Test Plan & Case Design |
| 4 | Feature Validation & UAT | Code Review & Architecture Oversight | Implementation & Coding | Test Execution & Automation |
| 5 | Launch & Go-to-Market | Release Engineering & Deployment | Bug Fixes & Polish | Release Certification & Sign-off |

术语映射定义于：`.claude/references/role-phase-terminology.json`

### Skill 与 Agent 位置

**所有内容都在 `.claude/` 中**（单一事实来源）：
- `.claude/skills/` - 所有 skill 定义和提示词
- `.claude/agents/` - 所有子代理定义
- `.claude/commands/` - Slash 命令
- `.claude/references/` - 参考文档
- `.claude/templates/` - 状态文件模板

**基础 Skill：**
- `.claude/skills/why-driven-decision/` - **基础 WHY skill（优先加载）**
- `.claude/skills/reflection/` - 质量检查系统

Claude 根据角色和阶段从 `.claude/skills/` 加载 skill，从 `.claude/agents/` 加载 agent。

### 运行时状态

- 项目状态：`.aid/state.json`（阶段跟踪）
- 工作上下文：`.aid/context.json`（当前任务/步骤）
- 会话状态：`~/.aid/state.json`（角色、会话信息）
- 反馈：`~/.aid/feedback/pending/`

---

## 附录：5 Whys 技巧

当 WHY 不清晰时，深入挖掘：

```
Statement: "We need a dashboard"
  Why? → "To see metrics"
  Why? → "To track performance"
  Why? → "To make better decisions"
  Why? → "Because they're overwhelmed by data"
  ROOT WHY: Reduce overwhelm, create clarity

→ The real solution may not be a dashboard at all.
```

---

## 附录：WHY 陈述模板

在发现阶段后，清晰地表达：

```
We believe that [CORE BELIEF].
Therefore, we [HOW WE ACT ON IT].
Which results in [WHAT WE CREATE].
```

**AID 的 WHY：**
```
We believe that great software comes from understanding purpose before writing code.
Therefore, we enforce phase gates and WHY analysis at every step.
Which results in products that solve real problems, not just implement features.
```
