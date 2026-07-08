---
name: nitpicky-ordered-code-review
description: Use when reviewing code. Prevents vague, unactionable, or unordered review feedback by requiring nitpicky findings ranked by severity with file:line references. Use in coding contexts.
profiles: [coding]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [understand-project, change-project]
conflicts: []
---

# Nitpicky Ordered Code Review

**Review hard. Rank findings. Point to lines.**

When reviewing code:
- Be deliberately nitpicky: bugs, regressions, architectural or maintenance risk, weak coverage, unclear code, unnecessary complexity, style.
- Rank every finding by severity, highest first.
- Reference each finding with file:line.
- Distinguish blocking from non-blocking. Number each item.
- Skip style/format/lint nits that a linter can enforce. Focus on what a human must catch.

**This is working if:** review output is ordered, line-referenced, severity-ranked, and the author can act on each item without guessing what to fix first.
