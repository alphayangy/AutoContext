---
name: surgical-changes
description: Use when editing existing code. Prevents unrelated refactors, vanity cleanup, and scope creep that make review harder and introduce risk. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it. Don't delete it.

When your changes create orphans:
- Remove imports, variables, or functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

**This is working if:** every changed line traces directly to the user's request, and no unrelated refactors appear in the diff.
