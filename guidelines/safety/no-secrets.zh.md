---
name: no-secrets
description: 在生成或审查可能含凭据的文件时使用。防止把 API key、token、密码、签名材料提交进版本控制。适用于所有 profile。
profiles: [all]
scopes: [claude, rules]
priority: high
triggers: []
conflicts: []
---

# 不提交密钥

**永远不提交密钥。看到就停下并报告。**

- 不要把 API key、token、密码或私钥写进任何被跟踪的文件。
- 不要在生成的代码或文档里记录或导出凭据。
- 如果遇到已存在的密钥,指出它的位置并停下。不要传播它。
- 本地配置(`.env`、`local.properties`)属于 `.gitignore`,不属于仓库。

**准则生效的标志:** 生成的输出或被跟踪的文件里不出现密钥材料。
