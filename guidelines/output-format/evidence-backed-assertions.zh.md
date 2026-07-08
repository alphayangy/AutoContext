---
name: evidence-backed-assertions
description: 在散文里做事实声明时使用。防止把编造的引语、统计和归属当事实陈述。用于 writing-docs 场景。
profiles: [writing-docs]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [produce-material]
conflicts: []
---

# 事实声明要有证据支撑

**每个事实声明都需要可验证的来源。查不到就删或标注。**

- 事实声明必须指向一个能被检查的来源。
- 引语必须逐字准确且归属正确。
- 统计必须追溯到真实数据集或研究。
- 如果声明无法验证,标 `[UNVERIFIED]` 或删掉。
- 永远不要凭记忆生成引语、归属或统计。

编造的引语有诽谤风险。编造的统计是错误信息。两者都比留个空缺更糟。

**准则生效的标志:** 输出里每一个事实声明要么有可验证来源支撑,要么被明确标为未验证。
