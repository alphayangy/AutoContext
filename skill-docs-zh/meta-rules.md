# AutoContext 元规则

执行 AutoContext 时遵循的规则，不渲染进用户的项目文件。

1. **少生成，而不是多生成**：没检测到的项目事实不编；没必要的 atom 不召回。
2. **先审再写**：默认生成 proposal 并通过 Review 后直接落盘；Review 不通过时不写。
3. **不覆盖已有文件**：已有上下文文件走 review/patch 模式。
4. **CLAUDE.md < 200 行**：超出时拆分 `.claude/rules/`，而不是把文件写长。
5. **Profile 是召回维度，不是产物**：不要把 Profile 名称写进最终 `CLAUDE.md`。
6. **流程不进 CLAUDE.md**：多步骤流程应建议做成 `.claude/skills/`，不塞进项目上下文文件。
7. **同一条准则只在一处**：不在 `CLAUDE.md` 和 `AGENTS.md` 中重复。
8. **优先检测 Agent 再选产物**：根据 `detected_agents` 决定输出文件，不默认给所有项目写 `CLAUDE.md`。
9. **多 Agent 以 AGENTS.md 为单源**：各工具原生文件只 import / 引用 `AGENTS.md`，不复制内容。
10. **项目事实与 atoms 必须分离**：项目事实只进 `Project Overview` / `Commands` / `Reference Docs`；atoms 只进 `Working Rules` / `Verification` / `Safety`。
11. **全局 CLAUDE.md 不免除项目 atom**：检测到全局 `~/.claude/CLAUDE.md` 时，不因此省略本项目的通用 atom。全局是用户偏好，项目是项目约束，两者不互斥。
12. **写入前必须自审**：每次生成 proposal 后，执行 Review 检查清单。不通过就修正，修正后再写入；不把有问题的文件直接落盘。
13. **禁止改写 atom 原文**：`Working Rules` / `Verification` / `Safety` 必须通过 `tools/render-atoms.py` 渲染，不准许 LLM 手工改写、压缩或重新表述。
14. **高优先级 atom 默认保留**：`priority: high` 和 `profiles: [all]` 的 atom 不随意省略。省略必须给出"不保留会导致什么具体错误"的证据。
15. **Review 必须反向抽查**：随机抽取 3 个已渲染 atom，用 `diff` 对比脚本输出和 atom 原文。核心句 + 展开必须完全一致（除缩进和 bullet 标记外）。
16. **Review 不能全 ✅**：任何 proposal 至少存在一个可改进点。全 ✅ 说明 Review 太松，需要重审。
17. **规则必须带展开**：`Working Rules` / `Verification` / `Safety` 不能只写一句口号。每条必须包含 atom 核心句 + 缩进展开，让 agent 知道具体怎么做。
18. **可执行脚本优先于数据文件**：判定 profile 时，如果项目同时有 `*.py` / `*.sh` / `Makefile` / `Snakefile` / `inference*` / `batch_*` / `run.sh` 等执行或 pipeline 文件，以及 `.sql` / `.parquet` / `.csv` 等数据文件，优先判为 `coding`，数据相关 atom 仅作辅助召回。
19. **扫描要高效**：项目检测阶段只用 `tree -L 2` 一次拿结构，再挑关键文件读前 30 行。不要逐个目录 `ls`，不要全文读取，不要用 shell 探索 skill 自身文件结构。
20. **规则 section 必须用脚本渲染**：选定 atom 后，调用 `tools/render-atoms.py` 生成 `Working Rules` / `Verification` / `Safety`，不手工拼接。
21. **禁止占位符代替脚本输出**：proposal 中 `Working Rules` / `Verification` / `Safety` 必须是脚本真实输出，不允许用 `[渲染内容]`、`<!-- 待渲染 -->`、省略号或任何简写占位。
