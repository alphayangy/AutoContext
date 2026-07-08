---
name: do-not-guess-schema
description: Use when writing or reviewing SQL, dbt models, or notebooks. Prevents fabricating table names, columns, aliases, and metric definitions that can be inspected. Use in data-analysis contexts.
profiles: [data-analysis]
scopes: [claude, rules]
priority: high
triggers:
  files: ["*.sql", "dbt_project.yml", "*.ipynb"]
  user_intents: [change-project]
conflicts: []
---

# Do Not Guess Schema

**Inspect before asserting. Never fabricate structures that can be queried.**

When writing or reviewing SQL:
- Query `information_schema` or run `DESCRIBE` before referencing tables or columns.
- Confirm join keys and metric definitions before finalizing SQL.
- If a structure cannot be inspected, say so explicitly. Don't guess.
- Don't generate table or column names from memory.

**This is working if:** no SQL is merged that references non-existent tables or columns, and metric grain is confirmed before aggregation.
