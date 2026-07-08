---
name: minimal-privilege-agent-tools
description: Use when designing agents or tool-calling systems. Prevents over-privileged agents that can run destructive operations without approval. Use in security contexts.
profiles: [security]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Minimal Privilege Agent Tools

**Give an agent the smallest tool set that can do the job. Nothing more.**

- Start with read-only tools. Add write or exec tools only when the task requires them.
- Use short-lived, scoped tokens. Not long-lived broad credentials.
- Destructive operations require human approval before execution, not after.
- Log every tool call with arguments and result.
- Revoke tools the agent no longer needs during the session.

**This is working if:** no agent holds a tool or credential broader than its current task requires, and no destructive operation runs without explicit approval.
