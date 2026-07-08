---
name: no-unverified-claims-from-secondary
description: 在写引用政策、统计或来自二手来源的事实的声明时使用。防止把二手错误信息当事实陈述。用于 research 场景。
profiles: [research]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [produce-material, understand-project]
conflicts: []
---

# 不断言未经验证的二手信息

**没对照一手来源验证过的事,不要断言。**

- 引用、统计、会场政策和事实声明必须来自一手来源,而不是摘要或博客。
- 如果只有二手来源,把声明标为未验证。
- 不要在不查原文的情况下把引语或观点归给某人。
- "我在哪读过"不算来源。

**准则生效的标志:** 输出里每一个事实声明要么指向一手来源,要么被明确标为未验证。
