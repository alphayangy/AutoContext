---
name: fail-closed-on-error
description: 在安全敏感代码里设计错误处理时使用。防止出错时放行(fail-open),本该拒绝的操作却通过。用于 security 场景。
profiles: [security]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 出错时默认拒绝

**出问题时,默认拒绝。不是默认放行。**

- 出错时拒绝操作。不要落到放行路径。
- 不要向用户暴露堆栈或内部细节。
- 错误响应保持一致以防枚举(错用户与错密码用同样消息)。
- 内部记录细节。给用户看通用消息。

**准则生效的标志:** 代码里没有任何错误路径会授予访问、泄露内部、或让用户从错误差异推断状态。
