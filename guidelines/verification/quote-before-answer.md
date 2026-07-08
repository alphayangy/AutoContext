---
name: quote-before-answer
description: Use when answering questions over long documents. Prevents hallucinated answers by forcing the agent to first quote relevant source text, then answer based on those quotes. Applies to all profiles.
profiles: [all]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [understand-project, produce-material]
conflicts: []
---

# Quote Before Answer

**Find the quotes first. Answer from them.**

For long-document tasks:
- First, locate relevant quotes from the source documents. Place them in a `<quotes>` block.
- Then, answer the question based only on those quotes, in an `<info>` block.
- If no relevant quote exists, say so. Don't answer from memory.

This forces grounding in source text and makes hallucination visible.

**This is working if:** every answer traces to a quoted source, and ungrounded claims are flagged as missing.
