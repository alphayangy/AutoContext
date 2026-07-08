---
name: run-silent-verbose-output
description: 在 agent 工作流里跑 build、test、lint 命令时使用。防止 verbose 输出灌爆 context,避免管道截断导致的被迫重跑。用于 coding 场景。
profiles: [coding]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 静默运行:把 verbose 输出压成 ✓

**成功耗 <10 token。失败才 dump 全部。**

跑 build、test、lint 命令时:
- 包一层,成功只输出 `✓ <描述>`,失败才 dump 全输出。
- 输出存临时文件,不进 context。成功就丢。
- 不要用 `head`/`tail` 管道截断省 token。管道会杀掉进程,下次被迫重跑 5 分钟套件。
- 迭代到一次一个错:`pytest -x`、`jest --bail`、`go test -failfast`。

**准则生效的标志:** 成功的检查只耗 <10 token,没有命令因为输出被截断而重跑。
