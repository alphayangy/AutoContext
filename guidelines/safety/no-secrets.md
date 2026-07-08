---
name: no-secrets
description: Use when generating or reviewing any file that may contain credentials. Prevents committing API keys, tokens, passwords, and signing material into version control. Applies to all profiles.
profiles: [all]
scopes: [claude, rules]
priority: high
triggers: []
conflicts: []
---

# No Secrets

**Never commit secrets. If you see one, stop and report it.**

- Don't write API keys, tokens, passwords, or private keys into any tracked file.
- Don't log or export credentials in generated code or docs.
- If you encounter an existing secret, name its location and stop. Don't propagate it.
- Local config (`.env`, `local.properties`) belongs in `.gitignore`, not in the repo.

**This is working if:** no secret material appears in generated output or tracked files.
