---
name: evidence-backed-assertions
description: Use when making factual claims in prose. Prevents fabricated quotes, statistics, and attributions presented as fact. Use in writing-docs contexts.
profiles: [writing-docs]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [produce-material]
conflicts: []
---

# Evidence-Backed Assertions

**Every factual claim needs a verifiable source. If you can't cite it, cut it or mark it.**

- Factual claims must point to a source that can be checked.
- Quotes must be verbatim and attributed correctly.
- Statistics must trace to a real dataset or study.
- If a claim can't be verified, mark it `[UNVERIFIED]` or remove it.
- Never generate a quote, attribution, or statistic from memory.

A fabricated quote is defamation risk. A fabricated statistic is misinformation. Both are worse than a gap.

**This is working if:** every factual claim in the output is either backed by a verifiable source or explicitly marked as unverified.
