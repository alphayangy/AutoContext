---
name: read-before-editing
description: Use before modifying any file. Prevents blind edits that break context, miss existing patterns, or duplicate existing logic. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Read Before Editing

**Understand the context before changing it.**

Before modifying a file:
- Read the target file and its immediate context.
- Trace how the code is called and what depends on it.
- Check existing patterns, naming, and conventions in the same area.
- If unsure how something works, read it first. Don't guess.

**This is working if:** edits match existing patterns and don't break callers the author didn't check.
