---
name: banned-ai-words
description: 在所有生成的散文中使用。防止"delve""leverage""seamless""furthermore""it's important to note"等暴露机器生成填充的 AI 痕迹。适用于所有 profile。
profiles: [all]
scopes: [claude, rules]
priority: medium
triggers: []
conflicts: []
---

# 禁用 AI 口水词

**不要用那些暴露 AI 生成填充的词。**

在生成的散文中避免:
- 过渡填充:furthermore、moreover、additionally、notwithstanding、at its core
- AI 动词:delve、leverage、utilize、facilitate、empower、enable
- 营销词:seamless、revolutionary、game-changing、cutting-edge
- 空洞开场白:"In today's world""It's important to note""It's worth noting"

优先用朴素的动词和直接的陈述。

**准则生效的标志:** 生成的文本读起来像用心的人写的,而不是模型在凑字数。
