---
name: llm-output-as-untrusted
description: Use when LLM-generated output flows into SQL, shell, DOM, eval, or tool calls. Prevents prompt injection and hallucination from becoming code execution or data corruption. Use in security contexts.
profiles: [security]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# LLM Output as Untrusted Input

**Treat model output as hostile data until checked.**

Before LLM-generated text reaches any execution or rendering sink:
- SQL: parameterize, don't concatenate model output.
- Shell: don't pass model output to a shell string. Use list-form `subprocess` and validate inputs.
- DOM: escape and sanitize. Don't `innerHTML` model output.
- `eval` / dynamic exec: don't. Find a static path.
- Tool calls: validate the arguments against a schema before dispatch.

Separate trusted instructions from untrusted data with clear delimiters. Don't put secrets or auth logic in the system prompt.

**This is working if:** no model-generated string reaches an execution sink without validation, escaping, or sandboxing.
