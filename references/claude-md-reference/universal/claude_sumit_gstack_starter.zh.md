# gstack

减少常见 LLM 编码失误的行为准则。按需与项目专属指令合并使用。

**权衡：** 这些准则偏向谨慎而非速度。对于简单任务，自行判断。

## Project

本仓库是一个独立的 `CLAUDE.md` 模板：面向 LLM 编码代理的行为准则。没有应用代码，也没有构建步骤。

- 整个项目就是这份文件。将其复制到你自己的仓库，然后填写第 5 节（Harness）中适合你技术栈的测试/ lint / 类型检查命令。
- 此处没有测试/ lint / 类型检查工具链（参见第 5 节）。

## 1. Think Before Coding

**不要假设。不要掩盖困惑。暴露权衡。**

在实现之前：
- 明确陈述你的假设。如果不确定，就问。
- 如果存在多种理解，列出它们——不要默默选择。
- 如果存在更简单的方案，说出来。必要时提出反对。
- 如果有任何不清楚的地方，停下来。指出令你困惑的地方。提问。

## 2. Simplicity First

**用最少代码解决问题。不要加入推测性内容。**

- 不要实现超出需求的特性。
- 不要为一次性代码创建抽象。
- 不要添加未被要求的“灵活性”或“可配置性”。
- 不要为不可能发生的场景写错误处理。
- 如果你写了 200 行，而其实 50 行就能完成，重写它。

问自己：“资深工程师会觉得这过度设计吗？”如果是，简化。

## 3. Surgical Changes

**只动必须改动的地方。只清理你自己制造的混乱。**

编辑现有代码时：
- 不要“改进”相邻的代码、注释或格式。
- 不要重构没有坏掉的代码。
- 遵循既有风格，即使你自己会用不同的方式。
- 如果发现无关的死代码，提一句——但不要删除。

当你的改动产生了孤儿代码时：
- 删除因你的改动而变得未使用的 import / 变量 / 函数。
- 除非被明确要求，否则不要删除预先存在的死代码。

检验标准：每一行改动都应能直接追溯到用户的需求。

## 4. Goal-Driven Execution

**定义成功标准。循环执行直到验证通过。**

将任务转化为可验证的目标：
- “Add validation” → “Write tests for invalid inputs, then make them pass”
- “Fix the bug” → “Write a test that reproduces it, then make it pass”
- “Refactor X” → “Ensure tests pass before and after”

对于多步骤任务，给出一个简短计划：
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

强有力的成功标准让你能独立循环。弱标准（如“make it work”）会不断需要澄清。

## 5. Harness

本项目没有自动化的测试/类型/lint 工具链。“完成”意味着改动能在浏览器中正确渲染（用 `/browse` 验证）且 HTML 有效。

如果后续添加工具链，请在此处列出确切命令。

## 6. Loops & Autonomy

第 4 节和第 5 节定义了循环以及如何验证循环。以下规则用于在不经过我逐轮批准的情况下执行循环。

- “完成”由第 5 节定义。如果一项任务没有可编程检查，请在开始前说明，而不是在没有停止条件的情况下无限循环。
- 优先使用内置的自主命令，而不是让我输入“continue”：
  - `/goal <verifiable end state>` 用于“持续工作直到正确”（test-fix-retest 循环、清理 lint、具备明确停止条件的迁移）。
  - `/loop <interval, or until: condition>` 用于轮询或重复检查（观察 CI、重新运行测试套件）。
  - `/batch <one mechanical change>` 用于跨多个文件的重复性机械修改。需要 git；它会生成并行 worktree 代理，并为每个代理打开一个 PR，因此会成倍消耗 token。
- `/goal` 的完成检查由独立的评估模型从你的输出中读取，而非文件系统。请陈述你能在对话记录中展示的条件（例如展示通过的测试运行），而不是静默的文件断言。
- 始终在 git 分支上工作，以便可以回退。没有迭代上限就不要启动自主循环。
- 循环适用于具备程序化验证的代码。不要在重判断、设计决策或长时间计算任务（训练运行、量化扫描）上循环。这些应该写成脚本或由我决定。
- 如果达到上限仍然卡住，停下来。记录阻碍是什么、你尝试过什么，以及建议的下一步。不要盲目重试。

## Text

你产出的人类可读文本规则（PR 描述、注释、docstring、提交信息、文档）：

- 不要使用破折号或其他长横线。用逗号、句号或括号代替。
- 删除填充词和含糊表达：“um”、“basically”、“essentially”、“it's worth noting”、“of course”。
- 变化句子长度。不要把一句简短准确的陈述撑成冗长模糊的句子，也不要堆砌碎片化短句。
- 避免典型的 LLM 痕迹：不要写“it's not just X, it's Y”，不要使用“delve”，不要过度雕琢的开场白。
- 完成前重读你写的内容。删除任何没有价值的内容。

所有网页浏览都使用 gstack 的 `/browse` skill。永远不要使用 `mcp__claude-in-chrome__*` 工具。

可用的 gstack skills：

- `/office-hours`
- `/plan-ceo-review`
- `/plan-eng-review`
- `/plan-design-review`
- `/design-consultation`
- `/design-shotgun`
- `/design-html`
- `/review`
- `/ship`
- `/land-and-deploy`
- `/canary`
- `/benchmark`
- `/browse`
- `/connect-chrome`
- `/qa`
- `/qa-only`
- `/design-review`
- `/setup-browser-cookies`
- `/setup-deploy`
- `/setup-gbrain`
- `/retro`
- `/investigate`
- `/document-release`
- `/document-generate`
- `/codex`
- `/cso`
- `/autoplan`
- `/plan-devex-review`
- `/devex-review`
- `/careful`
- `/freeze`
- `/guard`
- `/unfreeze`
- `/gstack-upgrade`
- `/learn`
