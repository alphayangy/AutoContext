---
name: no-initiative-beyond-task
description: Use on every task. Prevents scope creep, unrequested docs or READMEs, and "while I'm here" refactors that bloat the diff. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# No Initiative Beyond Task

**Do what was asked. Nothing more, nothing less.**

- Don't create documentation, READMEs, or examples unless explicitly asked.
- Don't add features "while I'm here."
- Don't fix unrelated issues. Log them separately instead.
- Don't restructure code the task didn't touch.

If the user asked for X, ship X. Mention adjacent problems, but don't fix them.

**This is working if:** diffs contain only what the task required, and adjacent issues are reported rather than silently fixed.
