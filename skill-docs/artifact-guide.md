# Artifact Selection Guide

Detailed reference for AutoContext Step 6: choosing output files and rendering the proposal.

## Artifact Selection

Artifact selection is determined by `detected_agents` and project scale:

| Scenario | Artifact |
|----------|----------|
| Single small project + only Claude Code | `CLAUDE.md` |
| Single small project + only Cursor/Windsurf/Cline/Trae | `AGENTS.md` (generic) + optional native rule file for that tool |
| Code project + multi-agent | `AGENTS.md` as primary + `CLAUDE.md` importing `AGENTS.md` |
| Large/hybrid project | `AGENTS.md` + `CLAUDE.md` + `.claude/rules/*.md` |
| Existing `AGENTS.md` | Write `@AGENTS.md` in `CLAUDE.md`, no duplication; other tool files import `AGENTS.md` |
| Existing `CLAUDE.md` | Extract generic rules into `AGENTS.md`, change `CLAUDE.md` to import `AGENTS.md` |
| Empty project | Minimal `AGENTS.md` (generic) or minimal `CLAUDE.md` (if confirmed Claude only) |

## Agent-to-Artifact Mapping

| Primary Agent | Preferred Artifact | Notes |
|---------------|-------------------|-------|
| Claude Code | `CLAUDE.md` | If other agents exist, add `AGENTS.md` and have `CLAUDE.md` import it |
| Cursor | `AGENTS.md` + optional `.cursor/rules/*.mdc` | Cursor also reads `AGENTS.md`; prefer generic standard |
| Windsurf | `AGENTS.md` + optional `.windsurfrules` | Windsurf also reads `AGENTS.md` |
| Cline / Roo Code | `AGENTS.md` + optional `.clinerules` | Cline ecosystem often shares `.clinerules` |
| GitHub Copilot | `AGENTS.md` + optional `.github/copilot-instructions.md` | Official Copilot file; preferred for team scenarios |
| OpenAI Codex | `AGENTS.md` | Codex native standard |
| Kimi Code | `AGENTS.md` | Kimi Code native standard |
| Devin | `AGENTS.md` | Devin recommended standard |
| Zed | `AGENTS.md` | Zed native preferred |
| Gemini CLI / Firebase Studio | `AGENTS.md` + optional `GEMINI.md` | Gemini also reads `AGENTS.md` |
| Trae | `AGENTS.md` + optional `.trae/rules/*.md` | Trae's own rule format |

Principle: **Prefer `AGENTS.md` as the single source; native files for each tool only import or reference it, without duplicating content.**

## Migrating an Existing CLAUDE.md

When the project already has a `CLAUDE.md` but detection/user selection calls for generating an `AGENTS.md`, process in the following order. **`AGENTS.md` must not reference `CLAUDE.md`**:

1. **Read the old `CLAUDE.md`** and split it into three categories:
   - **Generic rules** (any Agent should follow) → migrate to `AGENTS.md` `Working Rules` / `Verification` / `Safety`
   - **Claude Code-specific instructions** (`@` syntax, `/init`, Claude-specific tool calls, etc.) → keep in the new `CLAUDE.md`
   - **Project facts** (stack, directories, commands) → only write in `AGENTS.md`; `CLAUDE.md` automatically gets them via `@AGENTS.md`
   - **Multi-step processes** → suggest splitting into `.claude/skills/`, do not stuff into context files

2. **Generate a full `AGENTS.md`**:
   - `Working Rules` / `Verification` / `Safety` must be rendered with `tools/render-atoms.py`
   - Must recall and render the atoms corresponding to generic rules from the old `CLAUDE.md`
   - Do not hand-rewrite or compress just because it was "moved from CLAUDE.md"

3. **Rewrite `CLAUDE.md` as a minimal import version**:

   ```md
   # Project Context

   Claude Code: please read `@AGENTS.md` first for general project context.

   ## Claude-specific pointers
   - Multi-step workflows are in `.claude/skills/`
   - Entry commands, stack, and general rules are all in `@AGENTS.md`
   ```

   - The new `CLAUDE.md` only keeps Claude-specific pointers and does not duplicate `AGENTS.md` content
   - Keep line count around 30 lines if possible

4. **No reverse references**:
   - `AGENTS.md` must not contain `@CLAUDE.md` or "see `CLAUDE.md`"
   - Reason: `AGENTS.md` is the single source; Codex/Cursor/Kimi and others reading it must not depend on Claude-specific files

5. **Review-specific checks**:
   - Did all generic rules from the old `CLAUDE.md` make it into `AGENTS.md`?
   - Does the new `CLAUDE.md` contain `@AGENTS.md`?
   - Does `AGENTS.md` not reference `CLAUDE.md`?
   - Are there circular references or duplicate paragraphs?

## Proposal Output Format

Generate the proposal and, after passing review, write it directly to file. User confirmation is not required by default:

```md
## Auto Context Proposal

Detected state: existing project
Primary profile: frontend-product
Secondary profile: coding
Confidence: 0.84
Detected agents: claude-code, cursor

Evidence:
- package.json includes vite, react, typescript
- src/ and components/ exist
- README contains local dev command
- Existing `.cursorrules` and `CLAUDE.md` found

Recommended files:
- Update AGENTS.md (single source, shared across agents)
- Update CLAUDE.md (imports AGENTS.md)
- Create .cursor/rules/frontend.mdc (Cursor-specific UI rules)

Call the script to generate the rules section (must show full output in the proposal):

```bash
python3 tools/render-atoms.py \
  --working-standard read-before-editing,surgical-changes \
  --verification run-smallest-relevant-test \
  --safety no-destructive-git \
  --output /tmp/rendered-rules.md
```

Paste the full contents of `/tmp/rendered-rules.md` directly into the preview below. Do not omit or use placeholders.

**Working Rules** / **Verification** / **Safety preview:**
```markdown
## Working Rules
- **Read relevant files before changing them.** [read-before-editing]
  - Before modifying a file:
  - Read the target file and its immediate context.
  - ...

## Verification
- **Run the smallest relevant test first.** [run-smallest-relevant-test]
  - ...

## Safety
- **Do not run destructive git commands unless explicitly requested.** [no-destructive-git]
  - ...
```

Project facts (for Project Overview / Commands / Reference Docs):
- Stack: TypeScript, React, Vite
- Commands: `npm install`, `npm run dev`, `npm test`
- Key docs: `README.md`, `docs/architecture.md`
- Existing agent configs: `.cursorrules`

Omitted guidelines:
- `do-not-guess-schema` — no SQL / data files
- `check-data-grain` — no data pipeline signals

Reason:
- Project needs both implementation guardrails and UI-quality expectations.
- Frontend-specific rules should be scoped separately to avoid bloating CLAUDE.md.
- Detected both Claude Code and Cursor, so use AGENTS.md as single source.
```
