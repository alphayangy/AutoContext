---
name: concrete-over-abstract
description: Use when generating prose. Prevents abstract category words like "factors", "aspects", "issues" that fill space without saying anything. Use in writing-docs contexts.
profiles: [writing-docs]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [produce-material]
conflicts: []
---

# Concrete Over Abstract

**Use specific nouns. Behind every phrase, point to a number, file, or mechanism.**

- Replace "factors" with the actual factors named.
- Replace "aspects" with the specific aspects.
- Replace "issues" with the concrete issues.
- If you can't point to a specific instance behind a category word, cut the phrase.

Abstract category words are AI filler. Specifics are content.

**This is working if:** no sentence in the output uses "factors", "aspects", "issues", or similar category words without a concrete instance behind it.
