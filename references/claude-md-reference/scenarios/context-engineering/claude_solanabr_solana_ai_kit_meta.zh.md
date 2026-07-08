# Solana AI Kit - 元配置
<!-- 这是配置仓库维护者文件（不会随用户项目一起交付）。
     真正随用户项目作为 CLAUDE.md 交付的是 CLAUDE-solana.md。 -->

本仓库包含用于 Solana 开发项目的 Claude Code 配置。实际的 Solana 构建器配置位于 `CLAUDE-solana.md`，应将其复制到目标项目作为它们的 `CLAUDE.md`。

**安装文档**：参见 README.md 与 QUICK-START.md。

---

## 本仓库用途

你正在维护 **solana-ai-kit** 仓库——一套用于 Solana 开发的 Claude Code 配置模板/库。你的职责是改进、测试并维护其他项目将使用的 agents、skills、commands、MCP servers 与 rules。

## Token 加载模型
<!-- 原因：理解每个文件何时加载，有助于你规划 token 预算。
     CLAUDE.md 是一条用户消息（非系统提示）——越短，遵循效果越好。
     无 globs 的规则在会话开始时加载，因此要保持精简。 -->

| 文件 | 加载时机 | 预算建议 |
|------|----------|----------|
| `CLAUDE.md` | 会话启动；作为用户消息下发（未缓存） | 保持少于 200 行；每次对话都消耗 token |
| `CLAUDE-solana.md` | 会话启动（用户项目） | 保持少于 120 行；未缓存；HTML 注释会被剥离（免费） |
| `MEMORY.md` | 会话启动 | 上限 200 行 / 25KB；仅保存索引指针 |
| `.claude/rules/*.md`（带 `globs:`） | 懒加载——匹配文件被读取时 | 可详细；零启动开销 |
| `.claude/rules/*.md`（无 `globs:`） | 会话启动 | 极简——始终加载 |
| `.claude/agents/*.md` | Agent 创建时 | 可详细 |
| `.claude/commands/*.md` | 调用时 | 可详细 |
| `.claude/skills/SKILL.md` | 调用时 | 中等；HTML 注释不会被剥离 |
| `.claude/skills/*.md` | 通过链接按需加载 | 可详细 |
| 子目录 `CLAUDE.md` | 懒加载——当 Claude 读取该目录下文件时 | Monorepo 模块配置 |

## 沟通风格

- 不要使用填充语（"I get it"、"Awesome, here's what I'll do"、"Great question"）
- 直接、高效回应——优先给出代码/配置，必要时再解释
- 不确定时承认不确定，不要猜测
- 所有新增内容都要考虑 token 效率

## 常见错误

**禁止**：
- 在未意识到 `CLAUDE-solana.md` 会交付到用户项目的情况下编辑它（受众与本仓库不同）
- 添加与外部子模块中已有内容重复的 agent/skill
- 在 `CLAUDE.md` 中按行号引用文件——行号会频繁变动
- 添加/移除 MCP server 时忘记更新 `.env.example`
- 留下过时的数量描述（例如 "15 agents"、"22 commands"）——提交前用 grep 验证

**应当**：
- 每次提交前运行 `bash validate.sh && bash tests/run_all.sh`
- 任何结构变更后检查 QUICK-START.md 与 README.md
- 修改 `install.sh` 后在临时目录中测试
- 保持 `CLAUDE-solana.md` 在 120 行以内——它会在每次用户对话时加载

## 影响映射
<!-- 关键：这是文档过时的首要原因。添加/移除
     任何组件时，提交前都要逐行检查以下表格。 -->

当 X 变更时，也要更新 Y：

| 变更项 | 需同步更新 |
|--------|------------|
| 添加/移除 **agent** | README.md agent 表格 + tree 数量，QUICK-START.md tree 数量，install.sh 输出，tests/test_agents.sh + test_install.sh 断言 |
| 添加/移除 **command** | README.md commands 表格 + tree 数量，QUICK-START.md tree 数量，tests/test_commands.sh + test_install.sh 断言 |
| 添加/移除 **MCP server** | README.md MCP 表格，CLAUDE-solana.md MCP 列表，QUICK-START.md MCP 列表，.env.example，.claude/commands/setup-mcp.md |
| 添加/移除 **submodule** | .gitmodules，README.md submodules 表格 + tree，QUICK-START.md tree，.claude/skills/SKILL.md 路由 |
| 修改 **install.sh** | 测试：在临时目录运行 `bash tests/test_install.sh` |
| 修改 **CLAUDE-solana.md** | 该文件会交付到所有用户项目——受众与本仓库不同 |
| 提升 **`.claude/VERSION`** | 同时提升 `plugin/.claude-plugin/plugin.json` 中的 `version`（必须与 VERSION 的 semver 一致——`tests/test_plugin.sh` 会强制检查）。插件通过 `plugin.json` 的 `version` + semver 的 `vX.Y.Z` git tag 锁定；不要运行 `claude plugin tag`（它会生成冗余的 `{name}--vX.Y.Z` tag，与 semver tag 重复）。 |

