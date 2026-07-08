---
name: address-root-cause-not-symptom
description: 在修 bug 或故障时使用。防止"让错误消失"的症状抑制,留下根因以后再冒头。用于 coding 场景。
profiles: [coding]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 修根因,不修症状

**不要抑制错误。修导致它的原因。**

修 bug 时:
- 写修复前先追到根因。
- 不要加 try/catch、null check 或 fallback 来掩盖症状。
- 抑制错误不是修复。它推迟失败,让以后更难追。
- 如果根因在你不该碰的代码里,把它暴露出来。不要在本地糊过去。
- 真修复防止一整类失败,不只是这一个实例。

**准则生效的标志:** 修复移除原因,没有新的抑制代码出现来掩盖症状而不处理为什么发生。
