# Apache Superset 的 LLM 上下文指南

Apache Superset 是一个数据可视化平台，采用 Flask/Python 后端与 React/TypeScript 前端。

## ⚠️ 关键：推送前必须运行 Pre-commit

**每次推送前都必须运行 `pre-commit run --all-files`。** 如果 pre-commit 检查未通过，CI 将会失败。这一点不可妥协。

```bash
# 首先暂存你的改动
git add .

# 对所有文件运行 pre-commit
pre-commit run --all-files

# 如果有自动修复，重新暂存并提交
git add .
git commit --amend  # 或者新建一次提交
```

常见的 pre-commit 失败原因：
- **格式化问题** - black、prettier、eslint 会自动修复
- **类型错误** - mypy 报错需要手动修复
- **代码风格问题** - ruff、pylint 报错需要手动修复

## ⚠️ 关键：正在进行的重构（禁止事项）

**以下迁移正在进行中，请避免使用已弃用的模式：**

### 前端现代化
- **不要使用 `any` 类型** - 使用正确的 TypeScript 类型
- **不要新建 JavaScript 文件** - 转换为 TypeScript（.ts/.tsx）
- **使用 @superset-ui/core** - 不要直接引入 Ant Design，优先使用 @superset-ui/core/components 中的 Ant Design 组件封装
- **使用 antd 主题 token** - 优先使用 antd token，而非旧版主题 token
- **避免自定义 CSS 和样式** - 遵循 antd 最佳实践，尽量避免样式和自定义 CSS

