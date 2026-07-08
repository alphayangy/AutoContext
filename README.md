# Auto Context

A project onboarding skill + context compiler for AI coding agents.

Scans your workspace, detects the project profile, recalls guideline atoms, and generates a minimal but effective `CLAUDE.md`, `AGENTS.md`, or agent-specific context pack.

## Why

Most agent context files are either:
- Too bloated, copied from READMEs and leaked workflows.
- Too vague, just a few generic slogans.
- Constantly rewritten by the LLM, losing the original intent.

Auto Context fixes this by:
1. Detecting project signals with `tree`, not exhaustive file reads.
2. Classifying the project profile (`coding`, `frontend-product`, `data-analysis`, etc.).
3. Recalling **guideline atoms** from a curated rule base.
4. Rendering rules deterministically via `tools/render-atoms.py` so the LLM cannot simplify or rewrite them.
5. Writing a reviewable, version-controllable context file.

## Supported Agents

| Agent | Output File | Install Path |
|-------|-------------|--------------|
| Claude Code | `CLAUDE.md` + `AGENTS.md` | `~/.claude/skills/auto-context/` or `.claude/skills/auto-context/` |
| Cursor | `AGENTS.md` + `.cursor/rules/` (optional) | `.cursor/skills/auto-context/` |
| Kimi Code | `AGENTS.md` | project root or `.kimi-code/` |
| Windsurf / Cline / Trae | `AGENTS.md` + native rules | `.windsurfrules` / `.clinerules` / `.trae/rules/` |

## Install

### Via install script

```bash
git clone https://github.com/alphayangy/AutoContext.git
cd AutoContext
bash install.sh
```

`install.sh` will install the skill for Claude Code globally and for Cursor in the current project by default. Use flags to customize:

```bash
bash install.sh --claude-global    # Claude Code global skill
bash install.sh --claude-project   # Claude Code project skill
bash install.sh --cursor-project   # Cursor project skill
bash install.sh --kimi-project     # Kimi Code project AGENTS.md
bash install.sh --all              # all of the above
```

### Manual install

```bash
# Claude Code (global)
cp -r AutoContext ~/.claude/skills/auto-context

# Claude Code (project)
cp -r AutoContext .claude/skills/auto-context

# Cursor (project)
cp -r AutoContext .cursor/skills/auto-context
```

## Usage

### In Claude Code

Run the skill in any project:

```
/auto-context
```

It will:
1. Scan the project.
2. Detect profile and agents.
3. Select guideline atoms.
4. Render rules via `tools/render-atoms.py`.
5. Write `AGENTS.md` and/or `CLAUDE.md` automatically.

### Standalone atom renderer

You can use the deterministic renderer without running the full skill:

```bash
python3 tools/render-atoms.py \
  --working-standard read-before-editing,surgical-changes \
  --verification ensure-runs-before-claiming-done \
  --safety no-secrets \
  --output /tmp/rules.md
```

## Project Structure

```
auto-context/
├── SKILL.md                  # Skill entry point for Claude Code / Cursor
├── README.md                 # This file
├── LICENSE                   # MIT
├── install.sh                # Multi-agent install script
├── .gitignore
├── guidelines/               # Guideline atoms
│   ├── working-standard/     # Working rules
│   ├── verification/         # Verification rules
│   ├── safety/               # Safety rules
│   └── output-format/        # Output style rules
├── references/               # Reference docs (meta-rules, etc.)
│   └── meta-rules.md
└── tools/
    └── render-atoms.py       # Deterministic atom renderer
```

## Guideline Atoms

Each atom is a markdown file with YAML frontmatter:

```yaml
---
name: read-before-editing
description: Read before modifying any file.
profiles: [all]
scopes: [claude]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# Read Before Editing

**Understand the context before changing it.**

Before modifying a file:
- Read the target file and its immediate context.
- Trace how the code is called and what depends on it.
- Check existing patterns, naming, and conventions in the same area.
- If unsure how something works, read it first. Don't guess.

**This is working if:** edits match existing patterns and don't break callers the author didn't check.
```

Atoms are grouped into `working-standard`, `verification`, `safety`, and `output-format` sections.

## Customizing

To add your own atoms:

1. Create a new `.md` file under `guidelines/<section>/`.
2. Add frontmatter with `name`, `profiles`, `priority`, and optional `triggers`/`conflicts`.
3. Write a bold core sentence, expansion bullets, and an acceptance sentence.
4. Reinstall or symlink the skill to your agent.

## License

MIT
