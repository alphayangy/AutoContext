# Auto Context

> English | [中文](README.zh.md)

A project onboarding skill + context compiler for AI coding agents.

Scans your workspace, detects the project profile, recalls guideline atoms, and generates a minimal but effective `CLAUDE.md`, `AGENTS.md`, or agent-specific context pack.

## Why

Every new agent session starts the same way: you explain the project, repeat the conventions, and correct the same mistakes. Existing tools only solve part of this:

- **Coverage is too narrow.** Claude Code `/init` and `AGENTS.md` are still mostly about code repos. Research reports, product docs, data analysis, writing projects, and creative work are left out — so users have to write context from scratch for anything that is not pure engineering.
- **Quality is too fragile.** Hand-written `AGENTS.md` / `CLAUDE.md` files quickly accumulate context-quality smells: README copy-paste, leaked multi-step workflows, lint rules rewritten as prose, and conflicting instructions. The agent ends up missing constraints, contradicting itself, or wasting tokens on noise.
- **There is no credible "how-to-work" layer.** `/init` tells the agent *what* the project is, and skills tell it how to run a specific workflow. But neither provides stable, reusable working standards distilled from real usage. Agents keep reinventing "read before editing", "run the smallest test", or "do not guess schema" every session.

Auto Context is a **context compiler** with a curated library of working rules:

- **Broad coverage** across code and non-code work via Context Profiles.
- **Quality control** by selecting, ranking, and rendering rules deterministically — no LLM simplification, no README bloat, no workflow leakage.
- **Credible rules** distilled from a large corpus of real `CLAUDE.md` / `AGENTS.md` files collected across the web, plus empirical research on agent manifests. These are reusable working standards extracted from many projects, not rules invented for a single session.
- **Clean separation**: project facts and long-term rules go into `CLAUDE.md` / `AGENTS.md`, multi-step workflows become `.claude/skills/`, path-specific rules become `.claude/rules/`.

> `/init` for every kind of work, not just code repos.

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
├── SKILL.md                  # Skill entry point for Claude Code / Cursor (English)
├── SKILL.zh.md               # Skill entry point (Chinese)
├── README.md                 # This file (English)
├── README.zh.md              # Chinese version
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
    ├── render-atoms.py       # Deterministic atom renderer
    └── verify-context.py     # Verify CLAUDE.md / AGENTS.md reference direction
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
