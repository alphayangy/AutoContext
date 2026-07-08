---
name: positive-instruction-framing
description: Use when writing instructions or rules for an agent. Prevents vague compliance with negation by stating what to do, not what to avoid. Applies to all profiles.
profiles: [all]
scopes: [claude, rules]
priority: medium
triggers: []
conflicts: []
---

# Positive Instruction Framing

**Say what to do. Not what not to do.**

- "Don't use markdown" is weaker than "Write in smoothly flowing prose paragraphs."
- Negation tells the agent what to avoid, but leaves the desired behavior undefined. The agent may comply with the letter while missing the intent.
- Rewrite prohibitions as positive expectations: state the concrete behavior you want.
- Some hard limits still need "never" (safety). But for output and style, prefer positive framing.

**This is working if:** instructions describe the target behavior, and the agent doesn't have to guess what "not X" means in practice.
