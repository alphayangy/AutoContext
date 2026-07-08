---
name: quote-before-answer
description: 在长文档上回答问题时使用。防止幻觉回答,强制 agent 先引用相关原文,再基于引用作答。适用于所有 profile。
profiles: [all]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [understand-project, produce-material]
conflicts: []
---

# 先引再答

**先找到引用。基于引用作答。**

长文档任务:
- 先定位源文档里的相关引用,放进 `<quotes>` 块。
- 然后只基于这些引用回答问题,放进 `<info>` 块。
- 如果没有相关引用,说明没有。不要凭记忆回答。

这强制基于原文,让幻觉可见。

**准则生效的标志:** 每个回答都能追溯到引用的来源,无依据的声明被标为缺失。
