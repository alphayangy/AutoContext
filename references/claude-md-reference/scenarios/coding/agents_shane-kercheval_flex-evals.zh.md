# flex-evals 项目执行手册

**⚡ AI 编码智能体指南 ⚡**

本手册是 AI 编码智能体与人类开发者使用 flex-evals 代码库的主要指南。它记录现有模式、约定和工作流，以确保开发的一致性。

---

## 1. 项目概览

**flex-evals** 是**灵活评估协议（Flexible Evaluation Protocol，FEP）**的 Python 实现，这是一种供应商无关、由模式驱动的标准，用于评估任何产生复杂或可变输出的系统——从确定性 API 到非确定性 LLM 以及智能体工作流。

### 关键技术

- **Python 3.11+**：使用现代类型提示与 async/await 模式
- **Pydantic**：用于模式验证与数据建模
- **JSONPath**：用于从评估上下文中动态提取数据
- **uv**：用于快速的依赖管理与构建流程
- **Pytest**：用于全面的测试，支持异步
- **Ruff**：用于代码检查与格式化

### 架构理念

- **注册表模式**：使用基于装饰器的注册机制实现可插拔的检查系统
- **异步优先**：自动检测并以最优方式执行同步/异步检查
- **模式驱动**：Pydantic 模型确保符合 FEP 协议
- **JSONPath 集成**：动态参数解析，灵活访问数据
- **错误上下文**：丰富的异常层级，提供详细的调试信息

---

## 2. 项目结构

```
~/repos/flex-evals/
├── src/flex_evals/           # 主包源码
│   ├── __init__.py          # 公共 API 导出
│   ├── engine.py            # 核心 evaluate() 函数
│   ├── registry.py          # 检查注册系统
│   ├── constants.py         # 字符串枚举（CheckType、Status 等）
│   ├── exceptions.py        # 自定义异常层级
│   ├── jsonpath_resolver.py # JSONPath 表达式处理
│   ├── checks/              # 检查实现
│   │   ├── base.py         # BaseCheck 与 BaseAsyncCheck 抽象
│   │   ├── standard/       # 内置同步检查
│   │   │   ├── exact_match.py
│   │   │   ├── contains.py
│   │   │   ├── regex.py
│   │   │   └── threshold.py
│   │   └── extended/       # 异步检查（LLM、API 调用）
│   │       ├── llm_judge.py
│   │       ├── semantic_similarity.py
│   │       └── custom_function.py
│   └── schemas/            # FEP 协议的 Pydantic 模型
│       ├── test_case.py    # TestCase 数据模型
│       ├── output.py       # Output 数据模型
│       ├── check.py        # Check 与 CheckResult 模型
│       ├── results.py      # 评估结果模型
│       └── experiments.py  # 实验元数据
├── tests/                  # 完整测试套件
│   ├── conftest.py        # 测试配置与 fixtures
│   ├── test_*.py          # 按模块组织的单元测试
│   └── test_schemas/      # 模式验证测试
├── examples/              # 用法示例与演示
│   ├── quickstart.ipynb   # 入门指南
│   ├── llm-as-a-judge.ipynb
│   ├── test_cases.yaml    # YAML 配置示例
│   └── *.json            # 样本评估数据
├── .github/workflows/     # CI/CD 配置
├── pyproject.toml        # 项目元数据与依赖
├── Makefile             # 开发命令
├── .ruff.toml          # 代码检查配置
└── uv.lock            # 依赖锁定文件
```

### 关键文件及其作用

**核心入口：**

- `src/flex_evals/__init__.py` - 公共 API 导出
- `src/flex_evals/engine.py` - 主 `evaluate()` 函数
- `src/flex_evals/registry.py` - 检查注册系统

**配置文件：**

- `pyproject.toml` - 项目元数据、依赖、pytest 配置
- `.ruff.toml` - 代码检查规则与代码风格配置
- `Makefile` - 开发工作流命令
- `uv.lock` - 用于可复现构建的精确依赖版本

**文件命名约定：**

- **模式文件**：`{entity}.py`（例如 `test_case.py`、`check.py`）
- **检查实现**：`{check_name}.py`（例如 `exact_match.py`）
- **测试文件**：`test_{module_name}.py`（例如 `test_engine.py`）
- **示例文件**：描述性名称并带扩展名（`.ipynb`、`.yaml`、`.json`）

### 目录组织模式

**代码归属：**

- **核心逻辑**：`src/flex_evals/`（引擎、注册表、工具）
- **数据模型**：`src/flex_evals/schemas/`（仅 Pydantic 模型）
- **检查实现**：`src/flex_evals/checks/standard/` 或 `extended/`
- **测试**：`tests/`，结构与 `src/` 对应
- **示例**：`examples/`，用于演示与教程
- **文档**：根目录文件（`README.md`、本手册）

