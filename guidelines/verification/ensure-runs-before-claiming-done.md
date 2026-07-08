---
name: ensure-runs-before-claiming-done
description: Use before reporting a task done. Prevents the common failure where code is written but doesn't run, or runs but doesn't pass its checks. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Ensure It Runs Before Claiming Done

**"Done" means it runs and passes, not "I finished writing it."**

Before claiming a task is done:
- The code runs in the target environment.
- The relevant checks (lint, type, test) pass.
- If a check can't be run, say what was verified and what wasn't.

Writing is not done. Running and passing is done.

**This is working if:** nothing reported as done later turns out to not run or not pass.
