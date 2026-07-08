---
name: surgical-changes
description: 在编辑现有代码时使用。防止无关重构、虚荣式清理、以及让审查更困难并引入风险的范围蔓延。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 外科手术式修改

**只动必须动的地方。只清理自己造成的混乱。**

编辑现有代码时:
- 不要"改进"相邻的代码、注释或格式。
- 不要重构没有问题的部分。
- 遵循现有风格,即使你自己会采用不同方式。
- 如果发现无关的死代码,提一句。不要删除。

当你的改动产生孤立代码时:
- 删除因你的改动而变得未使用的 import、变量或函数。
- 除非被要求,否则不要删除预先存在的死代码。

**准则生效的标志:** 每一行改动都能直接追溯到用户请求,diff 里没有无关重构。
