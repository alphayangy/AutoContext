---
name: comments-default-none-only-why
description: 在写或审查代码时使用。防止复述代码、叙述步骤或随时间腐烂的噪声注释,默认不注释,只在 why 不显然时加。用于 coding 场景。
profiles: [coding]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [change-project]
conflicts: []
---

# 注释:默认无,只解释 why

**默认不注释。只在 why 不显然时注释。**

- 默认不注释。代码应该通过清晰的命名和结构自文档化。
- 只当代码推断不出 why 时加注释:隐藏约束、不变量、非显然边界、或对 spec/上游来源的引用。
- 永不复述代码做什么。永不复述函数名。永不叙述步骤。
- 永不在注释里引用当前 task、PR、fix 或 commit。那些属于 PR 描述,会腐烂。
- lint 抱怨死代码就删代码。不要用注释抑制 lint。

**准则生效的标志:** 注释只在 why 不显然处出现,没有注释复述代码或引用临时 task。
