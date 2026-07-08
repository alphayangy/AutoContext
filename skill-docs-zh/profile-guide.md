# Profile 指南

AutoContext Step 2 的详细参考：判断项目类型。

## Profile 信号表

| Profile | 强信号 | 弱信号 |
|---------|--------|--------|
| `coding` | `pyproject.toml` + `src/` + `tests/`；`go.mod` + `main.go`；`Cargo.toml`；大量可执行脚本（`*.py`、`*.sh`、`Makefile`、`Snakefile`）+ inference/pipeline 语义文件名（如 `batch_infer.py`、`run.sh`、`inference/`、`pipeline/`） | `package.json` + CLI/库结构；少量 Python 脚本 + 无标准结构 |
| `frontend-product` | `package.json` + `app/`/`pages/` + `components/` + UI 框架 | 纯 `package.json` 但无 UI 目录 |
| `product-design` | `PRD.md`、`docs/PRD*`、大量产品文档 | 有 `docs/` 但无 PRD |
| `research` | `papers/`、`references/`、大量 PDF/Markdown 笔记、`*.tex` | 少量参考资料 |
| `writing-docs` | 以 `docs/` 为主且无代码依赖，或明确写作目标 | 代码仓库附带 docs |
| `data-analysis` | `*.ipynb`、`dbt_project.yml`、`.dbt/`、明显分析性 README | 单独的 `*.sql`、`*.parquet`、`*.csv`、`*.xlsx`（这些只是数据输入，不是分析目的） |
| `creative-media` | `remotion.config.*`、媒体资产、脚本目录 | 零散媒体文件 |

## 置信度规则

- `0.80 - 1.00`：直接推荐，可跳过问题 1。
- `0.50 - 0.79`：推荐 + 问 1-2 个问题。
- `0.00 - 0.49`：进入空项目/不确定项目问答流。

## 避免误判

- 文件少时不过度自信。
- `README` 和依赖文件冲突时，优先问用户目标。
- 有 `docs/` 不一定是写作项目；有 `package.json` 不一定是前端。
- **可执行脚本优先于数据文件**：如果项目里有大量 `*.py` / `*.sh` / `Makefile` / `Snakefile` / `batch_infer*` / `run.sh` / `inference*` 等执行或 pipeline 文件，即使同时有很多 `.sql` / `.parquet` / `.csv`，也优先判为 `coding`，数据相关 atom 作为辅助召回。
- **SQL 文件本身不是分析目的**：`.sql` 在 inference pipeline 里通常只是数据提取步骤，单独存在不足以把主 profile 拉成 `data-analysis`。
