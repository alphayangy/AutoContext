---
name: no-hardcoded-results-in-tex
description: Use when writing LaTeX or paper output that reports experimental results. Prevents hardcoded numbers that drift from the actual data when results change. Use in research contexts.
profiles: [research]
scopes: [claude, rules]
priority: high
triggers:
  files: ["*.tex", "*.bib", "results/", "figures/"]
  user_intents: [produce-material]
conflicts: []
---

# No Hardcoded Results in LaTeX

**Numbers in the paper come from scripts, not from typing.**

- Don't paste experimental numbers directly into `.tex` source.
- Generate result values from the data via scripts, macros, or `\input{}` from generated files.
- When results change, the paper updates automatically, not by hand.
- If a number must be hardcoded (rare), note where it came from and when it was last verified.

**This is working if:** re-running the experiment and the generation pipeline updates the paper's numbers without manual edits.
