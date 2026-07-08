---
name: concrete-over-abstract
description: 在生成散文时使用。防止"factors""aspects""issues"这类抽象类别词填充篇幅却什么都没说。用于 writing-docs 场景。
profiles: [writing-docs]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [produce-material]
conflicts: []
---

# 具体优于抽象

**用具体名词。每个短语背后要能指出一个数字、文件或机制。**

- 把"factors"换成实际列出的那些因素。
- 把"aspects"换成具体的方面。
- 把"issues"换成具体的问题。
- 如果一个类别词背后指不出具体实例,删掉这个短语。

抽象类别词是 AI 填充。具体才是内容。

**准则生效的标志:** 输出里没有任何句子在用"factors""aspects""issues"或类似类别词时背后没有具体实例。
