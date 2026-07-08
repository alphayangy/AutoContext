---
name: prefer-canonical-examples-over-rule-lists
description: 在给 agent 写指令、规则或指导时使用。防止冗长且脆弱的 edge-case 规则清单,改用少量多样的典型示例。适用于所有 profile。
profiles: [all]
scopes: [claude, rules]
priority: medium
triggers: []
conflicts: []
---

# 示例优于规则清单

**几个好示例比一长串 edge-case 规则教得更多。**

写指导时:
- 先放 2-3 个多样的典型示例,覆盖意图。
- 不要把每个 edge case 都列成规则。清单会变长、变脆,还是会漏。
- 示例值千言规则。它们隐式展示模式。
- 用规则去界定示例,不是替换示例。

**准则生效的标志:** 指导更短更清晰,agent 从示例正确泛化,而不是在做规则文本的字符串匹配。
