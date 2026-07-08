---
name: auto-context
description: Use before starting, onboarding, or recalibrating any project. Scans the workspace or interviews the user, identifies the project scenario, composes guideline atoms, and generates a reviewable CLAUDE.md, AGENTS.md, or .claude/rules/ context pack.
---

# Auto Context

Project onboarding skill + Context Compiler. Use before starting or while working on a project to identify the project scenario, compose guideline atoms, and generate a minimal but effective context file.

## When to Use

- Initialize a new project
- Add context to an existing project
- Feel the existing `CLAUDE.md` is inaccurate or outdated and want to recalibrate

## Core Flow

```text
Detect -> Determine Profile -> (if necessary) Ask Questions -> Recall Atoms -> Compose -> Render Proposal -> Self-Review -> Write
```

When executing, strictly follow [`references/meta-rules.md`](references/meta-rules.md) (AutoContext's own meta-rules), especially M7 "Would deleting this line cause a mistake?" and M8 "CLAUDE.md < 200 lines".

---

## Step 1: Detect Project (Detect)

Scan high-signal files and output structured detection results. **First use `tree` to quickly get the directory skeleton, then pick key files and read the first 30 lines. Do not `ls` directories one by one, and do not read whole files.**

### 1.1 Quick Scan Steps

1. **Get the directory structure in one shot**
   ```bash
   tree -L 2 -I 'node_modules|.git|.venv|venv|__pycache__|dist|build|target|.next|.nuxt|coverage|*.pyc'
   ```
   If `tree` is not available, use an equivalent `find` command, but only take two levels.

2. **Read the first 30 lines of high-signal files**
   Read the following files in priority order. Skip uncertain ones and do not read large files:
   - `README*`, `README.md`, `README.zh.md`
   - `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `requirements.txt`
   - `Makefile`, `justfile`, `docker-compose.yml`, `Dockerfile`
   - Entry scripts: `run.sh`, `main.py`, `batch_infer.py`, `src/main.*`, etc.
   - Existing agent config files: `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.cursor/rules/*.mdc`, `.windsurfrules`, etc.

3. **Count signals (only filenames and paths, not content)**
   - Executable code: `*.py`, `*.go`, `*.rs`, `*.ts`, `*.js`, `*.sh`, `Makefile`, `Snakefile`
   - Data files: `*.sql`, `*.ipynb`, `*.parquet`, `*.csv`, `*.xlsx`, `dbt_project.yml`
   - Config files: `*.toml`, `*.yaml`, `*.yml`, `*.json`
   - Docs/materials: `docs/`, `references/`, `papers/`, `*.md`

### 1.2 Output Fields

```json
{
  "workspace_state": "empty | existing | partial",
  "detected_stack": ["typescript", "react", "vite"],
  "important_dirs": ["src", "tests", "docs"],
  "commands": {
    "install": "npm install",
    "run": "npm run dev",
    "test": "npm test",
    "build": "npm run build"
  },
  "existing_context": ["CLAUDE.md", "AGENTS.md"],
  "detected_agents": ["claude-code", "cursor"],
  "profile_scores": [
    {"profile": "frontend-product", "score": 0.84, "evidence": ["package.json", "src/App.tsx", "vite.config.ts"]}
  ],
  "confidence": 0.84,
  "questions": []
}
```

- `workspace_state`: Empty directory / existing project / partial project (only a few files).
- `detected_stack`: Inferred stack from dependencies and files. Leave blank if uncertain.
- `commands`: Extracted from `package.json` scripts, `Makefile`, `README`. Mark `TBD` if uncertain.
- `existing_context`: Existing agent context files.
- `detected_agents`: Inferred list of user Agents based on existing config files, e.g. `["claude-code", "cursor"]`.
- `confidence`: Confidence of the primary profile.

### 1.3 Detect Which Agent Product the User Uses

In addition to scanning the project's context files, map files to specific Agents and output `detected_agents`:

| Detected File | Inferred Agent |
|---------------|----------------|
| `CLAUDE.md` / `.claude/CLAUDE.md` | Claude Code |
| `.cursorrules` / `.cursor/rules/*.mdc` | Cursor |
| `.windsurfrules` / `.windsurf/rules/*.md` | Windsurf |
| `.clinerules` / `.clinerules/*.md` | Cline / Roo Code |
| `.trae/rules/*.md` | Trae |
| `GEMINI.md` / `.idx/airules.md` | Gemini CLI / Firebase Studio |
| `.github/copilot-instructions.md` / `.github/agents/*.agent.md` | GitHub Copilot |
| `AGENTS.md` | Generic standard (Codex / Copilot / Devin / Kimi Code / Zed / Aider, etc.) |
| `.kimi-code/` or `~/.kimi-code/AGENTS.md` | Kimi Code |

#### Detection Rules

1. **Strong signals first**: If an Agent-specific file exists in the project, directly judge that Agent as in use.
2. **AGENTS.md is a cross-tool signal**: When `AGENTS.md` exists alone, treat it as a "multi-agent / generic standard" scenario.
3. **Multiple Agents coexist**: If `CLAUDE.md` + `AGENTS.md` + `.cursorrules` are detected simultaneously, `detected_agents` should include multiple entries and follow the multi-agent artifact strategy.
4. **Ask directly when there are no signals**: If the project has no agent config files, fold Agent selection into Question 1 or ask separately:

   > Which AI coding tool do you mainly use?
   > - A. Claude Code
   > - B. Cursor / Windsurf / Cline / Trae and other IDE-embedded Agents
   > - C. GitHub Copilot / OpenAI Codex / Kimi Code and other CLI Agents
   > - D. Multiple tools mixed

5. **Default fallback**: If the user does not answer and there are no signals, default to generating `AGENTS.md` (best generality); if the environment can identify that the current run is Claude Code, default to `CLAUDE.md`.

---

## Step 2: Determine Profile (Classify)

Judge the project type based on scan signals. MVP supports one primary profile and optionally one secondary profile.

### 2.1 Profile Signal Table

| Profile | Strong Signals | Weak Signals |
|---------|----------------|--------------|
| `coding` | `pyproject.toml` + `src/` + `tests/`; `go.mod` + `main.go`; `Cargo.toml`; **many executable scripts** (`*.py`, `*.sh`, `Makefile`, `Snakefile`) + inference/pipeline semantic filenames (e.g. `batch_infer.py`, `run.sh`, `inference/`, `pipeline/`) | `package.json` + CLI/library structure; a few Python scripts without standard structure |
| `frontend-product` | `package.json` + `app/`/`pages/` + `components/` + UI framework | Pure `package.json` but no UI directories |
| `product-design` | `PRD.md`, `docs/PRD*`, lots of product docs | Has `docs/` but no PRD |
| `research` | `papers/`, `references/`, lots of PDF/Markdown notes, `*.tex` | Few reference materials |
| `writing-docs` | Mainly `docs/` and no code dependencies, or explicit writing goal | Docs attached to a code repo |
| `data-analysis` | `*.ipynb`, `dbt_project.yml`, `.dbt/`, clearly analytical README | Standalone `*.sql`, `*.parquet`, `*.csv`, `*.xlsx` (these are just data inputs, not analysis goals) |
| `creative-media` | `remotion.config.*`, media assets, script directories | Scattered media files |

### 2.2 Confidence Rules

- `0.80 - 1.00`: Direct recommendation, may skip Question 1.
- `0.50 - 0.79`: Recommend + ask 1-2 questions.
- `0.00 - 0.49`: Enter empty-project/uncertain Q&A flow.

### 2.3 Avoid Misclassification

- Don't be overconfident when there are few files.
- When `README` and dependencies conflict, prioritize asking the user's goal.
- Having `docs/` does not necessarily mean a writing project; having `package.json` does not necessarily mean frontend.
- **Executable scripts take priority over data files**: If the project has many `*.py` / `*.sh` / `Makefile` / `Snakefile` / `batch_infer*` / `run.sh` / `inference*` and other execution or pipeline files, even if there are also many `.sql` / `.parquet` / `.csv`, prioritize `coding`; data-related atoms are only auxiliary recalls.
- **SQL files themselves are not analysis goals**: `.sql` in an inference pipeline is usually just a data extraction step; existing alone is not enough to pull the primary profile toward `data-analysis`.

---

## Step 3: Ask Questions (Ask, only when low confidence)

Ask at most 2 questions, each with at most 3 options. Do not ask when confidence is high.

### Question 1: What type of work do you mainly want the agent to do next?

- **A. Modify the project** (leaning toward coding / frontend-product / data-analysis / creative-media)
- **B. Understand the project** (leaning toward research / product-design / architecture-review / context-update)
- **C. Produce materials** (leaning toward writing-docs / product-design / research / creative-media)

### Question 2: Which kind of information do you least want to explain repeatedly?

- **A. Project facts** (goals, directories, stack, commands, data tables, key materials)
- **B. Work standards** (code rules, product judgment, UI quality, research evidence, data definitions)
- **C. Output formats** (document structure, citation format, SQL output, design report conventions)

If scan signals are strong, only ask Question 2; if context files already exist, review them first, then ask which repeated explanation the user most wants to reduce.

---

## Step 4: Recall Guideline Atoms

Read `guidelines/**/*.md` and filter by frontmatter. **After selecting atoms, you must actually invoke `tools/render-atoms.py` to render the rules sections, and paste the script's full output into the proposal. Placeholders are forbidden.**

### 4.0 Use the Rendering Script (must run)

To prevent the LLM from unconsciously rewriting, compressing, or losing atom source text, the rules sections (`Working Rules` / `Verification` / `Safety`) **must** be generated deterministically by `tools/render-atoms.py`. You may not write rule content directly, nor use placeholders like `[rendered content]` or `<!-- to be rendered -->`.

Run command:

```bash
python3 tools/render-atoms.py \
  --working-standard <atom1>,<atom2> \
  --verification <atom3>,<atom4> \
  --safety <atom5> \
  --output /tmp/rendered-rules.md
```

Then read the contents of `/tmp/rendered-rules.md` and **paste it in full** into the proposal.

- The script reads atom files and outputs the core sentence + expansion verbatim.
- The script only generates the rules sections; `Project Overview`, `Commands`, and `Reference Docs` are still handwritten by you based on Step 1 detection results.
- If `tools/render-atoms.py` is not found, first locate the skill root: `find ~/.claude/skills/auto-context -name render-atoms.py` or `find . -name render-atoms.py`.

**Showing a proposal without actually invoking the script is equivalent to an incomplete output.**

### 4.1 Recall Rules

1. **Universal atom**: `profiles: [all]` -> recall all.
2. **Profile atom**: `profiles` contains the primary or secondary profile -> recall.
3. **Trigger secondary filtering**: When `triggers.files` exists, do not recall if the project has no corresponding files.
4. **User intent filtering**: When `triggers.user_intents` exists, do not recall if it does not match the user's answer.

### 4.2 Reading Content

Each atom file contains:
- Frontmatter: `name`, `description`, `profiles`, `scopes`, `priority`, `triggers`, `conflicts`
- Body: bold core sentence + expansion + acceptance sentence

**The rules sections are rendered by `tools/render-atoms.py`; do not hand-edit them.** The script will:
- Output the core sentence verbatim
- Output all bullets and lead-in text of the expansion verbatim
- Not output the acceptance sentence (`This is working if:` is only used for Review verification)

Your only job is to decide which section each atom goes into (`Working Rules` / `Verification` / `Safety`), then hand it to the script.

### 4.3 Do Not Rewrite Atom Source (hard rule)

Entries in `Working Rules` / `Verification` / `Safety` **must come directly from atom files**, following these rules:

- **Must be rendered through `tools/render-atoms.py`**. Do not handwrite, do not copy-paste then modify, and do not let the LLM rephrase.
- **Allowed**: spaces and bullet markers added by the script for formatting indentation.
- **Forbidden**:
  - Rewriting the semantics of the core sentence
  - Adding explanations, examples, or project details not in the atom
  - Deleting or merging expansion bullets
  - Mashing multiple atoms into one new rule

**If an atom's content is not suitable for direct rendering, you selected the wrong atom.** Omit that atom or choose a more suitable one, rather than rewriting it.

During Review, the script output and atom source will be `diff`ed; any non-whitespace difference is treated as rewriting.

---

## Step 5: Compose (Compose)

Combine detected facts, user answers, and recalled atoms into a candidate set, then sort and deduplicate.

### 5.1 Compose Steps

1. **Separate the two types of content** (must be clearly distinguished, never mixed):
   - **Project Facts**: From Step 1 detection, including stack, directories, commands, existing context files, and key document locations. Project facts only go into the `Project Overview`, `Commands`, and `Reference Docs` sections.
   - **Guideline Atoms**: From Step 4 recall, only go into the `Working Rules`, `Verification`, and `Safety` sections.
2. **Render the rules sections**: Group selected atom names by section, invoke `tools/render-atoms.py`, and get deterministic rules markdown.
3. **Sort by priority**: `high` > `medium` > `low`. Sorting is done before invoking the script; the script outputs in the order you give.
4. **Deduplicate**: Keep only one of synonymous or same-goal atoms, and record merged items.
5. **Resolve conflicts**: If an atom declares `conflicts`, keep only the more relevant or higher-priority one.
6. **Strictly limit omissions**:
   - Atoms with `priority: high` are **not omitted by default**.
   - Atoms with `profiles: [all]` are **not omitted by default**.
   - Omitting an atom must be supported by specific evidence: "If we delete it, the agent will make a mistake in [specific scenario]", not "it doesn't look critical" or "the global file already covers it".
   - **A global `~/.claude/CLAUDE.md` is never a reason to omit**.
   - **You may not omit one of two atoms just because they "look overlapping"**; only resolve conflicts when the frontmatter explicitly declares `conflicts`.
7. **Check meta-rules**: Ensure no violation of M7/M8 (every line valuable, < 200 lines).

### 5.2 Strictly Forbid Process Leakage

The following content is **process/skill** and **must not** be written into `CLAUDE.md` / `AGENTS.md` / any agent context file:

- Multi-step operation manuals (e.g. "dry-run -> check output -> then run production")
- Prompt engineering iteration processes
- Experiment logging / experiment report writing processes
- Code review processes
- Deployment/release processes
- Any sequential instructions requiring 3 or more steps

If these already exist in project docs (README, Cursor Skill, internal wiki), **only give a one-line pointer in `Reference Docs`**, e.g.:

```md
## Reference Docs (read when relevant)
- `docs/deployment.md` — deployment process
- `.cursor/skills/experiment-logging/` — experiment logging skill
```

If the project **does not** have relevant docs, do not casually write one in the context file. Instead, suggest the user make it a `.claude/skills/` or `.cursor/skills/`.

### 5.2 Output

```json
{
  "selected_guidelines": ["read-before-editing", "small-scoped-changes", "run-smallest-relevant-test"],
  "artifact_targets": ["CLAUDE.md"],
  "omitted_guidelines": ["verify-rendered-ui: no frontend files"]
}
```

---

## Step 6: Select Artifacts and Render Proposal

### 6.1 Artifact Selection

Artifact selection is determined by `detected_agents` and project scale:

| Scenario | Artifact |
|----------|----------|
| Single small project + only Claude Code | `CLAUDE.md` |
| Single small project + only Cursor/Windsurf/Cline/Trae | `AGENTS.md` (generic) + optional native rule file for that tool |
| Code project + multi-agent | `AGENTS.md` as primary + `CLAUDE.md` importing `AGENTS.md` |
| Large/hybrid project | `AGENTS.md` + `CLAUDE.md` + `.claude/rules/*.md` |
| Existing `AGENTS.md` | Write `@AGENTS.md` in `CLAUDE.md`, no duplication; other tool files import `AGENTS.md` |
| Existing `CLAUDE.md` | Extract generic rules into `AGENTS.md`, change `CLAUDE.md` to import `AGENTS.md`; see [6.1.1 Migrating an Existing CLAUDE.md](#611-migrating-an-existing-claudemd) |
| Empty project | Minimal `AGENTS.md` (generic) or minimal `CLAUDE.md` (if confirmed Claude only) |

#### Agent-to-Artifact Mapping

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

#### 6.1.1 Migrating an Existing CLAUDE.md

When the project already has a `CLAUDE.md` but detection/user selection calls for generating an `AGENTS.md` (multi-agent, generic standard, or user explicitly requests), process in the following order. **`AGENTS.md` must not reference `CLAUDE.md`**:

1. **Read the old `CLAUDE.md`** and split it into three categories:
   - **Generic rules** (any Agent should follow) -> migrate to `AGENTS.md` `Working Rules` / `Verification` / `Safety`
   - **Claude Code-specific instructions** (`@` syntax, `/init`, Claude-specific tool calls, etc.) -> keep in the new `CLAUDE.md`
   - **Project facts** (stack, directories, commands) -> only write in `AGENTS.md`; `CLAUDE.md` automatically gets them via `@AGENTS.md`
   - **Multi-step processes** -> suggest splitting into `.claude/skills/`, do not stuff into context files

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

### 6.2 CLAUDE.md / AGENTS.md Structure

Both files use the same section structure. `AGENTS.md` is the single source; `CLAUDE.md` only imports it and adds Claude-specific pointers.

```md
# Project Context

## Project Overview
- Workspace state: existing project
- Primary profile: frontend-product
- Detected agents: claude-code, cursor
- Detected stack: TypeScript, React, Vite
- Important directories: src/, tests/, docs/
- Existing agent configs: .cursor/skills/, .claude/memory-graph/

## Commands
- Install: npm install
- Run: npm run dev
- Test: npm test
- Build: npm run build

## Working Rules
- **Read relevant files before changing them.** [read-before-editing]
  - Before modifying a file:
  - Read the target file and its immediate context.
  - Trace how the code is called and what depends on it.
  - Check existing patterns, naming, and conventions in the same area.
  - If unsure how something works, read it first. Don't guess.

- **Make the smallest change that solves the problem.** [surgical-changes]
  - When editing existing code:
  - Don't "improve" adjacent code, comments, or formatting.
  - Don't refactor things that aren't broken.
  - Match existing style, even if you'd do it differently.
  - If you notice unrelated dead code, mention it. Don't delete it.
  - When your changes create orphans:
  - Remove imports, variables, or functions that YOUR changes made unused.
  - Don't remove pre-existing dead code unless asked.

## Verification
- **Run the smallest relevant test first.** [run-smallest-relevant-test]
  - Before claiming a change works, run the smallest test that exercises it.
  - Prefer focused unit or integration tests over manual end-to-end runs.
  - If no test exists, create the smallest reproduction before fixing.

## Safety
- **Do not run destructive git commands unless explicitly requested.** [no-destructive-git]
  - No `git reset --hard`, `git clean -fd`, force-push, or branch deletion without confirmation.

## Reference Docs (read when relevant)
- `README.md` — project background
- `docs/architecture.md` — architecture design

## When to Update This File
- Add new stack/tool after it stabilizes.
- Move path-specific rules to .claude/rules/.
- Move multi-step workflows to .claude/skills/.
```

#### Source of Each Section

| Section | Source | Example |
|---------|--------|---------|
| `Project Overview` | Detection results | workspace state, profile, stack, dirs, existing agent configs |
| `Commands` | Detection results | install / run / test / build |
| `Working Rules` | **`tools/render-atoms.py` output** | `--working-standard read-before-editing,surgical-changes` |
| `Verification` | **`tools/render-atoms.py` output** | `--verification run-smallest-relevant-test` |
| `Safety` | **`tools/render-atoms.py` output** | `--safety no-destructive-git` |
| `Reference Docs` | Pointers to key detected docs | `README.md`, `docs/...`, existing skill directories |
| `When to Update` | Fixed template | update after stabilization, move path rules to `.claude/rules/`, move workflows to `.claude/skills/` |

**Every entry in Working Rules / Verification / Safety must satisfy:**
1. **Source**: Rendered directly from atom files by `tools/render-atoms.py`, without LLM rewriting.
2. **Format**: Core sentence as a top-level bullet, expansion as indented content (preserving atom structure).
3. **Annotation**: Append `[atom-name]` at the end of the core sentence.
4. **Verifiable**: During Review, `diff` the script output against the atom source; they must be identical (except for indentation and bullet markers).

**Bad example (hand-rewritten)**:
```md
- Touch only what you must. `[surgical-changes]`
```
Problem: No expansion, and the core sentence was rewritten.

**Good example (script output)**:
```md
- **Touch only what you must. Clean up only your own mess.** `[surgical-changes]`
  - When editing existing code:
  - Don't "improve" adjacent code, comments, or formatting.
  - Don't refactor things that aren't broken.
  - Match existing style, even if you'd do it differently.
  - If you notice unrelated dead code, mention it. Don't delete it.
  - When your changes create orphans:
  - Remove imports, variables, or functions that YOUR changes made unused.
  - Don't remove pre-existing dead code unless asked.
```

### 6.3 Proposal Output Format

Generate the proposal and, after passing Step 6.5 Review, write it directly to file. User confirmation is not required by default:

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

Paste the full contents of `/tmp/rendered-rules.md` directly into the preview below. **Do not omit or use placeholders.**

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

---

## Step 6.5: Self-Review (mandatory self-check before writing)

Before writing the proposal to files, perform a self-review. **Do not skip it.**

### 6.5.1 Review Checklist

Check the generated `AGENTS.md` / `CLAUDE.md` / `.claude/rules/*.md` item by item:

| # | Check Item | Pass Criteria | If Not Passed |
|---|------------|---------------|---------------|
| 1 | **Atom source traceable** | Every entry in `Working Rules` / `Verification` / `Safety` ends with `[atom-name]` | Delete unsourced entries or add atom annotations |
| 2 | **Script actually invoked** | `Working Rules` / `Verification` / `Safety` in the proposal are real output from `tools/render-atoms.py`, with no `[rendered content]` / `<!-- to be rendered -->` / ellipsis placeholders | Invoke the script and paste the full output into the proposal |
| 3 | **No atom rewriting** | `diff` script output against atom source; identical except for indentation and bullet markers | Revert to atom source; if atom source is unsuitable, omit that atom |
| 4 | **Expansion fully preserved** | Every rule has core sentence + indented expansion; no one-line slogans | Restore atom expansion; re-invoke the script to re-render |
| 5 | **No process leakage** | No "first X, then Y, finally Z" multi-step processes; no numbered steps 1/2/3 | Move to a one-line `Reference Docs` pointer, or suggest making it a skill |
| 6 | **No project facts mixed into Working Rules** | Working Rules do not contain specific commands, directory paths, filenames, or tool parameters | Move project facts to `Project Overview` / `Commands` / `Reference Docs` |
| 7 | **No excessive omissions** | Atoms with `priority: high` and `profiles: [all]` are not omitted; omission reason is not "global already covers" or "looks overlapping" | Add back atoms that should not have been omitted |
| 8 | **Length compliant** | Each file ≤ 200 lines | Split into `.claude/rules/`, or trim low-priority atoms |
| 9 | **No placeholders** | No `[TBD]`, `[to be filled]`, empty brackets, or other unfilled content | Delete or complete; mark `[UNVERIFIED]` with explanation if impossible to complete |
| 10 | **No conflicting rules** | No contradictory instructions (e.g. "always do X" vs. "never do X") | Keep the more relevant/higher-priority one and delete the other |
| 11 | **Agent artifact match** | Generated files match `detected_agents` (Claude -> CLAUDE.md, multi-agent -> AGENTS.md primary) | Re-select artifacts per Step 6.1 |
| 12 | **Project facts accurate** | Stack, directories, and commands in `Project Overview` / `Commands` match scanned files | Go back to Step 1 and re-detect |
| 13 | **No large README copy-paste** | No whole paragraphs copied from `README.md` into the context file | Replace with a one-line summary or pointer |
| 14 | **No lint/format rules in prose** | No ESLint/Prettier/black formatting rules written as long natural-language paragraphs | Delete; rely on the project's existing linter |
| 15 | **Context file reference direction correct** | If both `CLAUDE.md` and `AGENTS.md` exist: `CLAUDE.md` references `AGENTS.md`, `AGENTS.md` does not reference `CLAUDE.md`; verified by `tools/verify-context.py` | Fix reference direction per Step 6.1.1, then run the script to verify |

#### Spot Check (must run)

Spot-check the atom output rendered by the script:

1. Randomly sample 3 rendered atoms.
2. Use `diff` (or re-invoke `tools/render-atoms.py` for that atom alone) to compare script output with atom source.
3. Core sentence + expansion must be identical, except for the following allowed items:
   - Leading indentation spaces
   - Bullet markers `-` / `*`
   - Trailing whitespace
4. Any non-allowed difference -> judged as **atom rewriting**, Review fails.

#### Review Must Not Be All ✅

**Any proposal can find at least one improvement.** If all 15 Review items are ✅, the Review was too lenient. You must find at least one:

- An atom that could be deleted (M7: deleting it would not cause a mistake)
- A phrasing that could be closer to the atom source
- An expansion that could be restored or compressed more accurately
- A project fact that could be changed to a shorter pointer
- A section that could be split into `.claude/rules/`

Write at least one improvement into the Review output.

### 6.5.2 Review Output Format

Append the self-review results after the proposal:

```md
---

## Auto Context Review

| Check Item | Status | Note |
|------------|--------|------|
| Atom source traceable | ✅ | 8/8 entries annotated with `[atom-name]` |
| No process leakage | ⚠️ | `Pipeline discipline` contains a 4-step process, needs removal |
| Length compliant | ✅ | AGENTS.md ~48 lines, CLAUDE.md ~12 lines |
| No conflicting rules | ✅ | No conflicts found |

### Issues to Fix

1. **Process leakage**: The `## Working Standards` `Pipeline discipline` is a 4-step operation process, not an atom. Change to:
   ```md
   ## Reference Docs (read when relevant)
   - `user_memory_inference/README.md` — production inference run process
   ```

2. **Missing atom source**: The `Prompt Engineering` subsection has no `[atom-name]` and its content comes from README. Delete or change to a Reference Docs pointer.

### Corrected File Preview

[Put the corrected AGENTS.md / CLAUDE.md preview here]
```

### 6.5.3 Handling Review Failure

- **Atom rewriting found**: Must revert to atom source. If the atom source is genuinely unsuitable for this project, omit that atom instead of rewriting it.
- **1-2 minor issues found** (process leakage, project fact in wrong place, individual atom wrongly selected): Fix directly without re-asking the user.
- **Structural issues found** (wrong artifact selection, large process leakage, wrong profile, excessive omissions): Fix and regenerate the proposal, then re-Review.
- **Review table all ✅**: Send back for re-review; must find at least one improvement.
- **Uncertain whether it counts as leakage/rewriting**: Handle conservatively — "Is this sentence from the atom file?" If not, delete or change it.

---

## Step 7: Write (Write, default auto-commit to disk)

### 7.1 Write Rules

- **Write directly by default**: `auto-context` is a deterministic tool flow. After generating a proposal and passing Step 6.5 Review, write it to files directly without waiting for the user to say "write" or confirm.
- **Do not write when Review fails**: If Review finds atom rewriting, placeholders, process leakage, etc., fix first, then write; if unfixable, report the issue to the user and do not write a half-finished product.
- **Do not overwrite existing files**: When `CLAUDE.md` / `AGENTS.md` already exist, generate a patch / review instead of overwriting directly.
- Multi-agent scenario: Use `AGENTS.md` as the single source; `CLAUDE.md` only imports, without duplicating content.
- Perform a final lint before writing (subset of Step 6.5 Review, run through one last time):
  - Is the file > 200 lines?
  - Does it contain unfilled placeholders?
  - Did `Working Rules` / `Verification` / `Safety` actually invoke `tools/render-atoms.py`? (Check the proposal for script invocation record and full output.)
  - Is every entry in `Working Rules` / `Verification` / `Safety` annotated with `[atom-name]`?
  - Were multi-step processes stuffed into `CLAUDE.md` / `AGENTS.md`? (Check for "first X, then Y, finally Z" style sequential steps.)
  - Are project facts or operation processes mixed into `Working Rules` / `Verification` / `Safety`?
  - Are there conflicting rules?
  - **Did you run `python3 tools/verify-context.py`?** If generating both `CLAUDE.md` and `AGENTS.md`, you must verify that `CLAUDE.md` references `AGENTS.md` and `AGENTS.md` does not reference `CLAUDE.md`.

### 7.2 Default Post-Write Message

After writing, tell the user:
- Which files were generated
- When to update them
- If there are `.claude/rules/` or `.claude/skills/` recommendations, list next steps

---

## Meta-Rules (AutoContext's Own)

When executing this skill, you must also follow:

1. **Generate less, not more**: Don't invent undetected project facts; don't recall unnecessary atoms.
2. **Review before writing**: Generate a proposal and write directly after Review by default; do not write when Review fails.
3. **Do not overwrite existing files**: Existing context files go through review/patch mode.
4. **CLAUDE.md < 200 lines**: When exceeded, split into `.claude/rules/` instead of making the file longer.
5. **Profile is a recall dimension, not an artifact**: Do not write the Profile name into the final `CLAUDE.md`.
6. **Processes don't go into CLAUDE.md**: Multi-step processes should be suggested as `.claude/skills/`, not stuffed into project context files.
7. **Same rule in one place only**: Do not duplicate it in both `CLAUDE.md` and `AGENTS.md`.
8. **Detect Agent before selecting artifact**: Decide output files based on `detected_agents`, do not default to `CLAUDE.md` for every project.
9. **Multi-agent uses AGENTS.md as single source**: Native files for each tool only import / reference `AGENTS.md`, without copying content.
10. **Project facts and atoms must be separated**: Project facts only go into `Project Overview` / `Commands` / `Reference Docs`; atoms only go into `Working Rules` / `Verification` / `Safety`.
11. **Global CLAUDE.md does not exempt project atoms**: When a global `~/.claude/CLAUDE.md` is detected, do not omit universal atoms for this project because of it. Global is user preference; project is project constraint; they are not mutually exclusive.
12. **Self-review before writing**: After every proposal generation, run the Step 6.5 Review checklist. If it fails, fix and then write; do not write problematic files directly to disk.
13. **Atom rewriting is forbidden**: `Working Rules` / `Verification` / `Safety` must be rendered by `tools/render-atoms.py`; LLM hand-rewriting, compressing, or rephrasing is not allowed.
14. **High-priority atoms kept by default**: Atoms with `priority: high` and `profiles: [all]` are not casually omitted. Omission must provide evidence of "what specific error would occur if not kept."
15. **Review must spot-check**: Randomly sample 3 rendered atoms and `diff` the script output against atom source. Core sentence + expansion must be identical (except indentation and bullet markers).
16. **Review must not be all ✅**: Any proposal has at least one improvement. All ✅ means the Review was too lenient and needs re-review.
17. **Rules must include expansion**: `Working Rules` / `Verification` / `Safety` cannot be one-line slogans. Every entry must contain the atom core sentence + indented expansion so the agent knows exactly what to do.
18. **Executable scripts take priority over data files**: When classifying profile, if the project has both `*.py` / `*.sh` / `Makefile` / `Snakefile` / `inference*` / `batch_*` / `run.sh` and other execution or pipeline files, as well as `.sql` / `.parquet` / `.csv` data files, prioritize `coding`; data-related atoms are only auxiliary recalls.
19. **Scan efficiently**: During project detection, use `tree -L 2` once to get the structure, then pick key files and read the first 30 lines. Do not `ls` directories one by one, do not read whole files, and do not use the shell to explore the skill's own file structure.
20. **Rules sections must be rendered by script**: After selecting atoms, invoke `tools/render-atoms.py` to generate `Working Rules` / `Verification` / `Safety`, without hand-assembling.
21. **Placeholders must not replace script output**: `Working Rules` / `Verification` / `Safety` in the proposal must be the script's real output; placeholders like `[rendered content]`, `<!-- to be rendered -->`, ellipses, or shorthand are not allowed.

---

## Optional Extensions

- Run Context Smell detection on existing `CLAUDE.md` (bloat / skill leakage / lint leakage / conflicting instructions).
- Generate `.claude/rules/` splits.
- Support exporting Cursor rules / Windsurf rules (v1.0).
