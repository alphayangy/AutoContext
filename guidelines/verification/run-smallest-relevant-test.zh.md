---
name: run-smallest-relevant-test
description: 在有测试的项目里改完代码后使用。防止跳过验证或为一个改动等整套测试。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers:
  files: ["*test*", "*spec*", "tests/", "test/"]
  user_intents: [change-project]
conflicts: []
---

# 跑最小相关测试

**用最便宜、能失败的检查先验证。**

改动之后:
- 跑与改动最相关的那个测试或检查。
- 除非改动范围大,否则不要等整套测试。
- 如果测试跑不了,说明原因以及你检查了什么。
- 如果相关检查在你改动前就已经失败,说明这一点。不要声称你的工作让它通过。

**准则生效的标志:** 没有任何改动在没跑过至少一个相关验证的情况下被报完成。
