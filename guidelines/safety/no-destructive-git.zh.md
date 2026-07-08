---
name: no-destructive-git
description: 在运行 git 命令时使用。防止 force-push、hard reset、压缩已推送提交等改写历史的操作破坏工作或打乱审查者跟踪。适用于所有 profile。
profiles: [all]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 不跑破坏性 git

**除非明确要求,否则不改写历史。**

没有用户明确要求时,不要跑这些:
- `git push --force` / `--force-with-lease` 推到共享分支。
- `git reset --hard` 丢弃未提交的工作。
- `git rebase` 或 `git commit --amend` 已推送的提交。
- `git push --no-verify` 跳过钩子。

如果分支是共享的或已推送的,把它的历史当作固定的。

**准则生效的标志:** 没有共享或已推送的历史在未经用户明确同意的情况下被改写。
