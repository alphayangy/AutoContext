---
name: think-before-coding
description: Use before implementing any non-trivial change. Prevents assumption-driven coding, hidden confusion, and silent picks between interpretations. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, understand-project]
conflicts: []
---

# Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them. Don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

**This is working if:** clarifying questions come before implementation, not after mistakes.
