---
name: show-evidence-not-just-assertion
description: Use whenever reporting a result, fix, or completion. Prevents success claims that reviewers can't verify, by requiring the evidence to be shown alongside the claim. Applies to all profiles.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# Show Evidence, Not Just Assertion

**Don't say it worked. Show that it worked.**

When reporting a result:
- Paste the test output, command return value, or screenshot that proves it.
- "Done" without evidence is a claim. "Done, here's the passing test" is a result.
- If the evidence is too large, point to where it is and quote the key line.
- If you can't produce evidence, say so explicitly. Don't claim success.

This refines verify-before-assert: not only must you check before claiming, you must show the check.

**This is working if:** no success claim appears in output without supporting evidence attached or referenced.
