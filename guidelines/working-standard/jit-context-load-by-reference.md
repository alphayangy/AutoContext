---
name: jit-context-load-by-reference
description: Use when working within a context-limited agent. Prevents context bloat from pre-loading full data, by loading details just-in-time via light references. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers: []
conflicts: []
---

# JIT Context: Load by Reference, Not by Pre-load

**Don't pre-load full data. Give pointers. Load on demand.**

- In system prompts, give file paths, queries, or links. Not full contents.
- Provide retrieval and read tools so the agent can fetch specific slices on demand.
- Let the agent write targeted queries to pull only the fragments it needs.
- Once a fragment is consumed and incorporated, drop the raw result from context.

This is how Claude Code navigates large codebases: `glob`/`grep`/`head`/`tail`, not "paste the whole repo."

**This is working if:** the agent never asks to pre-load full datasets, and context stays focused on the current step.
