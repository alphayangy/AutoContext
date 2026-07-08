---
name: positive-instruction-framing
description: 在给 agent 写指令或规则时使用。防止对禁令的模糊遵守,改为陈述要做什么,不说不要做什么。适用于所有 profile。
profiles: [all]
scopes: [claude, rules]
priority: medium
triggers: []
conflicts: []
---

# 正向表述

**说要做什么。不说不要做什么。**

- "不要用 markdown"不如"写流畅的散文段落"。
- 禁令告诉 agent 要避免什么,但期望行为没定义。agent 可能字面上遵守却错过意图。
- 把禁令改写成正向期望:陈述你要的具体行为。
- 有些硬限制仍需"never"(安全)。但输出和风格,优先正向表述。

**准则生效的标志:** 指令描述目标行为,agent 不用猜"不做 X"实际该怎么做。
