# CLAUDE.md

本文件为 Claude Code（claude.ai/code）处理本仓库代码时提供指导。

---

## 项目概览

**ClaudeForge** 是一套用于自动化创建、增强和维护 Claude Code 项目 CLAUDE.md 文件的完整工具包。本仓库由三个集成组件构成：

1. **Skill** (`claudeforge-skill`) - 负责分析、生成与验证的核心 Python 模块
2. **Slash Command** (`/enhance-claude-md`) - 交互式多阶段发现工作流
3. **Guardian Agent** (`claude-md-guardian`) - 后台维护代理

---

## 架构

### 组件交互流程

```
User Project
    ↓
/enhance-claude-md (Slash Command)
    ↓
[Phase 1: Discovery] → [Phase 2: Analysis] → [Phase 3: Task]
    ↓
claude-md-guardian (Agent) OR Direct Skill Invocation
    ↓
claudeforge-skill (Python Modules)
    ↓
workflow.py → analyzer.py → validator.py → template_selector.py → generator.py
    ↓
CLAUDE.md Created/Updated with 100% Native Format
```

### Python 模块架构

本 skill 包含 5 个核心模块（约 2,190 行）：

**workflow.py (432 行)** - `InitializationWorkflow` 类
- 为新项目编排交互式初始化流程
- 方法：`check_claude_md_exists()`、`generate_exploration_prompt()`、`analyze_discoveries()`
- 检测内容：项目类型、技术栈、团队规模、开发阶段、工作流
- 返回：用于模板选择的项目上下文字典

**analyzer.py (382 行)** - `CLAUDEMDAnalyzer` 类
- 分析现有 CLAUDE.md 文件
- 方法：`analyze_file()`、`detect_sections()`、`calculate_quality_score()`、`generate_recommendations()`
- 质量评分：0-100 分，基于长度（25 分）、完整性（25 分）、格式（20 分）、针对性（15 分）、模块化（15 分）
- 返回：包含质量评分与可执行建议的分析报告

**validator.py (429 行)** - `BestPracticesValidator` 类
- 对照 Anthropic 指南进行验证
- 方法：`validate_length()`、`validate_structure()`、`validate_formatting()`、`validate_completeness()`、`validate_all()`
- 检查项：文件长度（20-300 行）、必需章节、Markdown 格式、反模式
- 返回：包含通过/失败状态与详细问题的验证报告

**template_selector.py (467 行)** - `TemplateSelector` 类
- 基于上下文选择合适模板
- 方法：`select_template()`、`customize_template()`、`recommend_modular_structure()`
- 逻辑：将项目类型 + 团队规模映射到模板复杂度
- 返回：包含目标行数与模块化建议的模板配置

**generator.py (480 行)** - `ContentGenerator` 类
- 生成新的或增强现有 CLAUDE.md 内容
- 方法：`generate_root_file()`、`generate_context_file()`、`generate_section()`、`merge_with_existing()`
- 支持：根文件、上下文特定文件（backend/、frontend/、database/）、单独章节
- 返回：完全符合原生格式要求的完整 CLAUDE.md 内容

### 关键验证规则

所有生成的 CLAUDE.md 文件必须包含：
- 项目结构（ASCII 树形图）
- 文件结构说明
- 设置与安装说明
- 架构章节（适用于复杂项目）
- 与 `/update-claude-md` slash command 格式兼容的验证
- 与 `skill/examples/` 中参考示例的交叉检查

---

## 安装与测试

### 测试安装脚本

```bash
# macOS/Linux
./install.sh
# 选择选项 1（用户级）或 2（项目级）
# 在 ~/.claude/ 或 ./.claude/ 验证安装

# Windows
.\install.ps1
# 选项同上

# 验证已安装组件：
ls -la ~/.claude/skills/claudeforge-skill/
ls -la ~/.claude/commands/enhance-claude-md/
ls -la ~/.claude/agents/claude-md-guardian.md
```

