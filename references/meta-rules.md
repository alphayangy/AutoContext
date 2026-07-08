# AutoContext 元规则(Meta Rules)

这是 AutoContext 自己守的规则,不是输出给用户 agent 的准则,也不是给人的操作技巧。AutoContext 在生成/组合/维护上下文时自己遵守,不渲染进用户的项目文件。

三个文档职责不重叠:
- [`techniques-overview.md`](./techniques-overview.md):给 agent 的候选(atom / skill / Path Rule 评估)
- [`tips.md`](./tips.md):给人的操作技巧(触发/转述)
- `meta-rules.md`(本文件):AutoContext 自己守的元规则

来源:英文社区(HN / Reddit / Simon Willison / danluu / Anthropic / HumanLayer)、prompt 工程资源(Anthropic docs / promptingguide.ai)、中文社区(V2EX / GitHub)。

---

## M1. Right-Altitude 系统提示(Goldilocks 区)
- 来源:Anthropic context-engineering 文
- 描述:不要写脆弱的 if-else 硬编码行为,也不要写空泛高层口号,取中间"具体到能引导、松到能给启发式"。
- 用法:从"最小可用 prompt + 最强模型"起步,按失败模式逐步补具体指令/示例。

## M2. 通用 CoT 指令胜过手写步骤表
- 来源:Anthropic best-practices
- 描述:"think thoroughly" 这类泛指令常比人手写的分步计划更好。模型内禀推理常优于人类处方。
- 用法:优先用泛指令,只在失败时才逐步规定。

## M3. Layered Context Architecture(系统/任务/工具/记忆四层)
- 来源:promptingguide.ai/agents/context-engineering
- 描述:把 agent context 概念上分四层(system/task/tool/memory)分别工程化。

## M4. 过约束 vs 欠约束的纠偏
- 来源:promptingguide.ai
- 描述:"NEVER skip / ALWAYS exactly 3" 是过约束;"do some research" 是欠约束;给"aim to... 如果冗余先合并并记录理由"的中间态。

## M5. context validation 四问(completeness/clarity/consistency/testability)
- 来源:promptingguide.ai
- 描述:部署前用"覆盖全场景?无歧义?各部分一致?可验证?"四问审 context 设计。

## M6. 7 种指令机制决策表(选 artifact)
- 来源:claude.com/blog/steering-claude-code-skills-hooks-rules-subagents
- 描述:AutoContext 组合准则时,根据准则性质选渲染到哪个 artifact。不是给 agent 守的准则,是 AutoContext 自己的分发逻辑。
- 判断点:
  - "每次 X 总做 Y" → hook(确定性)
  - "绝对不做 Z" → PreToolUse hook exit 2(CLAUDE.md 的 never 在长会话或注入污染下失效)
  - "30 行流程" → skill(调用时载入)
  - "仅适用某路径" → path-scoped rule
  - "所有工程适用的事实" → CLAUDE.md(根)
  - "个人偏好" → ~/.claude/CLAUDE.md 或 CLAUDE.local.md

## M7. CLAUDE.md 每行问"删了会犯错吗"
- 来源:humanlayer.dev/blog/writing-a-good-claude-md
- 描述:AutoContext 生成 CLAUDE.md 时,每行问"删了 agent 会犯错吗",不会则删。不 universal 的行均匀摊薄所有指令的遵从度。
- 数据点:前沿 thinking 模型可靠跟随约 150-200 条指令;Claude Code 系统提示已占约 50 条,CLAUDE.md 一上来吃掉 1/3 预算。

## M8. CLAUDE.md 体积上限 + owner + review
- 来源:Anthropic steering 博客
- 描述:生成的 CLAUDE.md 保持 < 200 行;给负责人;改动像 code 一样 review。团队级配 claudeMdExcludes,monorepo 给每个 team 子目录自己的 CLAUDE.md。

## M9. Progressive disclosure:给指针不给副本
- 来源:humanlayer CLAUDE.md blog + centminmod/my-claude-code-setup
- 描述:AutoContext 生成 CLAUDE.md 时,详细内容拆到 agent_docs/*.md,CLAUDE.md 只列文件名 + 一句话描述让 agent 按需 read。不塞 code snippet(会过期),用 file:line references。
- 怎么用:CLAUDE.md 末尾放 "Topic cheatsheets (read only if relevant): - agent_docs/building_the_project.md - ..."

## M10. Stop hook 把验证变成确定性 gate
- 来源:Anthropic best-practices
- 描述:AutoContext 生成项目配置时,该用 Stop hook 把验证变确定性 gate,别只靠 CLAUDE.md 的 advisory。advisory(模型可能忘)→ deterministic(脚本强制,不通过不能结束 turn)。连续 8 次被 hook 阻止后强制结束(防死循环)。
- 四档渐强:同一 prompt 自纠 → /goal 设验证 → Stop hook(确定性)→ 子代理 verification
