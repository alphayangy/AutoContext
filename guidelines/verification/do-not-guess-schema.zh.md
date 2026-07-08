---
name: do-not-guess-schema
description: 在写或审查 SQL、dbt 模型、notebook 时使用。防止编造能查到的表名、列、别名和指标定义。用于 data-analysis 场景。
profiles: [data-analysis]
scopes: [claude, rules]
priority: high
triggers:
  files: ["*.sql", "dbt_project.yml", "*.ipynb"]
  user_intents: [change-project]
conflicts: []
---

# 不猜表结构

**断言前先查。永远不编造能查询到的结构。**

写或审查 SQL 时:
- 引用表或列之前,查 `information_schema` 或跑 `DESCRIBE`。
- 定稿 SQL 前确认 join key 和指标定义。
- 如果某结构查不到,明确说明。不要猜。
- 不要凭记忆生成表名或列名。

**准则生效的标志:** 没有 SQL 在合并后引用不存在的表或列,指标粒度在聚合前已确认。
