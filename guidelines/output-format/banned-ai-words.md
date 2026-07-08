---
name: banned-ai-words
description: Use in all generated prose. Prevents AI tells like "delve", "leverage", "seamless", "furthermore", "it's important to note" that mark text as machine-generated filler. Applies to all profiles.
profiles: [all]
scopes: [claude, rules]
priority: medium
triggers: []
conflicts: []
---

# Banned AI Words

**Don't use the words that signal AI-generated filler.**

Avoid these in generated prose:
- Transition filler: furthermore, moreover, additionally, notwithstanding, at its core
- AI verbs: delve, leverage, utilize, facilitate, empower, enable
- Marketing words: seamless, revolutionary, game-changing, cutting-edge
- Empty openers: "In today's world", "It's important to note", "It's worth noting"

Prefer plain verbs and direct statements.

**This is working if:** generated text reads like a careful human wrote it, not a model filling space.
