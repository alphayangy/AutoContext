# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在本仓库中处理代码时提供指引。

## 项目概览

claude-reflect 是一个 Claude Code 插件，实现了一个两阶段自学习系统：
1. **捕获阶段**（自动）：Hooks 检测用户提示中的纠正模式，并将其加入队列
2. **处理阶段**（手动）：`/reflect` 命令处理队列中的学习内容，经人工审核后写入 CLAUDE.md 文件

## 架构

```
.claude-plugin/plugin.json  → Plugin manifest, points to hooks
hooks/hooks.json            → Hook definitions (PreCompact, PostToolUse)
scripts/                    → Python scripts for hooks and extraction
scripts/lib/                → Shared utilities (reflect_utils.py)
scripts/legacy/             → Deprecated bash scripts (for reference)
commands/*.md               → Skill definitions for /reflect, /reflect-skills, /skip-reflect, /view-queue
SKILL.md                    → Context provided when plugin is invoked
tests/                      → Test suite (pytest)
```

### 数据流

1. 用户提示 → `capture_learning.py`（UserPromptSubmit hook）→ `~/.claude/learnings-queue.json`
2. `/reflect` 命令 → 读取队列并扫描会话 → 过滤/去重 → 路由到记忆目标
3. 会话文件位于 `~/.claude/projects/[PROJECT_FOLDER]/*.jsonl`

### 记忆目标（完整层级）

| 目标 | 路径 | 类型 | 说明 |
|------|------|------|------|
| 全局 CLAUDE.md | `~/.claude/CLAUDE.md` | `global` | 始终启用 |
| 项目 CLAUDE.md | `./CLAUDE.md` | `root` | 项目专属 |
| CLAUDE.local.md | `./CLAUDE.local.md` | `local` | 个人使用，已加入 gitignore |
| 子目录 | `./**/CLAUDE.md` | `subdirectory` | 自动发现 |
| 项目规则 | `./.claude/rules/*.md` | `rule` | 模块化，按路径作用域 |
| 用户规则 | `~/.claude/rules/*.md` | `user-rule` | 全局模块化规则 |
| 自动记忆 | `~/.claude/projects/<project>/memory/*.md` | `auto-memory` | 低置信度暂存 |
| 技能文件 | `./commands/*.md` | `skill` | 使用技能期间的纠正 |
| AGENTS.md | `./AGENTS.md` | `agents` | 跨工具标准 |

### 关键文件

- `scripts/lib/reflect_utils.py`：共享工具（路径、队列操作、正则检测、记忆层级发现、自动记忆、规则 frontmatter 解析）
- `scripts/lib/semantic_detector.py`：通过 `claude -p` 进行 AI 语义分析
- `scripts/capture_learning.py`：模式检测（纠正、正向、显式标记）及置信度打分
- `scripts/check_learnings.py`：在上下文压缩前备份队列的 PreCompact hook
- `scripts/extract_session_learnings.py`：从会话 JSONL 文件中提取用户消息
- `scripts/extract_tool_rejections.py`：从工具拒绝信息中提取用户纠正
- `scripts/compare_detection.py`：在会话数据上对比正则检测与语义检测
- `commands/reflect.md`：定义 `/reflect` 工作流的主技能（具备记忆层级感知）
- `commands/reflect-skills.md`：技能发现——基于 AI 的会话模式检测

## 开发命令

```bash
# Test capture hook with simulated input
echo '{"prompt":"no, use gpt-5.1 not gpt-5"}' | python3 scripts/capture_learning.py

# View current learnings queue
cat ~/.claude/learnings-queue.json

# Test session extraction
python3 scripts/extract_session_learnings.py ~/.claude/projects/[PROJECT]/*.jsonl --corrections-only

# Run tests
python -m pytest tests/ -v

# Clear queue for testing
echo "[]" > ~/.claude/learnings-queue.json
```

## 插件结构

插件通过 `.claude-plugin/plugin.json` 注册：
- Hooks 定义在 `hooks/hooks.json` 中
- 命令（技能）是 `commands/` 目录下的 Markdown 文件
- `SKILL.md` 在插件激活时提供上下文