### 安装后的目录结构

```
~/.claude/                           # 用户级安装
├── skills/
│   └── claudeforge-skill/          # 从 skill/ 复制
│       ├── SKILL.md
│       ├── analyzer.py
│       ├── validator.py
│       ├── generator.py
│       ├── template_selector.py
│       ├── workflow.py
│       └── examples/               # 7 个参考模板
├── commands/
│   └── enhance-claude-md/          # 从 command/ 复制
│       └── enhance-claude-md.md
└── agents/
    └── claude-md-guardian.md       # 从 agent/ 复制
```

---

## 开发工作流

### 修改 Python 模块

更新 skill 模块（analyzer.py、generator.py 等）时：

1. 编辑 `skill/` 目录中的文件
2. 重新安装以测试变更：`./install.sh`（选择选项 2 进行项目级测试）
3. 在 Claude Code 中测试 skill 调用：`/enhance-claude-md`
4. 对照 `skill/examples/` 中的参考示例验证输出
5. 在 `CHANGELOG.md` 中记录变更

### 修改 Slash Command

更新 `/enhance-claude-md` 命令时：

1. 编辑 `command/enhance-claude-md.md`
2. 重点修改以下章节：
   - **Phase 1 (Discovery)**：检查项目状态的 Bash 命令
   - **Phase 2 (Analysis)**：决定初始化还是增强的逻辑
   - **Phase 3 (Task)**：Skill/agent 调用逻辑
3. 通过复制命令重新安装测试：`cp command/enhance-claude-md.md ~/.claude/commands/enhance-claude-md/`
4. 重启 Claude Code 并测试：`/enhance-claude-md`

### 修改 Guardian Agent

更新 `claude-md-guardian` 代理时：

1. 编辑 `agent/claude-md-guardian.md`
2. 关键 YAML frontmatter 字段：
   - `tools`：限定为 Bash、Read、Write、Edit、Grep、Glob、Skill
   - `model`：设置为 `haiku` 以节省 token
   - `color`：视觉指示器（紫色）
3. Agent 工作流阶段：
   - Phase 1：评估（检查 git 变更）
   - Phase 2：分析（确定范围）
   - Phase 3：更新（调用 skill 进行定向更新）
4. 测试：`cp agent/claude-md-guardian.md ~/.claude/agents/`

### 添加新模板

添加新参考模板（例如 Rust、移动端）时：

1. 在 `skill/examples/` 中创建新模板文件
2. 遵循原生格式结构：
   - 项目结构图（ASCII 树）
   - 设置与安装
   - 架构章节
   - 技术特定指南
3. 在 `skill/examples/README.md` 中更新新模板说明
4. 更新 `template_selector.py` 逻辑以检测何时使用新模板
5. 在 `skill/sample_input.json` 中添加测试用例

---

## 测试与验证

### 手动测试清单

**测试新项目初始化：**
```bash
# 1. 创建测试项目
mkdir test-project && cd test-project
git init
npm init -y  # 或创建 package.json

# 2. 运行 slash command
/enhance-claude-md

# 3. 验证 Claude：
#    - 探索仓库
#    - 检测 TypeScript/Node 项目
#    - 展示发现结果
#    - 请求确认
#    - 创建原生格式 CLAUDE.md
```

**测试现有项目增强：**
```bash
# 1. 创建基础 CLAUDE.md
echo "# CLAUDE.md\n\n## Tech Stack\n- TypeScript" > CLAUDE.md

# 2. 运行 slash command
/enhance-claude-md

# 3. 验证 Claude：
#    - 分析现有文件
#    - 计算质量评分（0-100）
#    - 识别缺失章节（Project Structure、Setup 等）
#    - 请求增强
#    - 添加缺失的原生格式章节
```

