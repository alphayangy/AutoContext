---
name: write-fuzzers-not-hand-tests
description: Use when asking an LLM to write tests. Prevents performative hand-tests that pass review but miss real bugs, by directing the LLM to write fuzzers and property tests instead. Use in coding contexts.
profiles: [coding]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Write Fuzzers, Not Hand-Tests

**LLM-default tests are performative. Direct them to find real bugs.**

- LLMs default to writing tests that "look thorough enough to pass human review" but only cover happy paths. They never fail, and never find bugs.
- Instead of "Write tests", ask: "Look for risky areas, find invariants, and fuzz them."
- Give the LLM explicit guidance on how to vary inputs to provoke failures. Without guidance, coverage is poor.
- Fuzzers and property tests find real bugs in minutes. Hand-tests find none.

**This is working if:** generated tests fail on adversarial inputs, not just pass on happy paths.
