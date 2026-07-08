---
name: show-evidence-not-just-assertion
description: 在报告结果、修复或完成时使用。防止 reviewer 无法验证的成功声明,要求声称的同时附上证据。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# 展示证据,不只断言

**别说它成了。展示它成了。**

报告结果时:
- 贴出证明它的测试输出、命令返回值或截图。
- "完成"没有证据只是声明。"完成,这是通过的测试"才是结果。
- 证据太大就指向它在哪里,并引用关键那一行。
- 拿不出证据就明说。不要声称成功。

这条细化 verify-before-assert:不仅要在声称前检查,还要把检查展示出来。

**准则生效的标志:** 输出里没有任何成功声明背后没有附上或指向支撑证据。
