---
name: nitpicky-ordered-code-review
description: 在审查代码时使用。防止含糊、不可操作或无序的审查反馈,要求按严重度排序、带 file:line 引用的 nitpicky 发现。用于 coding 场景。
profiles: [coding]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [understand-project, change-project]
conflicts: []
---

# Nitpicky 有序代码评审

**评审要狠。发现要排序。指向行号。**

审查代码时:
- 刻意 nitpicky:bug、回归、架构或维护风险、弱覆盖、不清晰代码、不必要复杂度、风格。
- 每个发现按严重度排序,最严重的在前。
- 每个发现引用 file:line。
- 区分阻塞与非阻塞。每条编号。
- 跳过 linter 能管的风格/格式/lint 抠细节。聚焦必须人来抓的。

**准则生效的标志:** 评审输出有序、带行号引用、按严重度排序,作者能逐条行动而不用猜先修哪个。
