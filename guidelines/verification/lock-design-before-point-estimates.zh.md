---
name: lock-design-before-point-estimates
description: 在解读实验或统计结果时使用。防止"先看到数字再把设计掰弯去迎合"的确认偏误。用于 research 场景。
profiles: [research]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [understand-project, produce-material]
conflicts: []
---

# 看点估计前先锁研究设计

**在看数字之前,先把研究设计定死。**

读点估计或最终结果之前:
- 锁研究设计:变量、样本、方法、预注册决定。
- 锁分析计划:什么算答案,什么不算。
- 然后才看点估计。

如果设计在看到数字后变了,结果就不再是同一个声明。说明这一点。

**准则生效的标志:** 没有任何分析计划在结果已知后改变,任何事后调整都被标注为事后。
