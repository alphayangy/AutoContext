---
name: verify-rendered-ui
description: 在做前端或 UI 改动后使用。防止只看代码"看起来对"就报完成,而渲染出来的界面是坏的。用于 frontend-product 场景。
profiles: [frontend-product]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 检查渲染出的 UI

**不要只凭代码就报 UI 完成。看渲染结果。**

UI 改动之后:
- 启动应用,或打开渲染后的页面。
- 检查实际渲染输出,而不只是源码。
- 在目标视口验证,包括相关的响应式布局。
- 如果应用跑不起来,说明你检查了什么、没检查什么。

代码看起来对,渲染可能错。浏览器才是检查。

**准则生效的标志:** 没有 UI 改动在没检查渲染输出的情况下被报完成。