### 测试策略迁移
- **优先单元测试**，其次集成测试
- **优先集成测试**，其次端到端测试
- **E2E 测试使用 Playwright** - 正在从 Cypress 迁移
- **Cypress 已弃用** - 迁移完成后将移除
- **组件测试使用 Jest + React Testing Library**
- **使用 `test()` 替代 `describe()`** - 遵循 [避免测试嵌套](https://kentcdodds.com/blog/avoid-nesting-when-youre-testing) 原则

### 后端类型安全
- **添加类型注解** - 所有新增 Python 代码都需要正确类型
- **MyPy 合规** - 运行 `pre-commit run mypy` 验证
- **SQLAlchemy 类型** - 使用正确的模型注解

### UUID 迁移
- **优先使用 UUID 而非自增 ID** - 新模型应使用 UUID 主键
- **对外暴露 API 时使用 UUID** - 公共 API 中应使用 UUID 而非内部整数 ID
- **现有模型** - 在整数 ID 旁增加 UUID 字段，逐步实现迁移

## 安全与威胁模型

在评估任何代码路径的安全问题之前，请先阅读 [`SECURITY.md`](SECURITY.md)。该文件是 Apache Superset 安全模型的权威规范，人工报告者和自动化扫描工具都会引用它。

简而言之，判断一个发现是否属于范围内的唯一标准是：

> *它是否允许某个主体执行 `SECURITY.md` 中角色与能力矩阵未授权的操作？*

如果是，则在范围内；否则不在范围内。

三条信任边界如下：

1. **Admin 角色** 是完全可信的运营主体。Admin 通过文档化的配置、API 或 UI 执行的任何操作都属于预期能力，不构成漏洞。
2. **运营方（operator）** 拥有部署时决策权（密钥、网络暴露、功能开关、连接器和编解码器选择、通知目标、第三方插件等）。该层级的配置错误属于部署缺陷，不是 Superset 漏洞。
3. **代码库** 负责在向主体暴露功能的所有位置强制执行角色与能力矩阵：API 路由、命令与 DAO 层、UI 处理程序、后台任务以及任何其他入口点。遗漏或错误的权限检查无论出现在何处，都属于范围内。不过，代码仍可能包含注入、SSRF、XSS 或其他类别的问题，这些需单独评估。

本代码库中，路由级授权根据路由类型使用以下三种 Flask-AppBuilder 装饰器之一：

- `@protect()` 用于 REST API 路由（`ModelRestApi` / `BaseApi`）
- `@has_access_api` 用于旧版视图路由
- `@has_access` 用于旧版 HTML 视图路由

对象级授权通过 `security_manager.raise_for_access(...)` 应用于承载数据的对象：仪表盘、图表、数据集与数据源、查询、数据库与表访问权限、查询上下文。其他资源（注解、标签、CSS 模板、报表、RLS 规则等）依赖路由级装饰器加上 DAO 的 `base_filters` 进行所有者范围限定；这些资源未使用 `raise_for_access` 是设计使然，不是可报告的发现。对返回或修改特定数据承载对象的路由遗漏 per-object 门控，属于范围内；遵循其资源类正确模式的代码仍可能存在注入、SSRF、XSS 或其他类别的发现，需单独评估。

完整的角色与能力矩阵、范围内/范围外类别清单以及 CVE 聚合规则均在 [`SECURITY.md`](SECURITY.md) 中。任何具体细节以该文档为准。

**自动化工具提交发现的必备要求**

针对本代码库提交发现的自动化扫描工具（基于 LLM 的代码扫描器、静态分析工具、依赖分析工具等）必须在每条发现中说明：

1. 该发现认为被违反的 [`SECURITY.md`](SECURITY.md) 中角色与能力矩阵的具体行。
2. 该发现假设攻击者所拥有的主体身份（Public、Gamma、sql_lab、Alpha、Admin、嵌入式访客令牌，或具有明确能力授予的自定义角色）。

无法同时说明以上两点的发现应作为问题提交，而非漏洞。此要求旨在确保每个报告的问题都可以对照已发布的安全模型进行测试，并将投机性或仅模式匹配的报告排除在分类队列之外。

## 关键目录

```
superset/
├── superset/                    # Python 后端（Flask、SQLAlchemy）
│   ├── views/api/              # REST API 端点
│   ├── models/                 # 数据库模型
│   └── connectors/             # 数据库连接
├── superset-frontend/src/       # React TypeScript 前端
│   ├── components/             # 可复用组件
│   ├── explore/                # 图表构建器
│   ├── dashboard/              # 仪表盘界面
│   └── SqlLab/                 # SQL 编辑器
├── superset-frontend/packages/
│   └── superset-ui-core/       # UI 组件库（请使用这个）
├── tests/                      # Python/集成测试
├── docs/                       # 文档（变更时请更新）
└── UPDATING.md                 # 破坏性变更日志
```

## 代码规范

### TypeScript 前端
- **避免 `any` 类型** - 使用正确的 TypeScript，复用已有类型
- **函数式组件** 搭配 hooks
- **@superset-ui/core** 用于 UI 组件（不要直接引入 antd）
- **Jest** 进行测试（不要使用 Enzyme）
- **Redux** 用于已有的全局状态，hooks 用于局部状态

### Python 后端
- **所有新增代码必须包含类型注解**
- **MyPy 合规** - 运行 `pre-commit run mypy`
- **SQLAlchemy 模型** 需正确类型化
- **pytest** 进行测试

### Apache 许可证头
- **新文件必须包含 ASF 许可证头** - 创建新代码文件时，请包含标准的 Apache Software Foundation 许可证头
- **LLM 指令文件除外** - 像 AGENTS.md、CLAUDE.md 等文件已列入 `.rat-excludes`，以避免头信息 token 开销

### 代码注释
- **避免时间相关表述** - 注释中不要使用 "now"、"currently"、"today" 等会过时的词
- **编写 timeless 注释** - 无论何时阅读，注释都应保持准确

## 文档要求

- **docs/**：任何面向用户的变更都需要更新
- **UPDATING.md**：在此处添加破坏性变更
- **Docstrings**：新函数/类必须编写文档字符串

## 开发者门户：Storybook 转 MDX 文档

开发者门户会根据 Storybook stories 自动生成 MDX 文档。**Stories 是唯一的真实来源。**

### 核心理念
- **在 STORY 中修复问题，而不是在生成器里** - 当渲染不正确时，首先更新 story 文件
- **生成器应保持轻量** - 它只负责提取和透传数据，避免特殊情况处理
- **Stories 定义一切** - Props、controls、图库、示例均来自 story 元数据

### 面向文档生成的 Story 要求
- 使用 `export default { title: '...' }`（内联），不要 `const meta = ...; export default meta;`
- 交互式 story 命名为 `Interactive${ComponentName}`（例如 `InteractiveButton`）
- 使用 `args` 定义默认 prop 值
- 在 story 级别（而非 meta 级别）定义 `argTypes`，包含控件类型和描述
- 使用 `parameters.docs.gallery` 展示 size×style 变体网格
- 使用 `parameters.docs.sampleChildren` 为需要子元素的组件提供示例子节点
- 使用 `parameters.docs.liveExample` 自定义实时代码块
- 使用 `parameters.docs.staticProps` 处理无法内联解析的复杂对象 prop

### 生成器位置
- 脚本：`docs/scripts/generate-superset-components.mjs`
- 包装器：`docs/src/components/StorybookWrapper.jsx`
- 输出：`docs/developer_portal/components/`

## 架构模式

### 安全与功能
- **安全模型**：参阅顶部 [安全与威胁模型](#安全与威胁模型) 章节以及 [`SECURITY.md`](SECURITY.md)
- **RBAC**：通过 Flask-AppBuilder 实现基于角色的访问控制
- **功能开关**：控制功能上线
- **行级安全**：基于 SQL 的数据访问控制

## 测试工具

### Python 测试辅助
- **`SupersetTestCase`** - 位于 `tests/integration_tests/base_tests.py` 的基类
- **`@with_config`** - 配置模拟装饰器
- **`@with_feature_flags`** - 功能开关测试
- **`login_as()`、`login_as_admin()`** - 认证辅助函数
- **`create_dashboard()`、`create_slice()`** - 数据设置工具

### TypeScript 测试辅助
- **`superset-frontend/spec/helpers/testing-library.tsx`** - 带提供器的自定义 render()
- **`createWrapper()`** - Redux/Router/Theme 包装器
- **`selectOption()`** - Select 组件辅助
- **React Testing Library** - 不要使用 Enzyme（已移除）

### 测试数据库模式
- **Mock 模式**：对配置对象使用 `MagicMock()`，同步代码避免使用 `AsyncMock`
- **API 测试**：新增模型字段时更新预期列

### 运行测试
```bash
# 前端
npm run test                           # 全部测试
npm run test -- filename.test.tsx     # 单个文件

# E2E 测试（Playwright - 推荐）
npm run playwright:test                # 全部 Playwright 测试
npm run playwright:ui                  # 交互式 UI 模式
npm run playwright:headed              # 测试时显示浏览器
npx playwright test tests/auth/login.spec.ts  # 单个文件
npm run playwright:debug tests/auth/login.spec.ts  # 调试指定文件

# E2E 测试（Cypress - 已弃用）
cd superset-frontend/cypress-base
npm run cypress-run-chrome             # 全部 Cypress 测试（无头）
npm run cypress-debug                  # 交互式 Cypress UI

# 后端
pytest                                 # 全部测试
pytest tests/unit_tests/specific_test.py  # 单个文件
pytest tests/unit_tests/               # 目录

# 如果 pytest 因数据库/环境问题失败，请让用户运行测试环境初始化
```

## 环境验证

**快速设置检查（请先运行）：**

```bash
# 验证 Superset 是否运行
curl -f http://localhost:8088/health || echo "❌ 需要初始化设置 - 请参阅 https://superset.apache.org/docs/contributing/development#working-with-llms"
```

**如果健康检查失败：**
"看起来你的环境尚未正确配置。请参阅开发文档中的 [Working with LLMs](https://superset.apache.org/docs/contributing/development#working-with-llms) 章节获取设置说明。"

**关键项目文件：**
- `superset-frontend/package.json` - 前端构建脚本（`npm run dev` 在 9000 端口运行、`npm run test`、`npm run lint`）
- `pyproject.toml` - Python 工具配置（ruff、mypy 配置）
- `requirements/` 文件夹 - Python 依赖（base.txt、development.txt）

## SQLAlchemy 查询最佳实践
- **使用取反运算符**：使用 `~Model.field` 而不是 `== False`，以避免 ruff E712 报错
- **示例**：使用 `~Model.is_active` 而不是 `Model.is_active == False`

## 拉取请求指南

**创建拉取请求时：**

1. **阅读当前 PR 模板**：始终检查 `.github/PULL_REQUEST_TEMPLATE.md` 获取最新格式
2. **使用模板章节**：包含模板中的所有章节（SUMMARY、BEFORE/AFTER、TESTING INSTRUCTIONS、ADDITIONAL INFORMATION）
3. **遵循 PR 标题规范**：使用 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
   - 格式：`type(scope): description`
   - 示例：`fix(dashboard): load charts correctly`
   - 类型：`fix`、`feat`、`docs`、`style`、`refactor`、`perf`、`test`、`chore`

**重要**：始终引用实际的模板文件 `.github/PULL_REQUEST_TEMPLATE.md`，不要依赖缓存内容，因为模板可能会随时间更新。

## Pre-commit 验证

**使用 pre-commit 钩子进行质量验证：**

```bash
# 安装钩子
pre-commit install

# 重要：先暂存你的改动！
git add .                        # pre-commit 只检查已暂存文件

# 快速验证（比 --all-files 更快）
pre-commit run                   # 仅已暂存文件
pre-commit run mypy              # Python 类型检查
pre-commit run prettier          # 代码格式化
pre-commit run eslint            # 前端代码检查
```

**重要的 pre-commit 使用说明：**
- **先暂存文件**：运行 `pre-commit run` 前先执行 `git add .`，这样只检查改动文件（快得多）
- **虚拟环境**：运行 pre-commit 前先激活 Python 虚拟环境
  ```bash
  # 常见的虚拟环境位置（你的可能不同）：
  source .venv/bin/activate      # 若使用 .venv
  source venv/bin/activate       # 若使用 venv
  source ~/venvs/superset/bin/activate  # 若使用集中管理位置
  ```
  如果出现 "command not found" 错误，请询问用户应激活哪个虚拟环境
- **自动修复**：某些钩子会自动修复问题（例如去除行尾空格）。修复后请重新运行

## 常见文件模式

### API 结构
- **`/api.py`** - REST 端点，含装饰器和 OpenAPI 文档字符串
- **`/schemas.py`** - 用于 OpenAPI 规范的 Marshmallow 校验 schema
- **`/commands/`** - 业务逻辑类，使用 @transaction() 装饰器
- **`/models/`** - SQLAlchemy 数据库模型
- **OpenAPI 文档**：根据文档字符串和 schema 自动生成于 `/swagger/v1`

### 迁移文件
- **位置**：`superset/migrations/versions/`
- **命名**：`YYYY-MM-DD_HH-MM_hash_description.py`
- **工具**：使用 `superset.migrations.shared.utils` 中的辅助函数以保证数据库兼容性
- **模式**：导入工具函数，而不是直接执行原始 SQLAlchemy 操作

## 平台特定说明

- **[CLAUDE.md](CLAUDE.md)** - 适用于 Claude/Anthropic 工具
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - 适用于 GitHub Copilot
- **[GEMINI.md](GEMINI.md)** - 适用于 Google Gemini 工具
- **[GPT.md](GPT.md)** - 适用于 OpenAI/ChatGPT 工具
- **[.cursor/rules/dev-standard.mdc](.cursor/rules/dev-standard.mdc)** - 适用于 Cursor 编辑器

---

**LLM 注意**：本代码库正在积极向完整 TypeScript 和类型安全现代化。始终运行 `pre-commit run` 验证改动。遵循上述正在进行的重构章节，避免使用已弃用模式。
