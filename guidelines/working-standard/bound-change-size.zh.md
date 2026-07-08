---
name: bound-change-size
description: 在任何非简单改动上使用。防止无法安全评审的超大 diff,要求有体积上限,超了就分阶段拆。用于 coding 场景。
profiles: [coding]
scopes: [claude, rules]
priority: medium
triggers:
  user_intents: [change-project]
conflicts: []
---

# 有界变更体积

**改动要保持小到能评审。不够就拆。**

- 非机械改动应低于一个体积上限(如 800 行)。复杂逻辑更紧(如 500)。
- 超过上限就拆成可评审阶段。先落最小连贯单元。
- 不要为了省往返把无关工作捆进一个改动。
- 大 diff 藏 bug。reviewer 略读。回归就从这里来。

**准则生效的标志:** 没有合并的 diff 在不分级的情况下超过上限,每个阶段都能独立评审。
