# AGENTS.md

本文件为在仓库中编写代码的 AI 编码助手提供工作指导。

## 快速参考

**项目类型**: 数据集成平台（ELT/ETL）
**语言**: Python 3.10+
**包管理器**: `uv`
**任务运行器**: `nox`
**测试**: `pytest`，支持多种数据库后端
**代码检查与格式化**: `ruff`
**类型检查**: `mypy` + `ty`

## 开发命令

### 包管理

- 安装依赖: `uv sync --all-extras --all-groups`

### 测试

- 运行特定测试: `uv run pytest tests/path/to/test.py::test_function`
- 运行全部测试: `nox -t test` 或 `nox -s pytest`
- 在单一 Python 版本上运行部分测试: `nox -p 3.14 -s pytest -- tests/meltano/core/state_store`
- 使用指定后端运行: `PYTEST_BACKEND=postgresql nox -s pytest`

### 代码检查、格式化与类型检查

- 运行全部代码检查: `nox -t lint`
- 仅运行类型检查: `nox -s typing`
- 仅运行 pre-commit 检查: `nox -s pre-commit`

### 开发工作流

开发任务请使用 `nox` —— 它会自动管理虚拟环境和依赖：

```bash
nox -l  # 列出可用会话
nox     # 运行默认会话（mypy、pre-commit、pytest）
```

## GitHub

向 GitHub 提交 pull request 时，请以仓库中的 `.github/pull_request_template.md` 为基础来编写描述。请注意，未使用该模板可能导致 PR 被直接关闭。

## 编码规范

- 所有新代码必须添加类型注解。类型检查的运行方式见上文。
- 注意 asyncio 开销，例如 https://github.com/meltano/meltano/pull/9724。
- 核心功能围绕专门的服务类组织，新增核心功能通常应从实现新的服务类开始。这些类通常不是抽象基类，但 `SettingsService` 除外。
- 请继承并抛出 `MeltanoError`，以向用户提供可执行的错误信息和明确的后续步骤。
- 测试结构应与源码结构保持一致
- `tests/meltano/cli/` 中的集成测试覆盖完整 CLI 工作流
- 请对外部依赖进行模拟（例如使用 `unittest.mock`）
