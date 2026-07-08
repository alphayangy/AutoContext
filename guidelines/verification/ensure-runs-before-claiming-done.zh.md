---
name: ensure-runs-before-claiming-done
description: 在报告任务完成前使用。防止"代码写完了但跑不起来"或"跑起来了但没通过检查"的常见失败。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 能跑通再说完成

**"完成"意味着能跑且通过检查,不是"我写完了"。**

声称任务完成之前:
- 代码在目标环境能跑。
- 相关检查(lint、类型、测试)通过。
- 如果某项检查跑不了,说明你验证了什么、没验证什么。

写完不等于完成。能跑且通过才算完成。

**准则生效的标志:** 没有任何被报为完成的东西事后发现跑不起来或不通过。
