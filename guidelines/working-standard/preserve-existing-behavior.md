---
name: preserve-existing-behavior
description: Use when changing code that has existing users, callers, or contracts. Prevents regressions disguised as cleanup or design taste. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Preserve Existing Behavior

**Don't break userspace. Existing behavior beats theoretical cleanliness.**

- Don't introduce regressions just because a new design feels cleaner.
- Binary compatibility, public APIs, and established workflows are not optional.
- "Users should update" is not an argument. It's an admission of failure.
- If a change must break behavior, get explicit confirmation first and state the cost.

**This is working if:** no existing test, caller, or user workflow breaks without explicit user sign-off.
