---
name: address-root-cause-not-symptom
description: Use when fixing a bug or failure. Prevents symptom-suppression that makes the error go away while leaving the underlying cause to resurface later. Use in coding contexts.
profiles: [coding]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Address Root Cause, Not Symptom

**Don't suppress the error. Fix what caused it.**

When fixing a bug:
- Trace to the root cause before writing the fix.
- Don't add a try/catch, null check, or fallback that hides the symptom.
- Suppressing an error is not fixing it. It delays the failure and makes it harder to trace later.
- If the root cause is in code you shouldn't touch, surface it. Don't paper over it locally.
- A real fix prevents the class of failure, not just this instance.

**This is working if:** fixes remove the cause, and no new suppression code appears that masks symptoms without addressing why they occurred.
