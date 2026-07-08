---
name: preserve-existing-behavior
description: 在改有现有用户、调用方或契约的代码时使用。防止伪装成清理或设计品味的回归。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 保持现有行为

**不要破坏 userspace。现有行为胜过理论上的整洁。**

- 不要因为新设计感觉更干净就引入回归。
- 二进制兼容、公共 API 和已建立的工作流不是可选项。
- "用户应该自己改"不是论据,是承认失败。
- 如果改动必须破坏行为,先获得明确确认,并说明代价。

**准则生效的标志:** 没有现有测试、调用方或用户工作流在未经用户明确同意的情况下被破坏。
