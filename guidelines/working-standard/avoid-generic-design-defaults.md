---
name: avoid-generic-design-defaults
description: Use when generating UI or visual design for a frontend product. Prevents the default AI-generated look (Tailwind blue-500, purple-blue gradients, 3-column icon grids, blob SVGs) that makes every product look identical. Use in frontend-product contexts.
profiles: [frontend-product]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [change-project, produce-material]
conflicts: []
---

# Avoid Generic Design Defaults

**Don't ship the look that says "AI made this."**

Avoid these defaults that signal machine-generated filler:
- Tailwind `blue-500` as the primary color.
- Purple-to-blue gradient backgrounds.
- 3-column icon-plus-text feature grids.
- Abstract blob SVGs and decorative shapes.
- Generic stock copy ("revolutionize your workflow").

Design with a specific purpose and a distinct voice. If a section could appear unchanged on any generic SaaS site, it's too generic.

**This is working if:** generated UI doesn't reuse the default AI palette and layout clichés, and each section has a reason to exist.
