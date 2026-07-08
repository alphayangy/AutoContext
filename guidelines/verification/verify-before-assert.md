---
name: verify-before-assert
description: Use whenever claiming state, status, or completion. Prevents fabricated claims that code is configured, running, tested, or shipped when it isn't. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# Verify Before Assert

**Don't claim what you haven't checked.**

Before stating that something is:
- configured, installed, or running: confirm it actually is.
- tested: run the test and show the result.
- fixed: reproduce the fix, not just the change.
- shipped or deployed: point to the artifact or environment.

If you haven't verified it, say "I haven't verified this" rather than asserting it.

**This is working if:** no status claim appears in output without a corresponding check behind it.
