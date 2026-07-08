---
name: llm-output-as-untrusted
description: 在 LLM 生成的输出流入 SQL、shell、DOM、eval 或工具调用时使用。防止 prompt injection 和幻觉变成代码执行或数据损坏。用于 security 场景。
profiles: [security]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# LLM 输出当不可信输入

**模型输出当恶意数据对待,直到检查通过。**

LLM 生成的文本到达任何执行或渲染接收端之前:
- SQL:参数化,不要拼接模型输出。
- Shell:不要把模型输出传进 shell 字符串。用列表式 `subprocess` 并校验输入。
- DOM:转义并消毒。不要 `innerHTML` 模型输出。
- `eval` / 动态 exec:不要。找静态路径。
- 工具调用:派发前按 schema 校验参数。

用清晰分隔符把可信指令和不可信数据分开。不要把密钥或鉴权逻辑放进系统提示。

**准则生效的标志:** 没有任何模型生成的字符串在未经验证、转义或沙箱化的情况下到达执行接收端。
