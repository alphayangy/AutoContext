---
name: no-hardcoded-results-in-tex
description: 在写 LaTeX 或报告实验结果的论文输出时使用。防止硬编码的数字在结果变化时与真实数据脱节。用于 research 场景。
profiles: [research]
scopes: [claude, rules]
priority: high
triggers:
  files: ["*.tex", "*.bib", "results/", "figures/"]
  user_intents: [produce-material]
conflicts: []
---

# 不把结果硬编码进 LaTeX

**论文里的数字来自脚本,不是手敲的。**

- 不要把实验数字直接粘贴进 `.tex` 源码。
- 通过脚本、宏或从生成文件 `\input{}` 来生成结果值。
- 结果变化时,论文自动更新,而不是手动改。
- 如果某个数字必须硬编码(罕见),注明它来自哪里、上次验证是什么时候。

**准则生效的标志:** 重跑实验和生成管线后,论文里的数字无需手动编辑就更新了。
