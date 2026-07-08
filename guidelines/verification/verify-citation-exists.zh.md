---
name: verify-citation-exists
description: 在把引用或参考文献写进研究输出时使用。防止编造不存在的论文、作者和 DOI。用于 research 场景。
profiles: [research]
scopes: [claude, rules]
priority: high
triggers:
  files: ["*.tex", "*.bib", "references/", "citations/"]
  user_intents: [produce-material, understand-project]
conflicts: []
---

# 引用写入前查证存在

**没确认来源真实之前,不要写引用。**

把参考文献放进输出之前:
- 验证论文存在。查 DOI,或 URL,或可信索引。
- 验证作者和标题对得上。
- 查不到就不要引。标为未验证或删掉。
- 永远不要凭记忆生成 DOI、URL 或书目条目。

编造的引用比不引用更糟。如果归属错误,还有诽谤风险。

**准则生效的标志:** 输出里没有任何引用指向在真实索引里找不到的来源。
