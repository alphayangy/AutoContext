---
name: calibrate-assertion-to-evidence
description: 在散文里做声明时使用。防止"这证明了"式的过度断言和"可能或许大概"式的反射性模糊,让动词强度匹配证据。用于 writing-docs 场景。
profiles: [writing-docs]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [produce-material]
conflicts: []
---

# 断言要匹配证据强度

**动词匹配证据。不过断言。不反射性模糊。**

强度阶梯,从弱到强:
- suggest(弱证据,单次观察)
- show(一致模式,多个案例)
- prove(形式化,穷尽)

- 只有一个数据点时用"suggest"。
- 模式跨多个案例成立时用"show"。
- 只有形式化或穷尽证据时才用"prove"。
- 不要用"可能或许大概"去模糊一个你其实有证据的声明。陈述声明和证据。

**准则生效的标志:** 声明动词匹配其证据强度,没有过度断言也没有反射性模糊。
