---
name: no-destructive-git
description: Use when running git commands. Prevents force-push, hard resets, squashing pushed commits, and other history-rewriting operations that destroy work or break reviewer tracking. Applies to all profiles.
profiles: [all]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# No Destructive Git

**Don't rewrite history unless explicitly asked.**

Don't run these without explicit user request:
- `git push --force` / `--force-with-lease` to shared branches.
- `git reset --hard` to discard uncommitted work.
- `git rebase` or `git commit --amend` on already-pushed commits.
- `git push --no-verify` to skip hooks.

If a branch is shared or pushed, treat its history as fixed.

**This is working if:** no shared or pushed history is rewritten without explicit user sign-off.
