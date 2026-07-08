# 产物选择指南

AutoContext Step 6 的详细参考：选择输出文件并渲染 proposal。

## 产物选择

产物选择由 `detected_agents` 和项目规模共同决定：

| 场景 | 产物 |
|------|------|
| 单一小项目 + 只用 Claude Code | `CLAUDE.md` |
| 单一小项目 + 只用 Cursor/Windsurf/Cline/Trae | `AGENTS.md`（通用）+ 该工具原生规则文件（可选） |
| 代码项目 + 多 agent | `AGENTS.md` 为主 + `CLAUDE.md` import `AGENTS.md` |
| 大型/混合项目 | `AGENTS.md` + `CLAUDE.md` + `.claude/rules/*.md` |
| 已有 `AGENTS.md` | `CLAUDE.md` 中写 `@AGENTS.md`，不重复；其他工具文件 import `AGENTS.md` |
| 已有 `CLAUDE.md` | 提取通用规则到 `AGENTS.md`，`CLAUDE.md` 改为 import `AGENTS.md` |
| 空项目 | 最小 `AGENTS.md`（通用）或最小 `CLAUDE.md`（若确认只用 Claude） |

## Agent 与产物映射

| 主要 Agent | 首选产物 | 备注 |
|------------|----------|------|
| Claude Code | `CLAUDE.md` | 若存在其他 agent，加 `AGENTS.md` 并让 `CLAUDE.md` import |
| Cursor | `AGENTS.md` + `.cursor/rules/*.mdc`（可选） | Cursor 也读 `AGENTS.md`，优先通用标准 |
| Windsurf | `AGENTS.md` + `.windsurfrules`（可选） | Windsurf 也读 `AGENTS.md` |
| Cline / Roo Code | `AGENTS.md` + `.clinerules`（可选） | Cline 生态通常共用 `.clinerules` |
| GitHub Copilot | `AGENTS.md` + `.github/copilot-instructions.md`（可选） | Copilot 官方文件，团队场景优先 |
| OpenAI Codex | `AGENTS.md` | Codex 原生标准 |
| Kimi Code | `AGENTS.md` | Kimi Code 原生标准 |
| Devin | `AGENTS.md` | Devin 推荐标准 |
| Zed | `AGENTS.md` | Zed 原生首选 |
| Gemini CLI / Firebase Studio | `AGENTS.md` + `GEMINI.md`（可选） | Gemini 也读 `AGENTS.md` |
| Trae | `AGENTS.md` + `.trae/rules/*.md`（可选） | Trae 自有规则格式 |

原则：**尽量以 `AGENTS.md` 为单源，各工具原生文件只 import 或引用它，不重复内容。**

## 已有 CLAUDE.md 迁移

当项目已有 `CLAUDE.md` 但检测/用户选择要求生成 `AGENTS.md` 时，必须按以下顺序处理，**不能让 `AGENTS.md` 反过来引用 `CLAUDE.md`**：

1. **读取旧 `CLAUDE.md`**，拆成三类内容：
   - **通用规则**（任何 Agent 都该遵守）→ 迁移到 `AGENTS.md` 的 `Working Rules` / `Verification` / `Safety`
   - **Claude Code 专属指令**（`@` 语法、`/init`、Claude-specific 工具调用等）→ 留在新的 `CLAUDE.md`
   - **项目事实**（技术栈、目录、命令）→ 只写在 `AGENTS.md`，`CLAUDE.md` 通过 `@AGENTS.md` 自动获得
   - **多步骤流程** → 建议拆成 `.claude/skills/`，不塞进上下文文件

2. **生成完整 `AGENTS.md`**：
   - `Working Rules` / `Verification` / `Safety` 必须用 `tools/render-atoms.py` 渲染
   - 必须把旧 `CLAUDE.md` 中的通用规则对应 atom 召回并渲染进去
   - 不能因为是“从 CLAUDE.md 搬过来的”就手工改写或压缩

3. **重写 `CLAUDE.md` 为最小 import 版本**：

   ```md
   # Project Context

   Claude Code 请先阅读 `@AGENTS.md` 获取项目通用上下文。

   ## Claude-specific pointers
   - 多步骤工作流见 `.claude/skills/`
   - 项目入口命令、技术栈、通用规则全部在 `@AGENTS.md`
   ```

   - 新的 `CLAUDE.md` 只保留 Claude-specific 指针，不重复 `AGENTS.md` 内容
   - 行数尽量控制在 30 行以内

4. **禁止反向引用**：
   - `AGENTS.md` 里不准出现 `@CLAUDE.md` 或 "详见 `CLAUDE.md`"
   - 原因：`AGENTS.md` 是单源，Codex/Cursor/Kimi 等读到它时不能依赖 Claude-specific 文件

5. **Review 专项检查**：
   - 旧 `CLAUDE.md` 的通用规则是否都进了 `AGENTS.md`？
   - 新 `CLAUDE.md` 是否写了 `@AGENTS.md`？
   - `AGENTS.md` 是否没有引用 `CLAUDE.md`？
   - 是否出现循环引用或重复段落？

## Proposal 输出格式

生成 proposal 并通过 Review 后直接写入文件，默认不需要用户确认：

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
- Update AGENTS.md（单源，跨 agent 共享）
- Update CLAUDE.md（import AGENTS.md）
- Create .cursor/rules/frontend.mdc（Cursor 专属 UI 规则）

调用脚本生成规则 section（必须在 proposal 中展示完整输出）：

```bash
python3 tools/render-atoms.py \
  --working-standard read-before-editing,surgical-changes \
  --verification run-smallest-relevant-test \
  --safety no-destructive-git \
  --output /tmp/rendered-rules.md
```

把 `/tmp/rendered-rules.md` 的完整内容直接粘贴到下面的 preview 中，不要省略、不要用占位符。

**Working Rules** / **Verification** / **Safety 预览：**
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
- `do-not-guess-schema` — 无 SQL / 数据文件
- `check-data-grain` — 无数据 pipeline 信号

Reason:
- Project needs both implementation guardrails and UI-quality expectations.
- Frontend-specific rules should be scoped separately to avoid bloating CLAUDE.md.
- Detected both Claude Code and Cursor, so use AGENTS.md as single source.
```