**测试 Guardian Agent：**
```bash
# 1. 进行重大变更
npm install react  # 添加新依赖
mkdir src/components  # 新建目录

# 2. 启动新的 Claude Code 会话（触发 SessionStart）

# 3. 验证 agent：
#    - 通过 git diff 检测变更
#    - 自动更新 CLAUDE.md
#    - 报告："Tech Stack: Added react"、"Project Structure: Updated diagram"
```

### 质量验证

所有生成的 CLAUDE.md 文件应通过以下检查：

```python
# 使用 validator.py
validator = BestPracticesValidator(content)
results = validator.validate_all()

# 预期通过项：
# - 文件长度：20-300 行（或 >300 行时采用模块化）
# - 结构：必需章节存在
# - 格式：有效 markdown、正确的标题层级
# - 完整性：代码示例、技术栈、工作流
# - 反模式：无硬编码密钥、无 TODO/占位符
```

---

## 文件组织

### 仓库结构

```
ClaudeForge/
├── skill/                          # Python 模块（核心能力）
│   ├── analyzer.py                 # 文件分析
│   ├── validator.py                # 最佳实践验证
│   ├── generator.py                # 内容生成
│   ├── template_selector.py        # 模板选择逻辑
│   ├── workflow.py                 # 交互式初始化
│   ├── SKILL.md                    # Skill 定义（YAML frontmatter）
│   ├── sample_input.json           # 测试场景（6 个示例）
│   ├── expected_output.json        # 预期输出
│   └── examples/                   # 7 个参考模板
│
├── command/                        # Slash command 定义
│   ├── enhance-claude-md.md        # 多阶段工作流
│   └── README.md
│
├── agent/                          # Guardian agent 定义
│   ├── claude-md-guardian.md       # 后台维护代理
│   └── README.md
│
├── docs/                           # 文档
│   ├── INSTALLATION.md
│   ├── QUICK_START.md
│   ├── ARCHITECTURE.md
│   ├── TROUBLESHOOTING.md
│   └── CONTRIBUTING.md
│
├── examples/                       # 使用示例（markdown）
├── hooks/                          # 质量钩子（pre-commit）
├── .github/                        # GitHub 模板与工作流
│   ├── workflows/validate.yml      # CI/CD 验证
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODE_OF_CONDUCT.md
│
├── install.sh                      # macOS/Linux 安装脚本
├── install.ps1                     # Windows 安装脚本
├── README.md                       # 项目概览
├── CHANGELOG.md                    # 版本历史
├── LICENSE                         # MIT License
└── CLAUDE.md                       # 本文件
```

### 重要：双目录结构

注意存在重复：`claude-md-enhancer/`（旧版）和 `skill/`（当前）。进行修改时：
- **始终编辑 `skill/`** - 这是安装程序使用的活跃版本
- `claude-md-enhancer/` 仅作参考，不再积极维护

---

## 常见操作

### 更新参考模板

```bash
# 编辑模板
vim skill/examples/python-api-CLAUDE.md

# 测试模板选择
# 1. 创建符合模板条件的测试项目
mkdir test-python-api && cd test-python-api
echo "fastapi" > requirements.txt

# 2. 运行 slash command 并验证使用了该模板
/enhance-claude-md
```

### 更新质量评分逻辑

```bash
# 编辑 analyzer.py
vim skill/analyzer.py

# 更新 calculate_quality_score() 方法
# 当前评分细则：
#   - length_appropriateness: 25 分（20-300 行为理想）
#   - section_completeness: 25 分（必需章节存在）
#   - formatting_quality: 20 分（markdown、标题、代码块）
#   - content_specificity: 15 分（项目特定，非通用）
#   - modular_organization: 15 分（必要时使用上下文文件）

# 测试评分
python3 -c "
from skill.analyzer import CLAUDEMDAnalyzer
with open('test-CLAUDE.md') as f:
    analyzer = CLAUDEMDAnalyzer(f.read())
    report = analyzer.analyze_file()
    print(f'Quality Score: {report[\"quality_score\"]}/100')
"
```

