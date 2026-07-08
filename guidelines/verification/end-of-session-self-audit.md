---
name: end-of-session-self-audit
description: Use before reporting a task done or merging a large change. Prevents blind spots in the agent's own work by forcing a self-audit of confidence, gaps, and failure modes. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# End-of-Session Self-Audit

**Before saying done, surface your own blind spots.**

Before reporting completion, answer:
1. What are you least confident about in this work?
2. What might you be missing about the situation?
3. If this breaks in 3 months, what's the most likely reason?

Optional additions:
- What assumptions did you make that you never stated explicitly?
- Were there any tools, scripts, or hooks that would've reduced your churn if they'd existed?

Don't wait to be asked. Surface these proactively. About a quarter of what gets surfaced is critical and would otherwise go unspoken.

**This is working if:** blind spots are surfaced before completion, not after the user finds them.
