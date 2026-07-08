---
name: comments-default-none-only-why
description: Use when writing or reviewing code. Prevents noise comments that restate code, narrate steps, or rot with time, by defaulting to no comment and adding only when the why is non-obvious. Use in coding contexts.
profiles: [coding]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [change-project]
conflicts: []
---

# Comments: Default None, Only Why

**Don't comment by default. Comment only when the why is non-obvious.**

- Default to no comment. Code should self-document through clear names and structure.
- Add a comment only when the why can't be inferred from the code: a hidden constraint, an invariant, a non-obvious boundary, or a reference to a spec or upstream source.
- Never restate what the code does. Never restate the function name. Never narrate the steps.
- Don't reference the current task, PR, fix, or commit in a comment. That belongs in the PR description and rots.
- If a lint complains about dead code, delete the code. Don't suppress the lint with a comment.

**This is working if:** comments only appear where the why is non-obvious, and no comment restates code or references a transient task.
