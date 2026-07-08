---
name: fail-closed-on-error
description: Use when designing error handling in security-sensitive code. Prevents fail-open behavior that grants access or proceeds when an error should have blocked the action. Use in security contexts.
profiles: [security]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Fail Closed on Error

**When something goes wrong, default to deny. Not to allow.**

- On error, reject the action. Don't fall through to a permissive path.
- Don't expose stack traces or internal details to the user.
- Keep error responses consistent to prevent enumeration (same message for wrong user vs. wrong password).
- Log the detail internally. Show the user a generic message.

**This is working if:** no error path in the code grants access, leaks internals, or lets the user infer state from error differences.
