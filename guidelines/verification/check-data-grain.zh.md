---
name: check-data-grain
description: 在定稿前写或审查 SQL 时使用。防止"SQL 跑通了但结果错":粒度、别名、聚合不匹配。用于 data-analysis 场景。
profiles: [data-analysis]
scopes: [claude, rules]
priority: high
triggers:
  files: ["*.sql", "dbt_project.yml", "*.ipynb"]
  user_intents: [change-project, understand-project]
conflicts: []
---

# 核对数据粒度

**跑通不等于对。定稿前核对粒度。**

SQL 被认为完成之前:
- 表名真实且拼写正确。
- 列名和别名与 schema 匹配。
- 聚合粒度与目标指标匹配(按用户、按天、按会话)。
- join key 正确,不会乘多或丢行。

如果粒度不清,在定稿前向用户确认指标定义。

**准则生效的标志:** 没有 SQL 在粒度不匹配或编造列的情况下被定稿,指标定义在聚合前已确认。
