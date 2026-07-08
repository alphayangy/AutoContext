---
name: prefer-canonical-examples-over-rule-lists
description: Use when writing instructions, rules, or guidance for an agent. Prevents brittle edge-case rule lists that bloat context and miss cases, by using a few diverse canonical examples instead. Applies to all profiles.
profiles: [all]
scopes: [claude, rules]
priority: medium
triggers: []
conflicts: []
---

# Prefer Canonical Examples Over Rule Lists

**A few good examples teach more than a long list of edge-case rules.**

When writing guidance:
- Lead with 2-3 diverse canonical examples that cover the intent.
- Don't try to enumerate every edge case as a rule. The list gets long, brittle, and still misses cases.
- Examples are worth a thousand words of rules. They show the pattern implicitly.
- Use rules to bound the examples, not replace them.

**This is working if:** guidance is shorter, clearer, and the agent generalizes correctly from examples rather than pattern-matching rule text.
