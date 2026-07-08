---
name: goal-driven-execution
description: Use on any multi-step or ambiguous task. Prevents weak success criteria like "make it work" that require constant clarification and endless looping. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → write tests for invalid inputs, then make them pass.
- "Fix the bug" → write a test that reproduces it, then make it pass.
- "Refactor X" → ensure tests pass before and after.

For multi-step tasks, state a brief plan:
1. [Step] → verify: [check]
2. [Step] → verify: [check]

Strong success criteria let you loop independently. Weak criteria require constant clarification.

**This is working if:** the agent loops toward a defined end state and stops when verification passes, instead of asking "is this good?" repeatedly.