### Hook 事件

| Hook | 脚本 | 用途 |
|------|------|------|
| SessionStart | `session_start_reminder.py` | 显示待处理学习提醒 |
| UserPromptSubmit | `capture_learning.py` | 检测纠正并入队 |
| PreCompact | `check_learnings.py` | 在压缩前备份队列 |
| PostToolUse (Bash) | `post_commit_reminder.py` | 提交后提醒执行 /reflect |

## 检测方法

### 正则模式（实时）

`scripts/lib/reflect_utils.py` 定义了模式检测：
- **纠正类**："no, use X"、"don't use"、"stop using"、"that's wrong"、"actually"、"use X not Y"
- **正向类**："perfect!"、"exactly right"、"great approach"、"nailed it"
- **显式类**："remember:" 前缀（置信度最高）

根据模式强度与命中数量，置信度分数范围为 0.60–0.90。

### 语义 AI 校验（在 /reflect 期间）

`scripts/lib/semantic_detector.py` 提供 AI 驱动的校验：
- 使用 `claude -p --output-format json` 进行语义分析
- **多语言支持**——适用于任意语言，不限于英文
- **更高准确度**——过滤正则带来的误报
- **更简洁的学习项**——提取简明、可执行的陈述

关键函数：
- `semantic_analyze(text)` —— 分析单条消息
- `validate_queue_items(items)` —— 批量校验队列项

回退：如果 Claude CLI 不可用，则使用正则检测作为回退方案。

### 对比测试

`scripts/compare_detection.py` 对比正则检测与语义检测：
```bash
python scripts/compare_detection.py --project .
```

## 会话文件格式

会话文件为 JSONL 格式，位于 `~/.claude/projects/[PROJECT_FOLDER]/`：
- 用户消息：`{"type": "user", "message": {"content": [{"type": "text", "text": "..."}]}, "isMeta": false}`
- 工具拒绝：`{"type": "user", "message": {"content": [{"type": "tool_result", "is_error": true, "content": "...the user said:\n[feedback]"}]}}`
- 过滤 `isMeta: true`，以排除命令展开内容

## 队列项结构

```json
{
  "type": "auto|explicit|positive|guardrail",
  "message": "user's original text",
  "timestamp": "ISO8601",
  "project": "/path/to/project",
  "patterns": "matched pattern names",
  "confidence": 0.75,
  "sentiment": "correction|positive",
  "decay_days": 90
}
```

## 技能发现（/reflect-skills）

分析会话历史，发现可转化为技能的重复模式。

**设计原则：**
- **AI 驱动**——Claude 通过推理识别模式，而非正则
- **语义相似度**——在不同表述中识别相同意图
- **人机协同**——生成技能前由用户确认

**用法：**
```bash
/reflect-skills              # Analyze last 14 days
/reflect-skills --days 30    # Analyze last 30 days
/reflect-skills --dry-run    # Preview without generating files
```

**检测内容：**
- 工作流模式（重复的多步骤序列）
- 误解模式（可转化为护栏的纠正）
- 意图相似性（目标相同，表述不同）

## 技能改进路由

运行 `/reflect` 时，可将技能执行过程中产生的纠正回写到技能文件本身。

**工作原理：**
1. `/reflect` 检测纠正是否发生在技能调用之后（例如 `/deploy`）
2. Claude 判断该纠正是否与技能工作流相关
3. 向用户提供路由选项：技能文件 | CLAUDE.md | 两者
4. 在技能文件的适当章节（步骤、护栏等）进行更新

**示例：**
```
User: /deploy
Claude: [deploys without running tests]
User: "no, always run tests before deploying"

→ /reflect detects this relates to /deploy
→ Offers to add "Run tests before deploying" to commands/deploy.md
→ Skill file updated with new step in workflow
```

## 平台支持

- **macOS**：完全支持
- **Linux**：完全支持
- **Windows**：完全支持（原生 Python，无需 WSL）

需要 Python 3.6+。

## 发布

版本升级清单与发布流程请参阅 [RELEASING.md](RELEASING.md)。
