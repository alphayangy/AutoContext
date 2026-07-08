---
name: simplicity-first
description: Use whenever writing or reviewing code. Prevents speculative abstractions, unrequested flexibility, and overcomplication that a senior engineer would reject. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

**This is working if:** fewer rewrites due to overcomplication, and diffs contain only what the task required.
