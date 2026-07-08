---
name: bounded-consumption
description: 在构建服务用户或 agent、可能面对无界请求的系统时使用。防止失控循环、滥用或无限重试导致的资源耗尽。用于 security 场景。
profiles: [security]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 有界消耗

**每个用户、会话和 agent 都有预算。强制执行。**

- 按用户限速请求。
- 按用户给 LLM 调用设 token 和成本预算。
- 长操作设硬超时。不允许无界循环。
- 重试预算:限制尝试次数和总重试时间。遵守 `Retry-After`。
- 依赖持续失败时用熔断。

**准则生效的标志:** 没有用户或 agent 能消耗无界资源,失控循环撞到硬停止而不是永远跑。
