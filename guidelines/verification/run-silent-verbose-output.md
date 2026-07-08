---
name: run-silent-verbose-output
description: Use when running build, test, or lint commands in an agent workflow. Prevents verbose output from flooding context and avoids forced re-runs caused by pipe truncation. Use in coding contexts.
profiles: [coding]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Run Silent: Compress Verbose Output to ✓

**Success costs <10 tokens. Failure dumps everything.**

When running build, test, or lint commands:
- Wrap commands so success only prints `✓ <desc>`. Failure dumps the full output.
- Store output in a temp file, not in context. Drop it on success.
- Don't pipe through `head`/`tail` to save tokens. The pipe kills the process, forcing a 5-minute re-run next time.
- Iterate toward one-error-at-a-time: `pytest -x`, `jest --bail`, `go test -failfast`.

**This is working if:** successful checks cost <10 tokens of context, and no command is re-run because its output was truncated.
