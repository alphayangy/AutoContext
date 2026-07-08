---
name: verify-citation-exists
description: Use when writing citations or references into research output. Prevents fabricated papers, authors, and DOIs that don't exist. Use in research contexts.
profiles: [research]
scopes: [claude, rules]
priority: high
triggers:
  files: ["*.tex", "*.bib", "references/", "citations/"]
  user_intents: [produce-material, understand-project]
conflicts: []
---

# Verify Citation Exists

**Don't write a citation until you've confirmed the source is real.**

Before putting a reference into output:
- Verify the paper exists. Check the DOI, or the URL, or a reputable index.
- Verify the authors and title match.
- If you can't verify, don't cite it. Mark it as unverified or remove it.
- Never generate a DOI, URL, or bibliographic entry from memory.

A fabricated citation is worse than no citation. It's also a defamation risk if the attribution is wrong.

**This is working if:** no citation in the output points to a source that can't be located in a real index.
