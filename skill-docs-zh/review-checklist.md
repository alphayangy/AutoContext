# 自审 Checklist

AutoContext Step 7 的详细参考：写入前的自我审查。

## Review 检查清单

对生成的 `AGENTS.md` / `CLAUDE.md` / `.claude/rules/*.md` 逐项检查：

| # | 检查项 | 通过标准 | 不通过怎么办 |
|---|--------|---------|-------------|
| 1 | **Atom 来源可追溯** | `Working Rules` / `Verification` / `Safety` 每条末尾都有 `[atom-name]` | 删除无来源条目，或补 atom 标注 |
| 2 | **实际调用脚本渲染** | proposal 中 `Working Rules` / `Verification` / `Safety` 是 `tools/render-atoms.py` 的真实输出，没有 `[渲染内容]` / `<!-- 待渲染 -->` / 省略号占位 | 调用脚本并把完整输出粘贴进 proposal |
| 3 | **无 atom 改写** | 脚本输出与 atom 原文做 `diff`，除缩进和 bullet 标记外完全一致 | 改回 atom 原文；若 atom 原文不合适则 omit 该 atom |
| 4 | **展开完整保留** | 每条规则都有核心句 + 缩进展开；没有只剩一句口号 | 补回 atom 展开；调用脚本重新渲染 |
| 5 | **无流程泄漏** | 没有“先 X，再 Y，最后 Z”类的多步流程；没有 numbered steps 1/2/3 | 移到 `Reference Docs` 给指针，或建议做成 skill |
| 6 | **无项目事实混入 Working Rules** | Working Rules 里不出现具体命令、目录路径、文件名、工具参数 | 把项目事实移到 `Project Overview` / `Commands` / `Reference Docs` |
| 7 | **无过度 omit** | `priority: high` 和 `profiles: [all]` 的 atom 未被省略；omit 理由不是"全局已覆盖"或"看起来重叠" | 把不该省略的 atom 加回来 |
| 8 | **长度合规** | 每个文件 ≤ 200 行 | 拆分 `.claude/rules/`，或裁剪低优先级 atom |
| 9 | **无占位符** | 没有 `[TBD]`、`[待填]`、空括号等未填内容 | 删除或补全；无法补全的标 `[UNVERIFIED]` 并说明 |
| 10 | **无冲突规则** | 不存在互相矛盾的指令（例如“总是做 X” vs “绝不做 X”） | 保留更相关/更高优先级的一条，删除另一条 |
| 11 | **Agent 产物匹配** | 生成的文件与 `detected_agents` 一致（Claude → CLAUDE.md，多 agent → AGENTS.md 为主） | 按产物选择指南重新选择产物 |
| 12 | **项目事实准确** | `Project Overview` / `Commands` 里的技术栈、目录、命令与扫描到的文件一致 | 回 Step 1 重新检测 |
| 13 | **无重复 README 大段内容** | 没有从 `README.md` 整段复制进上下文文件 | 改成一句话摘要或指针 |
| 14 | **无 lint/format 规则口语化** | 没有把 ESLInt/Prettier/black 等格式规则写成自然语言大段 | 删除，交给项目已有 linter |
| 15 | **上下文文件引用方向正确** | 若同时存在 `CLAUDE.md` + `AGENTS.md`：`CLAUDE.md` 引用 `AGENTS.md`，`AGENTS.md` 不引用 `CLAUDE.md`；已通过 `tools/verify-context.py` | 按迁移指南修正引用方向，再运行脚本验证 |

## 反向抽查

抽查由脚本渲染的 atom 输出：

1. 随机抽取 3 个已渲染的 atom。
2. 用 `diff`（或重新调用 `tools/render-atoms.py` 对该 atom 单独渲染）对比脚本输出和 atom 原文。
3. 核心句 + 展开内容必须完全一致，除以下允许项外：
   - 行首缩进空格
   - bullet 标记 `-` / `*`
   - 行尾空白
4. 任何非允许差异 → 判定为 **atom 改写**，Review 不通过。

## Review 不能全是 ✅

**任何 proposal 都能找到至少一个可改进点。** 如果 Review 表 15 项全是 ✅，说明 Review 做得太松。必须至少找到一项：

- 某条可以删的 atom（M7：删了不会犯错）
- 某条表述可以更贴近 atom 原文
- 某条展开可以补回或压缩得更准确
- 某个项目事实可以改成更简洁的指针
- 某个 section 可以拆到 `.claude/rules/`

把至少一个改进点写进 Review 输出。

## Review 输出格式

把自审结果附加在 proposal 后面一起展示：

```md
---

## Auto Context Review

| 检查项 | 状态 | 说明 |
|--------|------|------|
| Atom 来源可追溯 | ✅ | 8/8 条已标注 `[atom-name]` |
| 无流程泄漏 | ⚠️ | `Pipeline 操作纪律` 含 4 步流程，需移除 |
| 长度合规 | ✅ | AGENTS.md 约 48 行，CLAUDE.md 约 12 行 |
| 无冲突规则 | ✅ | 未发现冲突 |

### 需修正的问题

1. **流程泄漏**：`## Working Standards` 下的 `Pipeline 操作纪律` 是 4 步操作流程，不是 atom。应改为：
   ```md
   ## Reference Docs (read when relevant)
   - `user_memory_inference/README.md` — 生产推理运行流程
   ```

2. **缺少 atom 来源**：`Prompt 工程` 小节无 `[atom-name]`，且内容来自 README。应删除或改为 Reference Docs 指针。

### 修正后的文件预览

[这里放修正后的 AGENTS.md / CLAUDE.md 预览]
```

## Review 不通过的处理

- **发现 atom 改写**：必须改回 atom 原文。如果 atom 原文确实不适合本项目，omit 该 atom 而不是改写。
- **发现 1-2 个小问题**（流程泄漏、项目事实位置不对、个别 atom 选错）：直接修正，不重新问用户。
- **发现结构性问题**（产物选择错误、大量流程泄漏、错误 Profile、过度 omit）：修正后重新生成 proposal，并重新 Review。
- **Review 表全 ✅**：退回重审，必须找到至少一个可改进点。
- **不确定是否算泄漏/改写**：按保守原则处理——“这是不是 atom 文件里有的句子？”不是则删或改。
