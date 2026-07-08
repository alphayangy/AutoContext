---
name: end-of-session-self-audit
description: 在报告任务完成或合并大改动前使用。通过强制自审置信度、遗漏和失败模式,防止 agent 自己工作里的盲区。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# 收尾自审

**说完成之前,先暴露自己的盲区。**

报告完成之前,回答:
1. 这份工作里你最小置信的是什么?
2. 关于这个情况,你可能漏掉了什么?
3. 如果这三个月后坏了,最可能的原因是什么?

可选补充:
- 你做了哪些从未明确说出来的假设?
- 有没有什么工具、脚本或钩子,如果一开始就有,会减少你的反复折腾?

不要等用户问。主动暴露。大约 1/4 被暴露出来的是关键问题,否则不会被说出来。

**准则生效的标志:** 盲区在完成前被暴露,而不是用户事后发现。
