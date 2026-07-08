---
name: no-llm-attribution-in-commits
description: 在生成提交信息或 PR 描述时使用。防止 LLM 署名、co-author 行和"Generated with Claude Code"脚注污染历史并可能违反政策。适用于所有 profile。
profiles: [all]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [change-project]
conflicts: []
---

# 提交不带 LLM 署名

**不要在提交或 PR 里加 LLM 署名。**

- 不加"Generated with Claude Code"脚注。
- 不加 `Co-Authored-By: Claude` 行。
- 不加"AI-assisted"备注,除非用户明确要求。

提交信息应该描述改了什么和为什么,而不是谁或什么写的。

**准则生效的标志:** git log 和 PR 描述里没有 LLM 署名,除非用户要求加。
