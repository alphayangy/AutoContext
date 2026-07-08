---
name: goal-driven-execution
description: 在多步骤或含糊的任务上使用。防止"让它跑起来"式的弱成功标准导致不断澄清和无限循环。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 目标驱动执行

**定义成功标准。循环验证直到通过。**

把任务转化为可验证目标:
- "添加验证" → 为无效输入写测试,然后让测试通过。
- "修复 bug" → 写一个能复现它的测试,然后让它通过。
- "重构 X" → 确保重构前后测试都通过。

多步骤任务,给出简短计划:
1. [步骤] → 验证:[检查]
2. [步骤] → 验证:[检查]

强成功标准让你能独立循环。弱标准需要不断澄清。

**准则生效的标志:** agent 朝定义的终点循环,验证通过就停,而不是反复问"这样行吗"。
