---
name: no-em-dash
description: Use in all generated text including CLAUDE.md, AGENTS.md, rules, comments, and commit messages. Prevents the em-dash, a strong AI-writing tell that disrupts flow and signals slop. Applies to all profiles.
profiles: [all]
scopes: [claude, rules]
priority: medium
triggers: []
conflicts: []
---

# No Em-Dash

**Don't use em-dashes. Use commas, periods, colons, or parentheses.**

- Replace "X — Y" with "X. Y." or "X, Y." or "X (Y)."
- This applies to all generated prose, comments, commit messages, and docs.
- Hyphens in compound words and list markers are fine. The em-dash as a clause separator is not.

**This is working if:** no em-dash character appears in generated output.
