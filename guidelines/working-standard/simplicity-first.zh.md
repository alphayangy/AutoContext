---
name: simplicity-first
description: 在编写或审查代码时使用。防止推测性抽象、未被要求的灵活性、以及资深工程师会拒绝的过度复杂。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# 简洁优先

**用最少代码解决问题。不做推测性设计。**

- 不添加超出需求的功能。
- 不为一次性代码创建抽象。
- 不添加未被要求的"灵活性"或"可配置性"。
- 不对不可能发生的场景写错误处理。
- 如果你写了 200 行而其实 50 行就够,重写。

问自己:"资深工程师会说这过度复杂吗?" 如果是,简化。

**准则生效的标志:** 因过度复杂导致的重写更少,diff 只包含任务所需的内容。
