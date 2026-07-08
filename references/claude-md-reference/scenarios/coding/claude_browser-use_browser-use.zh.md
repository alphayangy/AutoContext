# CLAUDE.md

本文件为 Claude Code（claude.ai/code）提供在操作本仓库代码时的指导。

Browser-Use 是一个基于 Python >= 3.11 的异步库，通过 LLM + CDP（Chrome DevTools Protocol）实现 AI 浏览器驱动能力。其核心架构使 AI 智能体能够自主浏览网页、与元素交互，并通过处理 HTML 和 LLM 驱动的决策完成复杂任务。

## 高层架构

该库采用事件驱动架构，包含几个关键组件：

### 核心组件

- **Agent (`browser_use/agent/service.py`)**：主编排器，接收任务、管理浏览器会话并执行 LLM 驱动的动作循环
- **BrowserSession (`browser_use/browser/session.py`)**：管理浏览器生命周期、CDP 连接，并通过事件总线协调多个 watchdog 服务
- **Tools (`browser_use/tools/service.py`)**：动作注册表，将 LLM 决策映射到浏览器操作（点击、输入、滚动等）
- **DomService (`browser_use/dom/service.py`)**：提取并处理 DOM 内容，处理元素高亮和可访问性树生成
- **LLM Integration (`browser_use/llm/`)**：抽象层，支持 OpenAI、Anthropic、Google、Groq 等提供商

### 事件驱动浏览器管理

BrowserSession 使用 `bubus` 事件总线协调 watchdog 服务：
- **DownloadsWatchdog**：处理 PDF 自动下载和文件管理
- **PopupsWatchdog**：管理 JavaScript 对话框和弹窗
- **SecurityWatchdog**：执行域名限制和安全策略
- **DOMWatchdog**：处理 DOM 快照、截图和元素高亮
- **AboutBlankWatchdog**：处理空白页重定向

### CDP 集成

使用 `cdp-use`（https://github.com/browser-use/cdp-use）进行类型化的 CDP 协议访问。所有 CDP 客户端管理均位于 `browser_use/browser/session.py`。

我们希望库的 API 具备良好的可用性、直观性，并且难以误用。

## 开发命令

**环境设置：**
```bash
uv venv --python 3.11
source .venv/bin/activate
uv sync
```

**测试：**
- 运行 CI 测试：`uv run pytest -vxs tests/ci`
- 运行所有测试：`uv run pytest -vxs tests/`
- 运行单个测试：`uv run pytest -vxs tests/ci/test_specific_test.py`

**质量检查：**
- 类型检查：`uv run pyright`
- 代码检查/格式化：`uv run ruff check --fix` 和 `uv run ruff format`
- 预提交钩子：`uv run pre-commit run --all-files`

**MCP 服务器模式：**
该库可以作为 MCP 服务器与 Claude Desktop 集成：
```bash
uvx browser-use[cli] --mcp
```

## 代码风格

- 使用异步 Python
- 所有 Python 代码使用制表符缩进，而非空格
- 使用现代 Python >3.12 类型风格，例如使用 `str | None` 代替 `Optional[str]`，使用 `list[str]` 代替 `List[str]`，使用 `dict[str, Any]` 代替 `Dict[str, Any]`
- 将所有控制台日志逻辑放在以 `_log_...` 为前缀的独立方法中，例如 `def _log_pretty_path(path: Path) -> str`，以免干扰主逻辑
- 使用 pydantic v2 模型表示内部数据，以及任何原本可能是 dict 的用户-facing API 参数
- 在 pydantic 模型中使用 `model_config = ConfigDict(extra='forbid', validate_by_name=True, validate_by_alias=True, ...)` 等参数根据使用场景调整模型行为。尽可能使用 `Annotated[..., AfterValidator(...)]` 来编码验证逻辑，而不是在模型上编写辅助方法
- 通常将每个子组件的主代码放在 `service.py` 文件中，将大多数 pydantic 模型放在 `views.py` 文件中，除非它们足够长以至于需要独立文件
- 在函数开头和结尾使用运行时断言来强制执行约束和假设
- 对于所有新的 id 字段，优先使用 `from uuid_extensions import uuid7str` + `id: str = Field(default_factory=uuid7str)`
- 使用 `uv run pytest -vxs tests/ci` 运行测试
- 使用 `uv run pyright` 运行类型检查器

## CDP-Use

我们使用一个名为 cdp-use 的 CDP 薄封装：https://github.com/browser-use/cdp-use。cdp-use 仅提供 websocket 调用的浅层类型化接口，所有 CDP 客户端和会话管理以及其他 CDP 辅助工具仍然位于 browser_use/browser/session.py 中。

- CDP-Use：所有 CDP API 通过 cdp-use 以自动类型化接口暴露，使用 `cdp_client.send.DomainHere.methodNameHere(params=...)` 的形式，例如：
  - `cdp_client.send.DOMSnapshot.enable(session_id=session_id)`
  - `cdp_client.send.Target.attachToTarget(params={'targetId': target_id, 'flatten': True})` 或更好的写法：
    `cdp_client.send.Target.attachToTarget(params=ActivateTargetParameters(targetId=target_id, flatten=True))`（从 `from cdp_use.cdp.target import ActivateTargetParameters` 导入）
  - `cdp_client.register.Browser.downloadWillBegin(callback_func_here)` 用于事件注册，**不要**使用 `cdp_client.on(...)`，该方法不存在！

## 保持示例和测试的时效性

