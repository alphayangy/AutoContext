---
name: verify-rendered-ui
description: Use after making frontend or UI changes. Prevents reporting "done" based only on code that looks right, when the rendered interface is broken. Use in frontend-product contexts.
profiles: [frontend-product]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Verify Rendered UI

**Don't report UI work done from code alone. Look at the rendered result.**

After a UI change:
- Start the app, or open the rendered page.
- Check the actual rendered output, not just the source.
- Verify on the target viewport, including responsive layouts where relevant.
- If the app can't run, say what was checked and what wasn't.

Code that looks right can render wrong. The browser is the check.

**This is working if:** no UI change is reported done without the rendered output being inspected.
