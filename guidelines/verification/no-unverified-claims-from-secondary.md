---
name: no-unverified-claims-from-secondary
description: Use when writing claims that cite policies, statistics, or facts from secondary sources. Prevents second-hand misinformation presented as fact. Use in research contexts.
profiles: [research]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [produce-material, understand-project]
conflicts: []
---

# No Unverified Claims From Secondary Sources

**Don't assert what you haven't verified against a primary source.**

- Citations, statistics, venue policies, and factual claims must come from a primary source, not from a summary or a blog.
- If only a secondary source is available, label the claim as unverified.
- Don't attribute quotes or positions to people without checking the original.
- "I read it somewhere" is not a source.

**This is working if:** every factual claim in the output either links to a primary source or is explicitly marked as unverified.
