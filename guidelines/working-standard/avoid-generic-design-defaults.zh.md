---
name: avoid-generic-design-defaults
description: 在为前端产品生成 UI 或视觉设计时使用。防止默认的 AI 生成外观(Tailwind blue-500、紫蓝渐变、3 列图标网格、blob SVG)让每个产品看起来都一样。用于 frontend-product 场景。
profiles: [frontend-product]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# 避开千篇一律的默认设计

**不要交付那种一看就是"AI 做的"外观。**

避免这些暴露机器生成填充的默认:
- Tailwind `blue-500` 作为主色。
- 紫到蓝的渐变背景。
- 3 列图标加文字的功能网格。
- 抽象 blob SVG 和装饰性形状。
- 通用模板文案("revolutionize your workflow")。

带着具体目的和独特声音来设计。如果某一段能原封不动出现在任何通用 SaaS 站点上,那就太通用了。

**准则生效的标志:** 生成的 UI 不复用默认 AI 配色和布局套路,每一节都有存在的理由。
