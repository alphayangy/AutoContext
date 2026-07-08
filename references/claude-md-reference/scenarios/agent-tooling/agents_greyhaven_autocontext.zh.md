# 代理指南

将本文件作为需要在本仓库中工作或与仓库交互的编码代理和自动化工具的首要入口。

## 选择正确的入口

- 完整的 autocontext 控制平面：`autocontext/`
- Node/TypeScript 工具包与 CLI：`ts/`
- 交互式终端 UI：`ts/src/tui/`
- 外部代理使用指南：`autocontext/docs/agent-integration.md`

## 工作目录

- 从 `autocontext/` 运行 Python 命令。
- 从 `ts/` 运行 Node/TypeScript 命令。
- 从 `ts/` 运行与 TUI 相关的命令。

README 中大多数仓库级命令都假设当前工作目录是上述某个包目录。

## 环境搭建

Python：

```bash
cd autocontext
uv venv
source .venv/bin/activate
uv sync --group dev
```

TypeScript：

```bash
cd ts
npm install
```

## 延后保持一致性的改动

除非跨运行时的功能一致性在同一版本中对外可见，否则先在一个运行时中实现。如果延后保持一致性，请在 PR 中说明位置及原因。

## 常用检查

Python：

```bash
cd autocontext
uv run ruff check src tests
uv run mypy src
uv run pytest
```

TypeScript：

```bash
cd ts
npm run lint
npm test
```

## 需要同步更新的公开文档

如果你改动了公开命令、环境变量、包名或面向代理的工作流程，请在同一次变更中更新相关文档：

- `README.md`
- `docs/README.md`
- `autocontext/README.md`
- `ts/README.md`
- `examples/README.md`
- `autocontext/docs/agent-integration.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`

## 关键参考

- 仓库概览：`README.md`
- 文档概览：`docs/README.md`
- 贡献者流程：`CONTRIBUTING.md`
- Python 包指南：`autocontext/README.md`
- TypeScript 包指南：`ts/README.md`
- 复制粘贴示例：`examples/README.md`
- 外部代理指南：`autocontext/docs/agent-integration.md`

## 有意识的删除

- 在恢复已删除模块以使 CI 通过之前，检查 `autocontext/src/` 是否仍在导入它们。
- 如果只有测试失败，优先考虑重写或删除测试，而不是恢复已移除的模块。
- 在调用方重新接线或删除被明确接受为破坏性变更之前，将可导入模块路径视为兼容性界面。
