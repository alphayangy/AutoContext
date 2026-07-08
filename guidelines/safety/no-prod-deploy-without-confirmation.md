---
name: no-prod-deploy-without-confirmation
description: Use when changes may reach production or a high-stakes environment such as mainnet, prod, or live. Prevents accidental deployments, direct pushes to main, and irreversible releases. Applies to all profiles.
profiles: [all]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# No Prod Deploy Without Confirmation

**Don't ship to prod or mainnet without explicit confirmation.**

- Don't push directly to `main`, `master`, or `production`.
- Don't deploy to mainnet, production, or live environments without a clear "yes."
- Don't run release, publish, or deploy commands on high-stakes targets without sign-off.
- If unsure whether an environment is high-stakes, ask first.

**This is working if:** no change reaches a production or mainnet-like environment without explicit user confirmation.
