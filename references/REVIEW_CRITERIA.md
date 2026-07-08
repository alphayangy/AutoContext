# 参考资料审核标准

Auto Context 的参考收集不是越多越好。每个来源先按同一套标准判断，再决定进入哪里。

## 评分维度

| 维度 | 问题 | 高分表现 |
| --- | --- | --- |
| Agent-facing | 内容是不是直接写给 coding agent / Claude Code / Codex 看的？ | 明确告诉 agent 如何理解项目、工作、约束。 |
| Project-context | 是不是描述真实项目上下文，而不是泛泛教程、工具说明或个人目录习惯？ | 包含项目结构、命令、工作流、边界、不变量。 |
| Transferability | 能不能去掉项目名后抽成可复用准则？ | 可拆成通用准则或明确场景准则。 |
| Specificity | 有没有具体、可执行、可验证的信息？ | 有命令、路径、测试、判断标准、禁止事项。 |
| Signal-to-noise | 个人化、模板化、营销化、重复内容是否少？ | 少废话，少个人路径，少空泛 best practice。 |

## 等级

| 等级 | 去向 | 判断 |
| --- | --- | --- |
| A | `references/claude-md-reference/` | 真实项目里的高质量 `CLAUDE.md` / `AGENTS.md`，可直接抽准则。 |
| B | `references/claude-md-reference/` | 有噪声，但能抽出明确场景准则。索引里标注限制。 |
| C | `references/reviewed-out/` | 看过，有少量启发，但不适合进入核心样本池。保留证据和原因。 |
| D | 不保存正文，只在来源索引里记一行 | README、博客、awesome list、工具说明、明显无关内容。 |

## 审核动作

1. 先判断来源类型：真实项目样本、模板、工具说明、文章、awesome list。
2. 再按五个维度打结论，不因为文件名叫 `CLAUDE.md` 就自动收录。
3. A/B 才进入 `claude-md-reference`。
4. C 移到 `reviewed-out`，避免污染核心样本，也避免重复审核。
5. D 直接跳过；如果已经下载且需要留痕，放到 `reviewed-out`。

## 对当前项目最有价值的样本

优先找这几类：

- 真实工程项目的 `CLAUDE.md` / `AGENTS.md`。
- 非代码项目但明确写给 agent 的上下文，例如文档库、研究项目、知识库。
- 短小但高密度的 agent 行为准则。
- 能体现“少问问题但拿到关键信息”的上下文组织方式。

低优先级：

- 个人工作区模板。
- 大而全的 Claude Code 教程。
- command / skill / MCP 工具 README。
- 带大量个人路径、个人偏好、安装说明的模板库。
