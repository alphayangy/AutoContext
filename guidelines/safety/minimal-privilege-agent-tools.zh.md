---
name: minimal-privilege-agent-tools
description: 在设计 agent 或工具调用系统时使用。防止过度授权的 agent 在未经审批的情况下跑破坏性操作。用于 security 场景。
profiles: [security]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# agent 最小权限

**给 agent 能完成工作的最小工具集。不多给。**

- 从只读工具开始。只在任务需要时加写或执行工具。
- 用短期、限定范围的令牌。不用长期宽凭证。
- 破坏性操作在执行前需要人工审批,不是事后。
- 记录每次工具调用的参数和结果。
- 撤销 agent 在会话中不再需要的工具。

**准则生效的标志:** 没有 agent 持有超出当前任务所需的工具或凭证,没有破坏性操作在未经明确审批的情况下运行。
