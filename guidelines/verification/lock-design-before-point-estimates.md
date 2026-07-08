---
name: lock-design-before-point-estimates
description: Use when interpreting experimental or statistical results. Prevents confirmation bias where seeing a number first bends the design to fit it. Use in research contexts.
profiles: [research]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [understand-project, produce-material]
conflicts: []
---

# Lock Design Before Point Estimates

**Fix the research design before looking at the numbers.**

Before reading point estimates or final results:
- Lock the research design: variables, sample, method, and pre-registered decisions.
- Lock the analysis plan: what counts as the answer, and what doesn't.
- Only then look at the point estimate.

If the design shifts after seeing the number, the result is no longer the same claim. Say so.

**This is working if:** no analysis plan changes after the result is known, and any post-hoc adjustment is labeled as such.
