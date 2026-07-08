---
name: verify-before-assert
description: 在声称任何状态、进度或完成时使用。防止编造"已配置/已运行/已测试/已发布"的虚假声明。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# 先验证再断言

**没查过的事不要声称。**

在声称某事是某状态之前:
- 已配置/已安装/已运行:确认它确实是。
- 已测试:跑测试,展示结果。
- 已修复:复现修复,而不只是展示改动。
- 已发布/已部署:指向产物或环境。

如果你没验证过,说"我还没验证这个",而不是断言它。

**准则生效的标志:** 输出里没有任何状态声明背后没有对应的检查支撑。
