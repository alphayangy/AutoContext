# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在操作本仓库代码时提供指导。

<!-- AUTO-MANAGED: project-description -->
## 概述

**claude-code-auto-memory** - 一个 Claude Code 插件，可随着代码库演化自动维护 CLAUDE.md 文件（多智能体仓库则维护 AGENTS.md）。通过 hooks 跟踪文件变更，派生智能体更新记忆，并提供用于代码库分析的技能。

核心功能：
- 通过 PostToolUse hooks 实现实时文件跟踪
- 集成 Stop hook 以触发记忆更新
- 用于初始设置的 codebase-analyzer skill
- 用于持续更新 CLAUDE.md 的 memory-processor skill
- 支持多智能体工作流的 AGENTS.md（OpenAI Codex、Gemini 等）

<!-- END AUTO-MANAGED -->

<!-- AUTO-MANAGED: build-commands -->
## 构建与开发命令

```bash
# 安装依赖
uv sync

# 运行测试
uv run pytest tests/ -v

# 运行单个测试文件
uv run pytest tests/test_hooks.py -v

# 代码检查
uv run ruff check .

# 代码格式化
uv run ruff format .

# 类型检查
uv run mypy scripts/
```

<!-- END AUTO-MANAGED -->

<!-- AUTO-MANAGED: architecture -->
## 架构

```
.claude-plugin/          # 插件清单
  plugin.json            # 插件元数据与版本
agents/
  memory-updater.md      # 更新 CLAUDE.md 的智能体
commands/
  init.md                # /auto-memory:init 命令
  calibrate.md           # /auto-memory:calibrate 命令
  status.md              # /auto-memory:status 命令
  sync.md                # /auto-memory:sync 命令
hooks/
  hooks.json             # Hook 注册
scripts/
  post-tool-use.py       # 跟踪文件编辑并写入 dirty-files
  trigger.py             # PreToolUse、Stop、SubagentStop 的统一处理入口
skills/
  codebase-analyzer/     # 初始 CLAUDE.md 生成
  memory-processor/      # 持续更新 CLAUDE.md
  shared/                # 共享引用
tests/
  test_hooks.py          # PostToolUse hook 行为测试
  test_trigger.py        # trigger.py 单元测试
  test_integration.py    # 插件结构测试
  test_skills.py         # Skill 验证测试
```

数据流：
1. 用户通过 Edit/Write 工具或 git 操作（rm、mv）编辑文件
2. PostToolUse hook 将路径追加到会话专用的 `.claude/auto-memory/dirty-files-{session_id}`（无 session_id 时回退到 `dirty-files`）
3. PreToolUse hook（仅 gitmode）在提交前阻止 git commit
4. Stop hook 检测到 dirty files，阻塞 Claude，并请求派生智能体
5. memory-updater 智能体处理文件并更新 CLAUDE.md
6. SubagentStop hook 自动提交 CLAUDE.md（如已配置），清空 dirty-files，并清理过期会话文件

配置：
- 触发模式：`default`（每轮对话后）或 `gitmode`（仅在 git 提交后）
- `memoryFiles`：指定要维护的记忆文件数组 - `["CLAUDE.md"]`（默认）、`["AGENTS.md"]`，或 `["CLAUDE.md", "AGENTS.md"]`（AGENTS.md 保存内容，CLAUDE.md 重定向）
- `autoCommit`：为 true 时，memory-updater 完成后自动提交记忆文件变更
- `autoPush`：为 true 时（需要 autoCommit），将提交推送到远程
- 配置存储在 `.claude/auto-memory/config.json`
- 初始化向导以交互方式配置 triggerMode、memoryFiles、autoCommit 和 autoPush，然后更新 `.gitignore` 以排除 `dirty-files*` 跟踪文件

<!-- END AUTO-MANAGED -->

<!-- AUTO-MANAGED: conventions -->
## 代码规范

- **Python**：3.9+，使用类型提示，snake_case 命名
- **导入**：按标准库、第三方、本地模块分组
- **文档字符串**：模块级文档字符串说明用途
- **Hooks**：PostToolUse/SubagentStop 零输出（节省 token），Stop/PreToolUse 输出 JSON
- **Hook 路由**：使用 stdin JSON 中的 hook_event_name 区分行为
- **Hook 命令**：使用 python3 并带回退（`python3 script.py || python script.py`）以保证跨平台兼容
- **Skills/Commands**：使用 YAML frontmatter，包含 name/description
- **行长度**：100 字符（ruff 配置）
- **测试**：pytest，测试名使用描述性命名（test_verb_condition）

<!-- END AUTO-MANAGED -->

<!-- AUTO-MANAGED: patterns -->
## 已识别模式

