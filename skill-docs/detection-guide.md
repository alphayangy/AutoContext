# Detection Guide

Detailed reference for AutoContext Step 1: scanning the workspace and detecting project signals.

## Quick Scan Steps

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

## Output Fields

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
- `detected_agents`: Inferred list of user Agents based on existing config files.
- `confidence`: Confidence of the primary profile.

## Detect Which Agent Product the User Uses

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

### Detection Rules

1. **Strong signals first**: If an Agent-specific file exists in the project, directly judge that Agent as in use.
2. **AGENTS.md is a cross-tool signal**: When `AGENTS.md` exists alone, treat it as a "multi-agent / generic standard" scenario.
3. **Multiple Agents coexist**: If `CLAUDE.md` + `AGENTS.md` + `.cursorrules` are detected simultaneously, `detected_agents` should include multiple entries and follow the multi-agent artifact strategy.
4. **Ask directly when there are no signals**: If the project has no agent config files, ask:

   > Which AI coding tool do you mainly use?
   > - A. Claude Code
   > - B. Cursor / Windsurf / Cline / Trae and other IDE-embedded Agents
   > - C. GitHub Copilot / OpenAI Codex / Kimi Code and other CLI Agents
   > - D. Multiple tools mixed

5. **Default fallback**: If the user does not answer and there are no signals, default to generating `AGENTS.md` (best generality); if the environment can identify that the current run is Claude Code, default to `CLAUDE.md`.