---

## 3. 快速开始

### 前提条件

- **Python 3.11 或更高版本**
- **uv** 包管理器（推荐）或 pip

### 环境配置

项目使用 `uv` 进行依赖管理，它会自动处理虚拟环境。开发无需额外环境配置。

**环境变量：**

- 核心功能不需要环境变量
- 个别检查可能需要 API 密钥（例如用于 LLM judge 检查）
- 测试执行使用 `pyproject.toml` 中的 pytest 配置

---

## 4. 开发工作流

### 在本地运行项目

**核心评估函数：**

```python
from flex_evals import evaluate, TestCase, Output, Check, CheckType

# 定义测试用例
test_cases = [TestCase(id='test_001', input="What is 2+2?", expected="4")]

# 待评估的系统输出
outputs = [Output(value="The answer is 4")]

# 定义检查
checks = [Check(type=CheckType.CONTAINS, arguments={'text': '$.output.value', 'phrases': ['4']})]

# 执行评估
results = evaluate(test_cases, outputs, checks)
print(f"Status: {results.status}")
```

### 开发服务器/环境命令

**主要开发命令：**

```bash
# 安装/更新依赖
uv add <package>              # 添加新的依赖
uv add --dev <package>        # 添加开发依赖
uv sync                       # 与 lock 文件同步依赖

# 代码质量
make linting                  # 运行 ruff 检查并自动修复
make unittests               # 运行 pytest 并生成覆盖率报告
make tests                   # 运行所有质量检查

# 包管理
make package-build           # 构建分发包
make package                 # 构建并发布（需要 UV_PUBLISH_TOKEN）
```

### 环境变量与配置

**开发配置：**

- **Pytest**：在 `pyproject.toml` 中配置，支持异步、超时与路径设置
- **Ruff**：在 `.ruff.toml` 中配置，包含全面的规则集
- **Coverage**：在 `htmlcov/` 目录生成 HTML 报告

**无持久化配置文件** - uv 会自动管理环境。

### 代码重载/热重载能力

**开发时：**

- 使用 `uv run` 执行脚本，以应用最新代码变更
- Jupyter notebook 使用 `%load_ext autoreload` 时会自动重载
- 测试直接运行当前代码，无需编译步骤

---

## 5. 代码标准与规范

### 语言特定约定

**类型提示（遵循现有模式）：**

```python
# ✅ 现代 Python 风格（项目标准）
def process_items(items: list[str]) -> dict[str, Any]:
    results: dict[str, int] = {}
    return results

# ❌ 避免使用旧版 typing 导入
from typing import List, Dict  # 不要这样使用
```

### 命名约定

**遵循整个代码库的现有模式：**

- **文件**：`snake_case.py`（例如 `exact_match.py`、`test_case.py`）
- **类**：`PascalCase`（例如 `ExactMatchCheck`、`TestCase`）
- **函数/方法**：`snake_case`（例如 `evaluate`、`resolve_arguments`）
- **变量**：`snake_case`（例如 `test_cases`、`check_results`）
- **常量**：`SCREAMING_SNAKE_CASE`（例如 `DEFAULT_TIMEOUT`）
- **枚举**：类名为 `PascalCase`，值为 `SCREAMING_SNAKE_CASE`（例如 `CheckType.EXACT_MATCH`）

---

## 6. 测试

### 测试框架与配置

**框架：** pytest，支持异步、覆盖率报告与超时处理

**配置位置：** `pyproject.toml`

### 测试文件组织与命名

**遵循现有测试组织模式：**

```
tests/
├── conftest.py                    # 共享 fixtures 与测试配置
├── test_evaluation_engine.py     # engine.py 的测试
├── test_standard_checks.py       # 标准检查的测试
├── test_extended_checks.py       # 异步检查的测试
├── test_registry.py              # 注册系统的测试
└── test_schemas/                 # 模式验证测试
    ├── test_check.py
    ├── test_output.py
    └── test_results.py
```

**命名约定：**

- 测试文件：`test_{module_name}.py`
- 测试类：`Test{ClassName}`
- 测试方法：`test_{specific_behavior}`

### 如何运行不同类型的测试

```bash
# 使用覆盖率运行全部测试
make unittests

# 运行指定测试文件
uv run pytest tests/test_evaluation_engine.py

# 运行指定测试方法
uv run pytest tests/test_evaluation_engine.py::TestEvaluationEngine::test_evaluate_function_signature

# 带输出运行测试
uv run pytest -v tests/

# 并行运行测试（如已安装）
uv run pytest -n auto tests/
```

