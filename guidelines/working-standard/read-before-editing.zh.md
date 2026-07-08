---
name: read-before-editing
description: 在修改任何文件前使用。防止盲改破坏上下文、错过现有模式或重复已有逻辑。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 改之前先读

**改之前先理解上下文。**

修改文件之前:
- 读目标文件及其直接上下文。
- 追踪代码如何被调用、什么依赖它。
- 检查同一区域的现有模式、命名和约定。
- 不确定某段代码怎么工作时,先读。不要猜。

**准则生效的标志:** 改动符合现有模式,不会破坏作者没检查过的调用方。
