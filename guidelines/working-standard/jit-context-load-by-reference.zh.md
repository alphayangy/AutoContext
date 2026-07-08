---
name: jit-context-load-by-reference
description: 在 context 受限的 agent 里工作时使用。防止预灌全量数据导致 context 膨胀,通过轻量引用按需加载细节。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers: []
conflicts: []
---

# JIT context:按引用加载,不预灌

**不要预灌全量数据。给指针。按需拉取。**

- 系统提示里给文件路径、查询或链接,不给全量内容。
- 提供检索和读取工具,让 agent 按需拉具体片段。
- 让 agent 自己写 targeted query,只拉它需要的片段。
- 片段被消费、内容吸收后,把原始结果从 context 丢掉。

这就是 Claude Code 翻大代码库的方式:用 `glob`/`grep`/`head`/`tail`,不是"把整个 repo 贴进来"。

**准则生效的标志:** agent 不要求预灌全量数据,context 聚焦在当前步骤。
