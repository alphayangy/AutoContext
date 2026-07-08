# Profile Guide

Detailed reference for AutoContext Step 2: classifying the project profile.

## Profile Signal Table

| Profile | Strong Signals | Weak Signals |
|---------|----------------|--------------|
| `coding` | `pyproject.toml` + `src/` + `tests/`; `go.mod` + `main.go`; `Cargo.toml`; many executable scripts (`*.py`, `*.sh`, `Makefile`, `Snakefile`) + inference/pipeline filenames (e.g. `batch_infer.py`, `run.sh`, `inference/`, `pipeline/`) | `package.json` + CLI/library structure; a few Python scripts without standard structure |
| `frontend-product` | `package.json` + `app/`/`pages/` + `components/` + UI framework | Pure `package.json` but no UI directories |
| `product-design` | `PRD.md`, `docs/PRD*`, lots of product docs | Has `docs/` but no PRD |
| `research` | `papers/`, `references/`, lots of PDF/Markdown notes, `*.tex` | Few reference materials |
| `writing-docs` | Mainly `docs/` and no code dependencies, or explicit writing goal | Docs attached to a code repo |
| `data-analysis` | `*.ipynb`, `dbt_project.yml`, `.dbt/`, clearly analytical README | Standalone `*.sql`, `*.parquet`, `*.csv`, `*.xlsx` (these are just data inputs, not analysis goals) |
| `creative-media` | `remotion.config.*`, media assets, script directories | Scattered media files |

## Confidence Rules

- `0.80 - 1.00`: Direct recommendation, may skip Question 1.
- `0.50 - 0.79`: Recommend + ask 1-2 questions.
- `0.00 - 0.49`: Enter empty-project/uncertain Q&A flow.

## Avoid Misclassification

- Don't be overconfident when there are few files.
- When `README` and dependencies conflict, prioritize asking the user's goal.
- Having `docs/` does not necessarily mean a writing project; having `package.json` does not necessarily mean frontend.
- **Executable scripts take priority over data files**: If the project has many `*.py` / `*.sh` / `Makefile` / `Snakefile` / `batch_infer*` / `run.sh` / `inference*` and other execution or pipeline files, even if there are also many `.sql` / `.parquet` / `.csv`, prioritize `coding`; data-related atoms are only auxiliary recalls.
- **SQL files themselves are not analysis goals**: `.sql` in an inference pipeline is usually just a data extraction step; existing alone is not enough to pull the primary profile toward `data-analysis`.