- **Hook 合并模式**：单个 trigger.py 处理 PreToolUse、Stop、SubagentStop hooks，根据 hook_event_name 路由
- **初始化保护模式**：post-tool-use.py 中的 `plugin_initialized()`、handle_stop() 和 handle_pre_tool_use() 均以 config.json 存在为前提 — 从未运行 `/auto-memory:init` 的项目保持完全静默
- **Hook 生命周期模式**：PostToolUse 跟踪 → Stop/PreToolUse 拦截 → 派生智能体 → SubagentStop 清理（清理仅以 dirty-files 为前提，而非 config.json，以防止无限循环）
- **关注点分离**：PostToolUse（静默跟踪） vs Stop/PreToolUse（带输出的拦截） vs SubagentStop（清理）
- **Dirty File 模式**：以字典键去重（路径作为键），在每轮末尾批量处理，通过 `dirty-files-{session_id}` 会话隔离；存在 commit context 条目时覆盖普通路径条目
- **Skill 模式**：YAML frontmatter + 含 algorithm 章节的 markdown 正文
- **模板模式**：AUTO-MANAGED 标记用于可自动更新章节
- **配置模式**：JSON 配置位于 `.claude/auto-memory/config.json`，包含 `triggerMode`、`autoCommit`、`autoPush`
- **内联提交上下文**：commit hash 和 message 与文件路径内联存储在 dirty-files 中（`/path/to/file [hash: message]`）
- **会话隔离模式**：来自 hook stdin JSON 的 `session_id` 用于按会话限定 dirty-files，并回退到共享文件以保持向后兼容
- **过期会话清理模式**：`cleanup_stale_session_files()` 在每次 SubagentStop 时清理超过 24 小时的孤立会话 dirty-files
- **Dirty-Files 读取顺序**：memory-updater 先读取普通 `dirty-files`；仅当普通文件为空或缺失时才检查会话专属 `dirty-files-*` 文件
- **Gitignore 管理模式**：`/auto-memory:init` 将 `.claude/auto-memory/dirty-files*` 追加到 `.gitignore`（如文件不存在则创建），确保跟踪文件不会被提交
- **Bash 跟踪范围模式**：`extract_files_from_bash()` 仅跟踪显式破坏文件的命令（rm、git rm、mv、git mv、unlink）；跳过其他 Bash 命令（只读、构建工具、包管理器）；解析器在 shell 操作符（`&&`、`||`、`;`、`|`）和重定向处停止
- **测试初始化辅助模式**：`_init_config(tmp_path)` 在测试中创建 `.claude/auto-memory/config.json` 以满足 `plugin_initialized()` 保护；验证静默行为的测试故意不调用此方法
- **记忆文件选择模式**：config.json 中的 `memoryFiles` 决定活跃记忆文件；memory-updater 读取配置以查找 `AGENTS.md` 或 `CLAUDE.md` 实例；所有 skills 和 commands 均尊重此配置，而非硬编码 CLAUDE.md
- **AGENTS.md 重定向模式**：当同时配置 CLAUDE.md 和 AGENTS.md 时，CLAUDE.md 仅包含单行重定向（`Read AGENTS.md in this directory for project context.`）；memory-processor 跳过更新重定向文件
- **多智能体记忆模式**：AGENTS.md 支持使 Claude Code、OpenAI Codex、Gemini 及其他读取 AGENTS.md 的智能体共享记忆；涉及 AGENTS.md 时自动提交消息使用 `chore: update memory files [auto-memory]`

<!-- END AUTO-MANAGED -->

<!-- AUTO-MANAGED: git-insights -->
## Git 洞察

来自提交历史的设计决策：
- Hook 合并：移除 stop.py，功能合并到 trigger.py 以简化维护
- 新增 SubagentStop hook，在智能体完成后自动清理 dirty-files
- 智能体简化：memory-updater.md 不再处理清理（委托给 SubagentStop）
- 新增 PreToolUse hook，用于 gitmode 在提交前拦截
- 新增模板强制，确保 CLAUDE.md 结构一致
- Git 提交上下文增强，以改善变更跟踪
- 可配置触发模式（default 与 gitmode）
- Windows 兼容：hook 命令中使用 python3/python 回退模式
- Default 模式优化：跳过 git commit 跟踪（文件已通过 Edit/Write 跟踪）
- SubagentStop 清理仅以 dirty-files 为前提（而非 config.json）：要求 config.json 会在未初始化项目中导致无限 Stop-hook 循环，因为 dirty-files 永远无法清空
- 新增初始化保护（#17）：PostToolUse、Stop 和 PreToolUse 中的 plugin_initialized() 检查使插件在从未运行 `/auto-memory:init` 的项目中保持完全静默
- 收紧类型注解：dict[str, Any] 泛型、typed main() -> None、收窄 handle_git_commit 返回类型
- 支持会话感知的 dirty-files（#16）：来自 hook stdin JSON 的 session_id 按会话限定 dirty-files，防止并发工作流中的跨会话干扰
- 自动提交/推送开关（#18）：SubagentStop 处理程序中的 autoCommit 和 autoPush 配置选项，仅提交 CLAUDE.md 文件并优雅处理失败
- handle_subagent_stop 签名由 (project_dir) 改为 (input_data, project_dir)，以接收 session_id 并支持加载 auto-commit 配置
- SubagentStop 清理修复（#28/#29）：build_spawn_reason() 现在在 Task 工具派生指令中显式传递 subagent_type='auto-memory:memory-updater' — 省略会导致 SubagentStop 不触发且 dirty-files 永远无法清空
- 新增 AGENTS.md 支持（#14, v0.9.2）：`memoryFiles` 配置选项支持维护 AGENTS.md 替代 CLAUDE.md 或与其同时维护；初始化向导、status、sync、codebase-analyzer 和 memory-processor 均已更新以尊重此配置；同时配置两者时生成 CLAUDE.md 重定向文件

<!-- END AUTO-MANAGED -->

<!-- AUTO-MANAGED: best-practices -->
## 最佳实践

来自 Claude Code 文档：
- 保持 CLAUDE.md 简洁，聚焦可执行指导
- 对需要自动更新的章节使用 AUTO-MANAGED 标记
- 对跨更新持久保留的自定义注释使用 MANUAL 章节
- 子树 CLAUDE.md 文件继承根文件并添加模块专属上下文

<!-- END AUTO-MANAGED -->

<!-- MANUAL -->
## 自定义备注

在此添加项目专属备注。本章节不会被自动修改。

<!-- END MANUAL -->
