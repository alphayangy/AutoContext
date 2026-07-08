---
name: auto-context
description: Use before starting, onboarding, or recalibrating any project. Scans the workspace, identifies the project scenario, composes guideline atoms, and generates a reviewable CLAUDE.md, AGENTS.md, or .claude/rules/ context pack.
---

# Auto Context

Project onboarding skill + Context Compiler. Generates minimal, effective agent context files.

## When to Use

- Initialize a new project
- Add context to an existing project
- Recalibrate outdated `CLAUDE.md` / `AGENTS.md`

## Core Flow

```text
Detect → Profile → Ask → Recall → Compose → Render → Review → Write
```

---

## Hard Rules

1. **Always invoke `tools/render-atoms.py`** for `Working Rules` / `Verification` / `Safety`. No placeholders, no hand-writing.
2. **Never rewrite atom content.** Paste the script output verbatim.
3. **Every rule entry must end with `[atom-name]`**.
4. **Do not overwrite existing `CLAUDE.md` / `AGENTS.md`** without explicit user confirmation.
5. **No multi-step processes** in context files. Move them to `.claude/skills/` or `Reference Docs`.
6. **Keep each generated file under 200 lines.** Split to `.claude/rules/` if needed.
7. **Project facts and atoms stay separate.** Facts → `Project Overview` / `Commands` / `Reference Docs`. Atoms → `Working Rules` / `Verification` / `Safety`.

---

## Step 1: Detect Project

Scan high-signal files and output a structured summary.

**Scan method:**

- Run `tree -L 2` once to get the directory skeleton.
- Read the first 30 lines of: `README*`, `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Makefile`, `docker-compose.yml`, and entry scripts.
- Count signals by filename/path only.

**Output summary must include:**

- `workspace_state`: `empty` | `existing` | `partial`
- `detected_stack`: inferred tech stack
- `profile_scores`: top 1–2 profiles with scores and evidence
- `detected_agents`: inferred from existing config files
- `confidence`: primary profile confidence
- `questions`: any clarifying questions

See `@skill-docs/detection-guide.md` for the full agent-file mapping and output field descriptions.

---

## Step 2: Determine Profile

Choose one primary profile and optionally one secondary.

**Profiles:**

- `coding`: software development, tests, scripts
- `frontend-product`: web apps with UI components
- `product-design`: PRDs, user journeys, feature design
- `research`: papers, technical investigation
- `writing-docs`: documentation, tutorials, proposals
- `data-analysis`: SQL, notebooks, metrics
- `creative-media`: video, scripts, content creation

**Confidence rules:**

- `≥ 0.80`: recommend directly
- `0.50–0.79`: ask 1–2 questions
- `< 0.50`: enter empty/uncertain flow

**Avoid misclassification:**

- Don't overclassify when few files exist.
- Executable scripts take priority over data files.
- A `docs/` folder alone does not mean `writing-docs`.
- `package.json` alone does not mean `frontend-product`.

See `@skill-docs/profile-guide.md` for the full signal table.

---

## Step 3: Ask Questions

Ask at most 2 questions, each with at most 3 options. Skip when confidence is high.

**Q1: What type of work next?**

- **A. Modify the project** → coding / frontend / data / creative
- **B. Understand the project** → research / product-design / architecture
- **C. Produce materials** → writing / product-design / research / creative

**Q2: What do you least want to explain repeatedly?**

- **A. Project facts** → stack, dirs, commands
- **B. Working standards** → code rules, quality bars
- **C. Output formats** → doc structure, citations

---

## Step 4: Recall Guideline Atoms

Read `guidelines/index.yaml` to list available atoms, then select by profile and user intent.

**Recall rules:**

1. Recall all atoms with `profiles: [all]`.
2. Recall atoms whose `profiles` include the primary or secondary profile.
3. If an atom declares `triggers.files`, only recall when matching files exist.
4. If an atom declares `triggers.user_intents`, only recall when the answer matches.

**Render with the script:**

```bash
python3 tools/render-atoms.py \
  --working-standard <atom1>,<atom2> \
  --verification <atom3> \
  --safety <atom4> \
  --output /tmp/rendered-rules.md
```

**Hard rules:**

- Paste the script output in full. No placeholders.
- Do not rewrite, compress, or rephrase atom content.
- If an atom is unsuitable, omit it; do not edit it.

---

## Step 5: Compose

Combine facts, answers, and selected atoms.

**Composition rules:**

- Project facts → `Project Overview` / `Commands` / `Reference Docs`
- Atoms → `Working Rules` / `Verification` / `Safety`
- Sort by priority: high → medium → low
- Deduplicate synonymous atoms
- Resolve declared conflicts by relevance/priority
- `priority: high` and `profiles: [all]` atoms are omitted only with concrete evidence
- A global `~/.claude/CLAUDE.md` is never a reason to omit project atoms
- No multi-step processes in context files

---

## Step 6: Select Artifacts and Render Proposal

**Artifact selection principles:**

- Only Claude Code → `CLAUDE.md`
- Cursor / Windsurf / Cline / Trae → `AGENTS.md` + optional native rule file
- Multiple agents → `AGENTS.md` as single source, `CLAUDE.md` imports it
- Large / hybrid projects → `AGENTS.md` + `CLAUDE.md` + `.claude/rules/`
- Existing `CLAUDE.md` to migrate → extract generic rules to `AGENTS.md`, keep Claude-specific pointers in `CLAUDE.md`

**File structure:**

```md
# Project Context

## Project Overview
- Workspace state, profile, stack, dirs, existing configs

## Commands
- Install / run / test / build

## Working Rules
- [rendered atoms]

## Verification
- [rendered atoms]

## Safety
- [rendered atoms]

## Reference Docs
- Pointers to relevant project docs

## When to Update This File
```

See `@skill-docs/artifact-guide.md` for the full mapping table, proposal template, and migration steps.

---

## Step 7: Review

Run before writing. Do not skip.

**Critical checks:**

- `tools/render-atoms.py` was actually invoked
- Every rule entry ends with `[atom-name]`
- No atom rewriting vs source
- No multi-step process leakage
- No project facts mixed into rule sections
- No placeholders like `[TBD]`
- File length ≤ 200 lines
- `CLAUDE.md` references `AGENTS.md`, not reverse

See `@skill-docs/review-checklist.md` for the full 15-item checklist and spot-check procedure.

---

## Step 8: Write

**Write rules:**

- **Write directly by default** after Review passes. Do not ask the user to say "write" or confirm.
- Do not write if Review fails.
- Do not overwrite existing files without confirmation.
- Multi-agent: keep `AGENTS.md` as single source.
- Run `tools/verify-context.py` if both `CLAUDE.md` and `AGENTS.md` are generated.

**Post-write message must include:**

- Which files were written or updated.
- Number and titles of atoms written, in both English and Chinese. Example:
  - "6 working rules, 2 verification rules, 1 safety rule / 6 条工作准则、2 条验证准则、1 条安全准则"
  - "Working Rules: read-before-editing, surgical-changes, simplicity-first, ... / 工作准则：改前阅读、精准修改、先简后繁……"
- When to update the file next.
- Any recommended `.claude/rules/` or `.claude/skills/` next steps.

---

## Meta-Rules

Follow `@skill-docs/meta-rules.md` when executing this skill.
