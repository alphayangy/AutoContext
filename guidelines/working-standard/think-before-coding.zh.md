---
name: think-before-coding
description: 在实现任何非简单改动前使用。防止假设式编码、隐藏困惑、在多种理解之间默默选择。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, understand-project]
conflicts: []
---

# 编码前先思考

**不要假设。不要隐藏困惑。揭示权衡。**

实现之前:
- 明确陈述你的假设。不确定就问。
- 如果存在多种理解,列出来。不要默默选择。
- 如果有更简单的方案,说出来。必要时提出异议。
- 如果有不清楚的地方,停下来。指出困惑之处。问。

**准则生效的标志:** 澄清问题出现在实施之前,而不是出错之后。