### 测试模式与约定

**遵循现有 pytest 测试模式：**

### 覆盖率工具与期望

**覆盖率配置：** 使用 `coverage` 生成 HTML 报告

- **位置：** 覆盖率报告生成在 `htmlcov/`
- **命令：** `uv run coverage html`（已包含在 `make unittests` 中）
- **目标：** 对新代码保持高覆盖率，尤其是核心逻辑

---

## 7. 代码质量与维护

### 代码检查工具与配置

**主要工具：** Ruff（替代 flake8、black、isort 等）

- **配置：** `.ruff.toml`
- **命令：** `make linting`（包含自动修复）

### 代码格式化标准

**遵循现有格式化模式：**

- **行长度：** 99 个字符（在 ruff 中配置）
- **缩进：** 4 个空格（Python 标准）
- **字符串引号：** 字符串使用双引号，短字面量使用单引号
- **导入排序：** 由 ruff 自动处理（标准库、第三方、本地）

### 预提交钩子与 CI 质量门

**CI 配置：** `.github/workflows/tests.yaml`

- **触发：** 推送到 main、对 main 的 PR（忽略 README.md 变更）
- **Python 版本：** 3.11、3.12、3.13
- **步骤：** 安装依赖、运行 lint、运行单元测试

**质量门：**

1. **Lint 必须通过：** `make linting`
2. **单元测试必须通过：** `make unittests`
3. **覆盖率报告：** 自动生成

### 如何在本地运行质量检查

```bash
# 运行所有质量检查（lint + 测试）
make tests

# 仅运行 lint 并自动修复
make linting

# 仅运行单元测试并生成覆盖率
make unittests

# 手动运行 ruff 命令
uv run ruff check src/flex_evals/ --fix
uv run ruff check tests/ --fix
uv run ruff check examples/ --fix
```

### 构建系统与依赖管理

**构建系统：** Hatchling（在 `pyproject.toml` 中配置）

```toml
[build-system]
requires = ["hatchling>=1.17.1"]
build-backend = "hatchling.build"
```

**依赖管理：**

```bash
# 添加新的依赖
uv add jsonpath-ng>=1.6.0           # 运行时依赖
uv add --dev pytest>=8.4.0          # 开发依赖

# 与 lock 文件同步
uv sync

# 构建包
make package-build                   # 创建 dist/ 目录
```

---

## 8. 项目特定指南

### 重要架构决策

**1. 检查注册表模式**

- 所有检查均使用 `@register` 装饰器自注册
- 实现动态检查发现与可插拔架构
- 支持版本控制与冲突检测

**2. 异步/同步自动检测**

- 引擎通过内省 `__call__` 方法自动检测异步检查
- 直接运行同步检查，并发运行异步检查，以优化执行
- 无论执行模式如何，都保持结果顺序

**3. JSONPath 参数解析**

- 以 `$.` 开头的参数被视为 JSONPath 表达式
- 可访问完整评估上下文：`$.test_case.*`、`$.output.*`
- 使用 `\\$.` 转义以 `$.` 开头的字面字符串

**4. 模式驱动开发**

- 所有数据结构均为 Pydantic 模型，确保类型安全
- 在模型创建时即进行验证
- 对无效数据提供清晰的错误信息

### 性能考虑与优化

**异步并发控制：**

```python
# 使用 max_async_concurrent 避免压垮外部 API
result = evaluate(
    test_cases, outputs, checks,
    max_async_concurrent=10  # 限制并发异步操作数
)
```

**并行处理：**

```python
# 对 CPU 密集型工作负载使用 max_parallel_workers
result = evaluate(
    test_cases, outputs, checks,
    max_parallel_workers=4  # 并行处理测试用例
)
```

**内存效率：**

- 尽可能对大数据集使用生成器
- 增量处理结果，而非全部存入内存
- 注册表状态会被序列化给并行工作进程，以保持检查可用

### 组件间集成模式

**检查注册模式：**

```python
# 导入即自动注册检查
import flex_evals.checks.standard  # 注册所有标准检查
import flex_evals.checks.extended  # 注册所有扩展检查

# 自定义注册
from flex_evals.registry import register
@register("custom_check", version="1.0.0")
class CustomCheck(BaseCheck): ...
```

**错误处理集成：**

```python
# 遵循现有错误传播模式
try:
    result = evaluate(test_cases, outputs, checks)
except ValidationError as e:
    # 处理验证错误
    logger.error(f"Validation failed: {e}")
except Exception as e:
    # 处理意外错误
    logger.error(f"Evaluation failed: {e}")
```

---

## 9. 命令参考

### 常用命令

**安装与设置：**

