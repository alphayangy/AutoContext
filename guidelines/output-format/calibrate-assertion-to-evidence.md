---
name: calibrate-assertion-to-evidence
description: Use when making claims in prose. Prevents over-assertion ("this proves") and reflexive hedging ("might possibly") by matching verb strength to evidence. Use in writing-docs contexts.
profiles: [writing-docs]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [produce-material]
conflicts: []
---

# Calibrate Assertion to Evidence

**Match the verb to the evidence. Don't over-claim. Don't reflexively hedge.**

Strength ladder, weakest to strongest:
- suggest (weak evidence, single observation)
- show (consistent pattern, multiple cases)
- prove (formal, exhaustive)

- Use "suggest" when you have one data point.
- Use "show" when a pattern holds across cases.
- Use "prove" only with formal or exhaustive evidence.
- Don't use "might possibly could" to hedge a claim you actually have evidence for. State the claim and the evidence.

**This is working if:** claim verbs match their evidence strength, with no over-assertion and no reflexive hedging.
