---
name: bounded-consumption
description: Use when building systems that serve users or agents with potentially unbounded requests. Prevents resource exhaustion from runaway loops, abuse, or infinite retries. Use in security contexts.
profiles: [security]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Bounded Consumption

**Every user, session, and agent has a budget. Enforce it.**

- Per-user rate limits on requests.
- Per-user token and cost budgets for LLM calls.
- Hard timeouts on long-running operations. No unbounded loops.
- Retry budgets: cap attempts and total retry time. Honor `Retry-After`.
- Circuit breakers when a dependency keeps failing.

**This is working if:** no user or agent can consume unbounded resources, and runaway loops hit a hard stop rather than running forever.