```bash
uv install --dev              # 安装所有依赖，包括开发工具
uv sync                       # 与 lock 文件同步依赖
uv add <package>              # 添加新的运行时依赖
uv add --dev <package>        # 添加新的开发依赖
```

**开发工作流：**

```bash
make tests                    # 运行所有质量检查（lint + 测试）
make linting                  # 运行 ruff lint 并自动修复
make unittests               # 运行 pytest 并生成覆盖率报告
```

**运行代码：**

```bash
uv run python <script.py>    # 在项目环境中运行 Python 脚本
uv run pytest <test_file>    # 运行指定测试
```

### 包管理

**添加依赖：**

```bash
uv add "requests>=2.32.4"               # 添加带版本约束的运行时依赖
uv add --dev "pytest>=8.4.0"            # 添加开发依赖
uv add --optional ml "scikit-learn"     # 添加到可选依赖组
```

### 测试命令

**基础测试：**

```bash
uv run pytest                           # 运行所有测试
uv run pytest tests/test_engine.py      # 运行指定测试文件
uv run pytest -k "test_exact_match"     # 运行匹配模式的测试
uv run pytest -v                        # 详细输出
uv run pytest --tb=short               # 短 traceback 格式
```

**覆盖率与报告：**

```bash
uv run coverage run -m pytest          # 运行测试并收集覆盖率（已包含在 make unittests 中）
uv run coverage report                 # 在终端显示覆盖率报告
uv run coverage html                   # 生成 HTML 覆盖率报告
open htmlcov/index.html                # 查看覆盖率报告（macOS）
```

**性能测试：**

```bash
uv run pytest --durations=10           # 显示最慢的 10 个测试
uv run pytest --timeout=30             # 设置测试超时
```

### 构建与质量

**代码质量：**

```bash
uv run ruff check src/                 # 检查 lint 问题
uv run ruff check --fix src/           # 自动修复 lint 问题
uv run ruff format src/                # 格式化代码（已包含在 check --fix 中）
```

---

## 10. 安全准则

### ⚠️ 禁止操作

**版本控制操作：**

```bash
# ❌ 切勿执行以下操作
git commit -m "message"       # 不要提交变更
git push origin main          # 不要推送到远程
git branch new-feature        # 不要创建分支
git merge feature-branch      # 不要合并分支
git tag v1.0.0               # 不要创建标签
git reset --hard HEAD~1      # 不要重置提交
```

**破坏性文件操作：**

```bash
# ❌ 切勿执行以下操作
rm -rf src/                   # 不要删除源代码
rm -rf .git/                  # 不要删除 git 历史
rm -rf tests/                 # 不要删除测试
mv src/ old_src/             # 不要移动关键目录
```

（删除单个文件通常是安全的，但避免删除关键目录或文件。）

**系统级变更：**

```bash
# ❌ 切勿执行以下操作
sudo pip install <package>   # 不要全局安装
pip install --system <pkg>   # 不要修改系统 Python
chmod -R 777 .               # 不要大范围修改权限
chown -R root:root .         # 不要修改所有者
```

**外部服务调用：**

```bash
# ❌ 切勿执行以下操作
curl -X POST https://api.production.com/deploy    # 不要调用生产 API
make package && uv publish                        # 不要发布包（会产生费用）
docker push production/image                       # 不要推送到生产镜像仓库
```

**数据安全：**

```bash
# ❌ 切勿执行以下操作
rm uv.lock                   # 不要删除锁定文件
rm pyproject.toml            # 不要删除项目配置
mv .env.example .env && git add .env  # 不要提交密钥
```

### ✅ 安全操作

**推荐的开发活动：**

- 阅读与分析代码
- 运行测试（`make tests`、`uv run pytest`）
- 运行代码检查（`make linting`）
- 在合适目录中创建新文件
- 按照既定模式修改现有代码
- 通过 `uv add` 添加依赖（非破坏性）
- 在本地构建包（`make package-build`）
- 运行示例与 notebook
- 调试与排查问题

**安全的文件操作：**

- 在 `tests/` 中创建新测试文件
- 在 `checks/` 中创建新检查实现
- 修改现有文件以修复缺陷或添加功能
- 在 `examples/` 中创建示例文件
- 添加文档

---

## 11. 手册维护

**📋 给 AI 编码智能体的重要提示：**

随着项目演进，应**及时更新**本手册。在对代码库进行重大变更时：

1. **更新相关章节**，以反映新模式
2. **在命令参考中添加新命令**
3. **更新故障排查**，补充新发现的常见问题
4. **修改代码示例**，使其与当前实现保持一致
5. **添加新的安全准则**，以覆盖可能出现的新操作