## Submodule 陷阱

- **永远不要** `git add .claude/skills/ext/<dir>`——这样会以 tree 形式提交，而不是 submodule。应使用 `git submodule add <url> .claude/skills/ext/<name>`，然后 `git add .gitmodules .claude/skills/ext/<name>`。
- 上游 submodule 路径重命名会波及所有引用 skill 文件的 agents 与 commands。提交前用 grep 查找旧路径。
- `install.sh` 会静默跳过非 git 仓库目标的 submodule 初始化——这是有意为之，不是 bug。

## 编辑本仓库时

| 组件 | 位置 | 关键规则 |
|------|------|----------|
| **Agents** | `.claude/agents/` | 职责不重叠；跨领域工作时创建其他 agents |
| **Skills** | `.claude/skills/` | 渐进加载；通过 `SKILL.md` 引用；优先用代码而非大段文字 |
| **Commands** | `.claude/commands/` | 原子化（一个 command，一个目的）；记录输入/输出 |
| **Rules** | `.claude/rules/` | 极简——每次匹配文件都会加载；frontmatter 中使用 `globs` |
| **MCP Servers** | `.mcp.json` | 记录环境变量；测试连通性；更新 setup-mcp command |
| **Plugin** | `.claude-plugin/marketplace.json` + `plugin/` | 仓库内 marketplace + 软链接的核心插件子树（agents/commands/.mcp.json/local skills 都是软链接到 `.claude/` 的；只有 `hooks/hooks.json` 与插件变体的 `skills/SKILL.md` 是真实文件）。保持 `plugin.json` 的 version = `.claude/VERSION`。`plugin/skills/SKILL.md` 不能包含 `ext/` 链接（插件安装中不存在 submodules）。验证：`claude plugin validate .` + `./plugin`。`install.sh` 仍是完整安装（rules/permissions/submodules） |

## Agent 团队

团队是动态的——通过自然语言创建，而非静态配置（在 settings.json 中启用 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`）。推荐团队模式见 README.md。

## 分支工作流

所有变更都在 feature 分支上进行：`git checkout -b <type>/<scope>-<description>-<DD-MM-YYYY>`

## 合并前检查清单

- [ ] `bash validate.sh && bash tests/run_all.sh` 通过
- [ ] 无重复功能或 AI 垃圾内容（运行 `/diff-review`）
- [ ] 已检查影响映射——所有交叉引用已更新
- [ ] 手动测试：`bash install.sh /tmp/test-project` → 在 Claude Code 中验证

## 测试本地变更

- **本地安装测试**：`SOLANA_AI_KIT_LOCAL_SRC=. bash install.sh /tmp/test-project` —— 使用本地仓库而非从 GitHub 克隆（旧版 `SOLANA_CLAUDE_LOCAL_SRC` 仍可用）。
- **仅 Agents 模式**：`bash install.sh --agents /path` —— 安装到 `.agents/` 而非 `.claude/`。修改 `install.sh` 时两种模式都要测试。

## 发布管理
<!-- 工作流：提升 .claude/VERSION → 更新 .claude/CHANGELOG.md → 验证 → 打 tag -->

- `.claude/VERSION` 保存当前 semver（例如 `1.1.0`）。bug 修复提升 **patch**，新增 agents/skills/commands 提升 **minor**，破坏 install.sh 的变更提升 **major**。
- 提升 VERSION 时，还要在 `.claude/CHANGELOG.md` 顶部新增一条带日期的条目，并按类别列出变更（Added/Changed/Fixed/Removed）。
- 提升后，运行 `bash validate.sh && bash tests/run_all.sh` 并打 tag：`git tag v$(cat .claude/VERSION)`。

## 项目经验
<!-- 在遇到非显而易见的 bug、文档过时事件或配置变更带来意外副作用后，
     追加 1-2 行条目。
     不要重复已有条目。追加前检查。 -->

### 反复出现的问题

### 修复模式

- 上游 submodule 路径变更时：`grep -r "old/path" .claude/` → 更新所有引用 → `bash validate.sh`
- 添加组件时：先按上方影响映射操作，然后运行 `bash validate.sh && bash tests/run_all.sh` 捕获遗漏

### 配置约定

- `.claude/VERSION` 遵循 semver；每次发布都提升。`.claude/CHANGELOG.md` 记录变更内容。
- `/dream` 触发记忆整合（合并、修剪、去重 MEMORY.md）。重大重构后运行。

---

**主配置**：`CLAUDE-solana.md` | **Agents**：`.claude/agents/` | **Skills**：`.claude/skills/` | **Commands**：`.claude/commands/` | **MCP**：`.mcp.json` | **Rules**：`.claude/rules/`