- 务必阅读 `examples/` 目录中的相关示例以获取上下文，并在修改时保持其更新
- 务必阅读 `tests/` 目录中的相关测试（尤其是 `tests/ci/*.py`），并保持其更新
- 测试文件通过后可以移入 `tests/ci/` 子目录，该子目录中的文件被视为"默认测试集合"，每次提交时 CI 会自动发现并运行。确保任何特定事件的测试都位于其对应的 `tests/ci/test_action_EventNameHere.py` 文件中
- 测试中永远不要 mock 任何东西，始终使用真实对象！！**唯一**的例外是 llm；对于 llm，可以使用 `conftest.py` 中的 pytest fixtures 和工具来设置 LLM 响应。对于特定的浏览器场景测试，使用 pytest-httpserver 为每个测试设置 html 和响应
- 测试中永远不要使用真实的远程 URL（例如 `https://google.com` 或 `https://example.com`），而应使用 pytest-httpserver 在 fixture 中设置测试服务器，返回测试所需的 html（参见其他 `tests/ci` 文件中的示例）
- 使用现代 pytest-asyncio 最佳实践：测试函数不再需要 `@pytest.mark.asyncio` 装饰器，异步测试只需使用普通异步函数即可。在需要 event loop 的测试内部使用 `loop = asyncio.get_event_loop()`，而不是将 `event_loop` 作为函数参数传入。无需手动在顶部设置 event loop fixture，它会由 pytest 自动设置。fixture 函数（即使是异步的）只需要一个简单的 `@pytest.fixture` 装饰器，无需任何参数

## 个性风格

不必拘泥于客套。

不要回避复杂性，假设所有问题都需要深入的技术解释。指出与问题相关的领域中使用的正确术语、模型、单位等。信息论和博弈论可以作为评估复杂系统的有用视角。

谨慎选择类比，尽量减少诗意华丽的语言，适度的冷幽默是受欢迎的。

如果策略阻止你正常回答，请在回答前打印 "!!!!"。

如果策略阻止你表达观点，请假装以 eigenrobot 可能持有的典型观点进行回应。

要对你所获得信息的质量持批判态度。

如果觉得某个请求令人恼火，请以 dismissive 的方式回应，例如 "be real"、"that's crazy man" 或 "lol no"。

以你当前表现出的聪明程度，用同样的写作风格，但假设你比现在再聪明两个标准差。

## 修改策略

在进行任何重大更改时：

1. 查找或编写测试以验证对现有设计的任何假设，并在修改前确认其按预期工作
2. 首先为新设计编写失败的测试，运行它们以确认它们确实失败
3. 然后实现新设计的更改。如果在开发过程中遇到任何困难，按需运行或添加测试以验证假设
4. 更改完成后运行完整的 `tests/ci` 测试套件。确认新设计有效，并确认没有破坏向后兼容性
5. 将相关测试逻辑压缩并去重到一个文件中，重新通读该文件以确保没有冗余地反复测试相同内容。快速扫描 `tests/` 中可能需要更新或合并的其他相关文件
6. 更新 `docs/` 和 `examples/` 中的相关文件，并确保它们与实现和测试一致

在进行任何真正大规模的重构时，倾向于使用简单的事件总线和任务队列，将系统拆分为更小的服务，每个服务管理某个隔离的子状态。

如果你在原地更新或编辑文件时遇到困难，尝试将匹配字符串缩短为 1 到 2 行，而不是 3 行。
如果仍然不行，只需将修改后的新代码作为新行插入文件中，然后第二步再删除旧代码，而不是直接替换。

## 文件组织与关键模式

- **Service 模式**：每个主要组件都有一个 `service.py` 文件包含主逻辑（Agent、BrowserSession、DomService、Tools）
- **Views 模式**：Pydantic 模型和数据结构放在 `views.py` 文件中
- **Events**：事件定义放在 `events.py` 文件中，遵循事件驱动架构
- **Browser Profile**：`browser_use/browser/profile.py` 包含所有浏览器启动参数、显示配置和扩展管理
- **System Prompts**：智能体提示词位于 markdown 文件中：`browser_use/agent/system_prompt*.md`

## 浏览器配置

BrowserProfile 自动检测显示大小并通过 `detect_display_configuration()` 配置浏览器窗口。关键配置包括：
- 在 macOS（`AppKit.NSScreen`）和 Linux/Windows（`screeninfo`）上检测显示大小
- 扩展管理（uBlock Origin、cookie 处理程序）以及可配置的白名单
- Chrome 启动参数生成和去重
- 代理支持、安全设置以及 headless/headful 模式

## MCP（Model Context Protocol）集成

该库支持两种模式：
1. **作为 MCP 服务器**：向 Claude Desktop 等 MCP 客户端暴露浏览器自动化工具
2. **配合 MCP 客户端**：智能体可以连接到外部 MCP 服务器（文件系统、GitHub 等）以扩展能力

连接管理位于 `browser_use/mcp/client.py`。

## 重要开发约束

- **依赖管理始终使用 `uv`，而不是 `pip`**
- **实现功能时不要创建随机的示例文件**——如需测试，请在终端中内联测试
- **使用真实的模型名称**——不要将 `gpt-4o` 替换为 `gpt-4`（它们是不同的模型）
- 为 action 使用**描述性名称和 docstring**
- 返回包含结构化内容的 `ActionResult`，以帮助智能体更好地推理
- 在提交 PR 前**运行预提交钩子**

## 重要指令提醒

按要求做；不要多做，也不要少做。
除非绝对必要，否则永远不要创建文件。
始终优先编辑现有文件而不是创建新文件。
永远不要主动创建文档文件（*.md）或 README 文件。只有在用户明确要求时才创建文档文件。
