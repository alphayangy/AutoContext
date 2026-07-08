# aspens

## Skills

- `.claude/skills/base/skill.md` — 基础仓库 skill；在此仓库中工作时始终加载。
- `.claude/skills/agent-customization/skill.md` — 通过 `aspens customize agents` 将项目上下文以 LLM 驱动的方式注入到已安装的 agent 模板中
- `.claude/skills/claude-runner/skill.md` — Claude/Codex CLI 执行层：prompt 加载、stream-json 解析、文件输出提取、路径清理、skill 文件写入以及 skill 规则生成
- `.claude/skills/cli-shell/skill.md` — 顶层 Commander 接入、欢迎界面、缺失 hook 警告、CliError 退出处理以及公开程序化 API 表面
- `.claude/skills/codex-support/skill.md` — 多目标输出系统：目标抽象、后端路由、面向 Codex CLI 及未来目标的 content transform
- `.claude/skills/doc-impact/skill.md` — 上下文健康度分析：新鲜度、领域覆盖、hub 浮现、drift 检测、LLM 驱动的解读以及生成式 agent 上下文的自动修复
- `.claude/skills/doc-sync/skill.md` — 增量式 skill 更新器，将 git diff 映射到受影响的 skill，并可选地通过 post-commit hook 自动同步
- `.claude/skills/import-graph/skill.md` — 静态导入分析，构建依赖图、领域聚类、hub 文件、git churn 热点以及文件优先级排序
- `.claude/skills/repo-scanning/skill.md` — 确定性仓库分析：语言/框架检测、结构映射、领域发现、健康检查以及导入图集成
- `.claude/skills/save-tokens/skill.md` — 省 token 会话自动化：状态栏、prompt 守卫、precompact 交接、会话轮换以及 Claude Code 的 handoff 命令
- `.claude/skills/skill-generation/skill.md` — 面向 Claude Code skills 与 CLAUDE.md 的 LLM 驱动生成流水线：doc-init 命令、prompt 系统、上下文构建以及输出解析
- `.claude/skills/template-library/skill.md` — 通过 `aspens add`、`aspens doc init` 和 `aspens save-tokens` 安装到用户 `.claude/` 目录中的捆绑 agents、commands、hooks 与 settings

## Commands

- `npm test` — 运行 Vitest（`vitest run`）
- `npm start` — 运行 CLI（`node bin/cli.js`）
- `npm run lint` — 空操作检查（`echo 'No linter configured yet' && exit 0`）
- `aspens scan [path]` — 确定性仓库扫描
- `aspens doc init [path]` — 生成 skills、hooks 与 instructions 文件（`--target claude|codex|all`，`--recommended` 表示包含 save-tokens、agents 和 doc-sync hook 的完整推荐配置）
- `aspens doc impact [path]` — 展示生成上下文的新鲜度、覆盖度、drift 以及 LLM 解读（可交互式应用修复）
- `aspens doc sync [path]` — 根据最近的 diff 更新文档
- `aspens doc graph [path]` — 重建 `.claude/graph.json`
- `aspens add <type> [name]` — 安装捆绑模板
- `aspens customize agents` — 将项目上下文注入到已安装的 agents 中
- `aspens save-tokens [path]` — 安装省 token 的会话设置（`--recommended`、`--remove`）

## Release

- Release workflow：`../dev/release.md`

## Conventions

- 仅使用 ESM：使用 `import`/`export`；禁止使用 `require()`。
- 优先在 command handlers 中使用 `CliError`；顶层处理位于 `bin/cli.js`。
- 在调用 `parse()` 之前必须先初始化 `es-module-lexer`。
- 区分 target/backend 语义：target 是输出格式/位置；backend 是生成 CLI。配置持久化在 `.aspens.json` 中。
- 不要在此重复 base-skill 的指引；如需更深入的仓库上下文，请查阅 `.claude/skills/base/skill.md`。

## Behavior

- **先验证，再断言** — 在未确认之前，不得声称某物已配置、正在运行、已排期或已完成。如果本次会话中尚未验证，请如实说明，不要臆测。
- **确保代码可运行** — 如果你建议修改代码，务必先确保代码运行并通过测试，再声称任务完成。
- **提出澄清问题** — 如果任务存在歧义，应主动询问以澄清，不要自行假设。不要暗示或猜测未明确说明的需求或约束。
- **极简优先** — 编写解决问题的最小代码。不要添加臆测性功能、仅使用一次的抽象，或针对不可能场景的错误处理。
- **精准改动** — 只触碰任务所要求的部分。不要重构相邻代码、修正无关格式，或“优化”并未损坏的部分。
