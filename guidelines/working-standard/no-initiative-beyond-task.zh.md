---
name: no-initiative-beyond-task
description: 在每个任务上使用。防止范围蔓延、未被要求的文档或 README、以及"顺手"重构导致 diff 膨胀。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# 不超出任务主动加戏

**按要求做。不多不少。**

- 不创建文档、README 或示例,除非明确要求。
- 不"顺手"加功能。
- 不修复无关问题。单独记录它们。
- 不重构任务没碰到的代码。

用户要 X,就交付 X。提及相邻问题,但不要修。

**准则生效的标志:** diff 只包含任务所需内容,相邻问题被报告而不是被默默修掉。
