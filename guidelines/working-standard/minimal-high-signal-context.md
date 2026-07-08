---
name: minimal-high-signal-context
description: Use whenever working within a context-limited agent. Prevents context rot and dilution by keeping the working context to the smallest high-signal token set that achieves the goal. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers: []
conflicts: []
---

# Minimal High-Signal Context

**Context is a finite resource. Maximize signal per token.**

- Keep only the smallest set of high-signal tokens needed for the current step.
- Load details just-in-time: leave a light reference (path, query, link) and load on demand. Don't pre-load.
- Once a tool result has been consumed and its content incorporated, drop the raw result from context.
- If context feels polluted or the agent keeps repeating mistakes, reset and start fresh with a better initial prompt.
- More tokens is not more capability. Marginal returns diminish.

**This is working if:** the working context stays focused on the current step, and stale or consumed content is dropped rather than carried.
