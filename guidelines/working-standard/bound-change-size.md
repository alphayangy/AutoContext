---
name: bound-change-size
description: Use on any non-trivial change. Prevents oversized diffs that can't be reviewed safely by requiring a size cap with staged breakdown when exceeded. Use in coding contexts.
profiles: [coding]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [change-project]
conflicts: []
---

# Bound Change Size

**Keep changes small enough to review. Split when they aren't.**

- Non-mechanical changes should stay under a size cap (e.g., 800 lines). Complex logic under a tighter cap (e.g., 500).
- If a change exceeds the cap, split it into reviewable stages. Land the smallest coherent unit first.
- Don't bundle unrelated work into one change to save round-trips.
- Large diffs hide bugs. Reviewers skim. That's where regressions land.

**This is working if:** no merged diff exceeds the cap without being staged, and each stage is independently reviewable.
