---
name: no-em-dash
description: 在所有生成的文本中使用,包括 CLAUDE.md、AGENTS.md、rules、注释、提交信息。防止 em-dash 这个强烈的 AI 写作痕迹,它打乱节奏并暴露 slop。适用于所有 profile。
profiles: [all]
scopes: [claude, rules]
priority: medium
triggers: []
conflicts: []
---

# 禁用 em-dash

**不要用 em-dash。用逗号、句号、冒号或括号。**

- 用 em-dash 分隔的从句,改用句号、逗号或括号分隔。
- 这适用于所有生成的散文、注释、提交信息和文档。
- 复合词中的连字符和列表标记没问题。作为从句分隔符的 em-dash 不行。

**准则生效的标志:** 生成的输出里不出现 em-dash 字符。
