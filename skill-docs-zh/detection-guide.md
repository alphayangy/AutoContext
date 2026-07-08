# 检测指南

AutoContext Step 1 的详细参考：扫描工作区并检测项目信号。

## 快速扫描步骤

1. **一次拿到目录结构**

   ```bash
   tree -L 2 -I 'node_modules|.git|.venv|venv|__pycache__|dist|build|target|.next|.nuxt|coverage|*.pyc'
   ```

   如果 `tree` 不可用，用等价的 `find` 命令，但只取两层。

2. **挑高信号文件读前 30 行**

   按优先级读取以下文件，不确定时跳过，不读大文件：

   - `README*`、`README.md`、`README.zh.md`
   - `package.json`、`pyproject.toml`、`go.mod`、`Cargo.toml`、`pom.xml`、`requirements.txt`
   - `Makefile`、`justfile`、`docker-compose.yml`、`Dockerfile`
   - 入口脚本：`run.sh`、`main.py`、`batch_infer.py`、`src/main.*` 等
   - 已有 agent 配置文件：`CLAUDE.md`、`AGENTS.md`、`.cursorrules`、`.cursor/rules/*.mdc`、`.windsurfrules` 等

3. **统计信号（只看文件名和路径，不看内容）**

   - 可执行代码：`*.py`、`*.go`、`*.rs`、`*.ts`、`*.js`、`*.sh`、`Makefile`、`Snakefile`
   - 数据文件：`*.sql`、`*.ipynb`、`*.parquet`、`*.csv`、`*.xlsx`、`dbt_project.yml`
   - 配置文件：`*.toml`、`*.yaml`、`*.yml`、`*.json`
   - 文档/资料：`docs/`、`references/`、`papers/`、`*.md`

## 输出字段

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

- `workspace_state`：空目录 / 已有项目 / 部分项目（只有少量文件）。
- `detected_stack`：从依赖和文件推断的技术栈，不确定时不填。
- `commands`：从 `package.json` scripts、`Makefile`、`README` 提取，不确定时标 `TBD`。
- `existing_context`：已存在的 agent 上下文文件。
- `detected_agents`：根据已有配置文件推断的用户 Agent 列表。
- `confidence`：主 Profile 的置信度。

## 检测用户使用的 Agent 产品

| 检测到的文件 | 推断的 Agent |
|-------------|-------------|
| `CLAUDE.md` / `.claude/CLAUDE.md` | Claude Code |
| `.cursorrules` / `.cursor/rules/*.mdc` | Cursor |
| `.windsurfrules` / `.windsurf/rules/*.md` | Windsurf |
| `.clinerules` / `.clinerules/*.md` | Cline / Roo Code |
| `.trae/rules/*.md` | Trae |
| `GEMINI.md` / `.idx/airules.md` | Gemini CLI / Firebase Studio |
| `.github/copilot-instructions.md` / `.github/agents/*.agent.md` | GitHub Copilot |
| `AGENTS.md` | 通用标准（Codex / Copilot / Devin / Kimi Code / Zed / Aider 等） |
| `.kimi-code/` 或 `~/.kimi-code/AGENTS.md` | Kimi Code |

### 检测规则

1. **强信号优先**：项目里存在某 Agent 专属文件，就直接判定该 Agent 被使用。
2. **AGENTS.md 是跨工具信号**：单独存在 `AGENTS.md` 时，视为“多 agent / 通用标准”场景。
3. **多 Agent 共存**：如果同时检测到 `CLAUDE.md` + `AGENTS.md` + `.cursorrules`，`detected_agents` 应包含多个，走多 agent 产物策略。
4. **无信号时直接问**：如果项目没有任何 agent 配置文件，问：

   > 你主要用哪个 AI coding 工具？
   > - A. Claude Code
   > - B. Cursor / Windsurf / Cline / Trae 等 IDE 内置 Agent
   > - C. GitHub Copilot / OpenAI Codex / Kimi Code 等 CLI Agent
   > - D. 多个工具混用

5. **默认回退**：用户未回答且无信号时，默认生成 `AGENTS.md`（通用性最好）；如果环境能识别当前运行的是 Claude Code，可默认 `CLAUDE.md`。
