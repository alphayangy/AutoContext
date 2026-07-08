---
name: no-prod-deploy-without-confirmation
description: 在改动可能触及生产或高危环境(mainnet、prod、live)时使用。防止误部署、直推 main、不可逆的发布。适用于所有 profile。
profiles: [all]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 不确认不部署生产

**没有明确确认就不往 prod 或 mainnet 发。**

- 不直推 `main`、`master` 或 `production`。
- 没有明确的"yes",不部署到 mainnet、生产或 live 环境。
- 没有签字确认,不在高危目标上跑 release、publish 或 deploy 命令。
- 不确定某环境是否高危,先问。

**准则生效的标志:** 没有任何改动在未经用户明确确认的情况下触及生产或 mainnet 级环境。