### 更新安装脚本

```bash
# 编辑安装程序
vim install.sh  # 或 install.ps1

# 关键章节：
# - 安装路径（用户级 vs 项目级）
# - 组件复制（skill、command、agent）
# - 备份逻辑（已有安装）
# - 质量钩子安装（可选）

# 测试安装脚本
./install.sh
# 选择测试选项并验证所有组件正确复制
```

---

## 集成点

### Skill ↔ Slash Command

Slash command 通过以下方式调用 skill：
```markdown
# 在 command/enhance-claude-md.md 的 Phase 3 中：

I can invoke the `claude-md-enhancer` skill directly to handle the appropriate workflow based on what I discovered above.
```

Claude Code 识别 skill 名称 `claude-md-enhancer` 并调用 Python 模块。

### Skill ↔ Guardian Agent

Agent 将 skill 作为其核心能力使用：
```yaml
# 在 agent/claude-md-guardian.md 中：
tools: Bash, Read, Write, Edit, Grep, Glob, Skill
```

Agent 在工作流中通过 `Skill: claude-md-enhancer` 调用 skill。

### Agent ↔ Git

Agent 通过 git 命令检测变更：
```bash
git diff --name-status HEAD~10
git log --since="1 week ago" --oneline --no-merges
git diff HEAD~10 -- package.json requirements.txt
```

在以下情况触发更新：
- 5 个以上文件被修改
- 新增依赖
- 新建目录
- 里程碑后手动调用

---

## 技术栈检测逻辑

workflow 和 template selector 通过以下方式检测技术栈：

**前端检测：**
- React：`package.json` 包含 `"react"`
- Vue：`package.json` 包含 `"vue"`
- Angular：`angular.json` 存在
- TypeScript：`tsconfig.json` 存在

**后端检测：**
- Node.js：`package.json` 存在
- Python：`requirements.txt`、`pyproject.toml`、`setup.py`
- Go：`go.mod` 存在
- Java：`pom.xml`、`build.gradle`
- Rust：`Cargo.toml` 存在

**数据库检测：**
- PostgreSQL：`package.json` 或 `requirements.txt` 包含 "pg" 或 "psycopg2"
- MongoDB：包含 "mongoose" 或 "pymongo"
- Redis：包含 "redis" 或 "ioredis"

在 `skill/workflow.py` 的 `_detect_tech_stack()` 方法中更新检测逻辑。

---

## 仓库命名

**项目名称：** ClaudeForge
**GitHub URL：** https://github.com/alirezarezvani/ClaudeForge
**Skill 名称：** `claudeforge-skill`（作为目录名安装）
**Slash Command：** `/enhance-claude-md`（固定名称，用户不可更改）
**Agent 名称：** `claude-md-guardian`（文件名）

更新引用时：
- `skill/SKILL.md` → YAML frontmatter `name: claude-md-enhancer`（为兼容保留）
- `README.md` → 使用 "ClaudeForge" 作为显示名称
- `install.sh` → 复制到 `claudeforge-skill/` 目录
- 内部文档 → 统一使用 "ClaudeForge"

---

## 版本管理

**当前版本：** 1.0.0（参见 CHANGELOG.md）
**版本规范：** 语义化版本（MAJOR.MINOR.PATCH）

发布新版本时：
1. 在 `CHANGELOG.md` 新版本标题下记录变更
2. 更新 `README.md` 中的版本徽章
3. 更新 `skill/SKILL.md` 底部版本信息
4. 创建 git 标签：`git tag -a v1.1.0 -m "Release v1.1.0"`
5. 推送标签：`git push origin v1.1.0`
6. 使用 CHANGELOG 摘录创建 GitHub release

---

## 许可与版权

**许可：** MIT License
**版权：** © 2025 Alireza Rezvani

所有文件应包含适当的版权声明头。LICENSE 文件具有最终效力。
