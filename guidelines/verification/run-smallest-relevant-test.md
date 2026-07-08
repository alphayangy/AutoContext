---
name: run-smallest-relevant-test
description: Use after any code change in a project with tests. Prevents skipping verification or waiting for the full suite when one test would confirm the change. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  files: ["*test*", "*spec*", "tests/", "test/"]
  user_intents: [change-project]
conflicts: []
---

# Run the Smallest Relevant Test

**Verify with the cheapest check that can fail first.**

After a change:
- Run the single test or check most relevant to the change.
- Don't wait for the full suite unless the change is wide.
- If tests can't run, explain why and what was checked instead.
- If the relevant check already failed before your change, say so. Don't claim your work caused a pass.

**This is working if:** no change is reported done without at least one relevant verification run.
