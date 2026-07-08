---
name: why-first-then-act
description: Use before any non-trivial product or design work. Prevents purposeless implementation, feature cargo-culting, and "just do it" pressure that leads to building the wrong thing. Use in product-design contexts.
profiles: [product-design]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# Why First, Then Act

**Anchor every action to a stated purpose. No purpose, no implementation.**

Before acting:
- Extract the explicit WHY: what outcome does the user want?
- Infer the implicit WHY: what problem are they really solving?
- Verify or ask to confirm the WHY.
- Anchor the proposed work to that WHY.

Danger signals that require stopping and asking:
- "Just do it."
- "It's urgent."
- "Everyone wants this."
- "Competitors have it."
- "Trust me."

"Urgent" is a reason to clarify the WHY faster, not to skip it.

**This is working if:** no feature or design is produced without a stated purpose, and "urgent" triggers more questions, not fewer.
