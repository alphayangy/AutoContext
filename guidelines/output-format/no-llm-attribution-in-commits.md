---
name: no-llm-attribution-in-commits
description: Use when generating commit messages or PR descriptions. Prevents LLM signatures, co-author lines, and "Generated with Claude Code" footers that pollute history and may violate policy. Applies to all profiles.
profiles: [all]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [change-project]
conflicts: []
---

# No LLM Attribution in Commits

**Don't sign commits or PRs with LLM attribution.**

- No "Generated with Claude Code" footer.
- No `Co-Authored-By: Claude` lines.
- No "AI-assisted" notes unless the user explicitly asks for them.

Commit messages should describe what changed and why, not who or what wrote them.

**This is working if:** git log and PR descriptions contain no LLM attribution unless the user asked for it.
