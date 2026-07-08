---
name: check-data-grain
description: Use when writing or reviewing SQL before it's finalized. Prevents SQL that runs but returns wrong results due to mismatched grain, aliases, or aggregation. Use in data-analysis contexts.
profiles: [data-analysis]
scopes: [claude, rules]
priority: high
triggers:
  files: ["*.sql", "dbt_project.yml", "*.ipynb"]
  user_intents: [change-project, understand-project]
conflicts: []
---

# Check Data Grain

**Running is not the same as correct. Check the grain before finalizing.**

Before a SQL query is considered done:
- Table names are real and spelled correctly.
- Column names and aliases match the schema.
- The aggregation grain matches the intended metric (per-user, per-day, per-session).
- Join keys are correct and don't multiply or drop rows.

If the grain isn't clear, confirm the metric definition with the user before finalizing.

**This is working if:** no SQL is finalized with a mismatched grain or a fabricated column, and metric definitions are confirmed before aggregation.
