# RAPTOR - 自主攻防研究框架

安全操作（安装、扫描、读取、生成）：直接执行。
危险操作（应用补丁、删除、git push）：先询问。

---

## 会话开始

**第一条消息时：**
非常重要：按顺序执行以下步骤。
1. 使用 Read 工具读取 `.startup-output`，然后原样输出其内容作为围栏代码块（```，不带语言标签）。不要改写或重新排版。（SessionStart hook 会在你的第一条消息之前自动生成此文件。）
2. 在单行输出 "Quick commands:"，然后列出 /agentic、/scan、/fuzz、/web 命令（不要解释功能），并注明 /commands 可查看完整列表。
3. 如果 `sage_inception` 工具存在于你可用的 MCP 工具中，加载 `core/sage/CLAUDE.md`（持久化内存工作流）。如果不存在，SAGE 未安装 —— 静默跳过，不要提及。

---

## 执行规则

当技能、命令文件或用户消息指定字面命令（`Execute: foo`、作为操作的围栏 shell 代码块或 "run X"）时，原样执行。不要添加管道（`| tail`、`| head`、`| grep`）、重定向（`2>&1`、`>/dev/null`）、标志（`--verbose`、`-q`）、包装器（`timeout`、`nice`）或 `cd` 前缀。
RAPTOR 流水线会输出进度行、实时成本追踪以及 `OUTPUT_DIR=<path>` 哨兵，下游生命周期步骤依赖这些信息。截断或过滤该输出会破坏操作可见性和编排。

例外：当技能本身展示了修改方式（例如文档化的 `| tee logfile` 模式），按技能打印的内容执行。

---

## 斜杠命令分发

当 `/command` 触发时：

1. 读取 `.claude/commands/<name>.md` 的 frontmatter。
2. 如果 `dispatch: <command-line>`：替换占位符（操作员参数原样；`$OUTPUT_DIR` 来自运行生命周期；`$TARGET_PATH` 来自默认目标目录），然后运行替换后的命令。执行规则适用 —— 不添加管道/标志/包装器。
3. 如果 `dispatch: skill`：这是多步骤工作流。遵循 .md 正文；没有单一的 libexec 可执行文件。
4. 操作员参数**原样传递**。如果子命令不在 .md 文档化范围内，仍然执行它，让分发自己的错误浮出水面。不要静默改写为相似的子命令。
5. 永远不要从描述或训练记忆中推断分发方式。.md 是权威来源；CI（`.github/scripts/check_command_metadata.py`）强制要求每个命令都有可解析的 `dispatch:` 字段且目标存在于磁盘上。

---

## 命令

/project - 项目管理：create、list、status、coverage、findings、diff、merge、report、clean、export
/scan /fuzz /web /agentic /codeql /analyze - 安全测试
/exploit /patch - 生成 PoC 和修复（beta）
/validate - 可利用性验证流水线（见下文）
/understand - 代码理解：绘制攻击面、追踪数据流、搜寻变体（见下文）
/diagram - 从 /understand 或 /validate 输出生成 Mermaid 可视化图（见下文）
/annotate - 为单个函数附加散文式注释（手动或 LLM 自动生成）

**覆盖率：** 当询问覆盖率时，运行 `libexec/raptor-coverage-summary`（无参数 = 活跃项目）。使用 `--detailed` 查看逐文件表格，使用 `--gaps` 查看未评审函数。标记/取消标记及完整 API 见 `.claude/skills/coverage.md`。

**注意：** `/agentic` 执行 scan → dedup → prep → analysis（含验证方法论）。使用 `--sequential` 绕过并行编排。使用 `--understand` 在扫描前预映射代码库，使用 `--validate`  afterwards 对可利用发现运行完整验证流水线。两个标志均为可选。多模型：`--model` 可重复 —— 多个模型各自独立分析每个发现，然后关联结果；`--consensus`、`--judge` 和 `--aggregate` 添加可选的评审/综合模型。
/crash-analysis - 自主崩溃根因分析（见下文）
/oss-forensics - GitHub 取证调查（见下文）
/scorecard - 检查各模型在不同决策类别上的可靠性；用自然语言询问哪个模型擅长什么（见下文）
/create-skill - 保存方法（alpha）

---

## 项目

项目是可选的命名工作区，将分析运行集中到共享目录。使用 `--project <name>` 的命令或在 `/project use <name>` 之后运行的命令会写入项目目录。没有项目时，命令行为与之前相同（`out/` 下的时间戳目录）。

```
/project create myapp --target /path/to/code -d "Description"
/project use myapp
/scan                          # 输出进入项目目录
/project status                # 显示所有运行
/project findings              # 显示跨运行合并的发现
/project coverage              # 显示工具覆盖率摘要
/project report                # 跨所有运行的合并视图
/project correlate             # 跨运行发现关联
/project binary add <path>     # 持久化调试二进制文件，用于 binary-oracle 增强
/project binary list           # 列出活跃项目上持久化的二进制文件
/project binary remove <path>  # 移除一个
/project binary clear          # 清空所有
/project clean --keep 3        # 删除旧运行
/project none                  # 清除活跃项目
```

完整命令列表见 `/project help`。

---

## 默认目标目录

当 `/scan`、`/agentic`、`/validate`、`/codeql` 或 `/fuzz` 命令**没有路径参数**运行时，按以下顺序解析默认目标：

1. **活跃项目目标：** 运行生命周期脚本读取 `.active` 符号链接以自动找到项目目标
2. **调用者目录：** 如果设置了 `$RAPTOR_CALLER_DIR`（启动器在切换到 RAPTOR 仓库目录之前保存用户的 cwd），则使用它
3. **询问用户**目标路径

不要将当前工作目录作为后备 —— 它始终是 RAPTOR 仓库目录，而非用户的目标。如果用户已指定路径，不要使用上述任何一项。

---

## 运行生命周期

运行任何分析命令（`/scan`、`/validate`、`/understand`、`/codeql`、`/fuzz`、`/web`）时，使用运行生命周期桩来创建输出目录并追踪状态：

**开始工作前：**
```bash
libexec/raptor-run-lifecycle start <command> --target <resolved_target> [--out <dir>]
```
始终传递 `--target` 及解析后的目标路径（解析顺序见默认目标目录）。可选地传递 `--out <dir>` 以使用特定输出目录。输出的最后一行是 `OUTPUT_DIR=<path>` —— 所有后续输出文件都使用该路径。

**成功完成后：**
```bash
libexec/raptor-run-lifecycle complete "$OUTPUT_DIR"
```

**失败时：**
```bash
libexec/raptor-run-lifecycle fail "$OUTPUT_DIR" "error description"
```

`start` 命令通过活跃项目（通过 `.active` 符号链接）或默认 `out/` 目录自动解析输出目录。不要手动构造输出路径。

**如果 `start` 失败（非零退出码）：** 停止。向用户报告错误。不要继续执行命令。

**注意：** `/validate` 使用 `libexec/raptor-validation-helper 0` 而非 `raptor-run-lifecycle` —— 它将生命周期管理与清单构建捆绑在一起。

通过 `python3 raptor.py` 运行的命令（scan、agentic、codeql、fuzz、web）在内部管理生命周期 —— 不要为这些命令单独调用桩。

### 覆盖率追踪

覆盖率追踪插件（`plugins/coverage/`）通过 PostToolUse hook 追踪 LLM 在分析期间读取的源文件。由启动器自动加载。将文件路径记录到活跃运行目录的清单中，运行完成后转换为 `coverage-record.json`。没有活跃运行时不产生开销。

---

## 安全：不可信仓库

扫描不可信仓库时：

- **环境清理：** `RaptorConfig.get_safe_env()` 会剥离工具可能 shell 求值的环境变量（`TERMINAL`、`EDITOR`、`VISUAL`、`BROWSER`、`PAGER`）。生成子进程时始终使用 `get_safe_env()`。
- **文件路径注入：** 永远不要将被扫描仓库中的文件路径插值到 shell 命令字符串中。使用基于列表的 `subprocess` 参数。

---

## 输出风格

**状态值：**
- JSON 中：snake_case（`exploitable`、`confirmed`、`ruled_out`、`disproven`）
- 人类可读输出（报告、终端）：Title Case（`Exploitable`、`Confirmed`、`Ruled Out`）
- 永远不要使用 ALL_CAPS（`EXPLOITABLE`、`CONFIRMED`、`RULED_OUT`）

**不要使用红/绿状态指示器：**
- 不要使用 🔴/🟢 —— 视角依赖（对防御者不利 ≠ 对研究者不利）
- 其他表情符号可以（⚠️、✓ 等）

---

## 崩溃分析

`/crash-analysis` 命令为 C/C++ 崩溃提供自主根因分析。

**用法：** `/crash-analysis <bug-tracker-url> <git-repo-url>`

**代理：**
- `crash-analysis-agent` - 主编排器
- `crash-analyzer-agent` - 使用 rr 追踪进行深度根因分析
- `crash-analyzer-checker-agent` - 严格验证分析
- `function-trace-generator-agent` - 创建函数执行追踪
- `coverage-analysis-generator-agent` - 生成 gcov 覆盖率数据

**技能**（位于 `.claude/skills/crash-analysis/`）：
- `rr-debugger` - 确定性记录重放调试
- `function-tracing` - 使用 -finstrument-functions 进行函数插桩
- `gcov-coverage` - 代码覆盖率收集
- `line-execution-checker` - 快速行执行查询

**需求：** rr、gcc/clang（含 ASAN）、gdb、gcov

---

## OSS 取证

`/oss-forensics` 命令为公共 GitHub 仓库提供基于证据的取证调查。

**用法：** `/oss-forensics <prompt> [--max-followups 3] [--max-retries 3]`

**代理：**
- `oss-forensics-agent` - 主编排器
- `oss-investigator-gh-archive-agent` - 通过 BigQuery 查询 GH Archive
- `oss-investigator-github-agent` - 查询实时 GitHub API
- `oss-investigator-wayback-agent` - 恢复已删除内容（Wayback/commits）
- `oss-investigator-local-git-agent` - 分析克隆仓库中的悬空提交
- `oss-investigator-ioc-extractor-agent` - 从厂商报告中提取 IOC
- `oss-hypothesis-former-agent` - 形成基于证据的假设
- `oss-evidence-verifier-agent` - 通过 `store.verify_all()` 验证证据
- `oss-hypothesis-checker-agent` - 针对已验证证据验证主张
- `oss-report-generator-agent` - 生成最终取证报告

**技能**（位于 `.claude/skills/oss-forensics/`）：
- `github-archive` - GH Archive BigQuery 查询
- `github-evidence-kit` - 证据收集、存储、验证
- `github-commit-recovery` - 恢复已删除提交
- `github-wayback-recovery` - 从 Wayback Machine 恢复内容

**需求：** BigQuery 需要 `GOOGLE_APPLICATION_CREDENTIALS`

**输出：** `.out/oss-forensics-<timestamp>/forensic-report.md`

---

## 可利用性验证

`/validate` 命令验证漏洞发现是否真实、可达且可利用。

**用法：** `/validate <target_path> [--vuln-type <type>] [--findings <file>]`

**阶段：** 0 → A → B → C → D → E → F → 1（见 `.claude/skills/exploitability-validation/PIPELINE.md`）

**技能**（位于 `.claude/skills/exploitability-validation/`）：
- `PIPELINE.md` - 阶段命名约定（字母 = LLM，数字 = 机械）
- `SKILL.md` - 共享上下文、关卡、执行规则
- `stage-0-inventory.md` 至 `stage-1-outputs.md` - 阶段指令

**输出：** `out/exploitability-validation-<timestamp>/validation-report.md`

**流水线交接：** 对于 `/understand` → `/validate` 工作流，使用相同的 `--out` 目录，以便 `context-map.json`、`checklist.json` 和 `flow-trace-*.json` 自动共享。

---

## 代码理解

`/understand` 命令为安全研究提供深度对抗性代码理解。

**用法：** `/understand <target> [--map] [--trace <entry>] [--hunt <pattern>] [--teach <subject>] [--out <dir>]`

**模式：**
- `--map` —— 构建上下文：入口点、信任边界、sink → `context-map.json`
- `--trace <entry>` —— 追踪一条数据流 source → sink，含完整调用链 → `flow-trace-<id>.json`
- `--hunt <pattern>` —— 在代码库中查找某模式的所有变体 → `variants.json`
- `--teach <subject>` —— 深入解释框架、库或模式（内联）

**技能**（位于 `.claude/skills/code-understanding/`）：
- `SKILL.md` —— 关卡、配置、输出格式
- `map.md` —— 入口点枚举、信任边界映射、sink 目录
- `trace.md` —— 逐步数据流追踪，含分支覆盖
- `hunt.md` —— 结构性、语义性和根因变体分析
- `teach.md` —— 框架/模式解释，含安全结论

**输出：** 由 `libexec/raptor-run-lifecycle start understand` 解析（项目目录或 `out/understand_<timestamp>/`）

**流水线集成：** `/validate` 阶段 0 通过桥接（`core/orchestration/understand_bridge.py`）自动导入 `/understand` 输出。无需对齐 `--out` —— 桥接按以下顺序搜索：(1) 同目录文件，(2) 项目同级文件，(3) 全局 `out/` 中按目标路径 + SHA-256 新鲜度。找到后预填充 `attack-surface.json`、导入 flow trace 作为攻击路径，并将入口点/sink 标记为清单高优先级。

---

## 图表生成

`/diagram` 命令从 `/understand` 和 `/validate` 的 JSON 输出生成 Mermaid 可视化图，为研究者提供代码流、source、sink、信任边界、攻击树和攻击路径的可视化表示。请注意这仍是进行中的工作，但对于希望更好查看关系和流的用户可能有用。

**用法：** `/diagram <out-dir> [--target <name>] [--type context-map|flow-trace|attack-tree|attack-paths|all]`

**渲染内容：**
- `context-map.json` → flowchart LR：入口点 → 信任边界 → sink；未检查流用虚线边
- `attack-surface.json` → 相同布局（阶段 B 等效视图）
- `flow-trace-*.json` → 每个 trace 的 flowchart TD：调用链每一跳、污染变量、分支、攻击者控制摘要
- `attack-tree.json` → flowchart TD：按状态样式化的知识图谱节点（confirmed/disproven/exploring/unexplored）
- `attack-paths.json` → 每个 path 的 flowchart TD：步骤链，含接近度评分和阻塞注释

**输出：** `diagrams.md` 写入目标目录（或 `--stdout` 打印）

**实现：** `libexec/raptor-render-diagrams <out-dir> [--target <name>]`

**何时运行：** 图表在 `/validate` 和 `/understand --map`/`--trace` 结束时自动生成。对 JSON 输出手动编辑后，使用 `/diagram <dir>` 重新渲染。

---

## 注释

`/annotate` 命令将自由格式散文附加到单个函数，以镜像源码树的 markdown 形式存储。操作员编写手动评审注释；LLM 运行（`/agentic`、`/understand`）自动生成逐函数注释。

**存储：** `<base>/<source_path>.md` —— 每个源文件一个注释文件，含 `## function_name` 节、HTML 注释元数据行和自由格式正文。基础目录默认为活跃项目的 `<output_dir>/annotations`。

**状态枚举：** `clean`（已评审，无问题）/ `suspicious`（真实 bug，不可利用）/ `finding`（可利用）/ `entry_point` / `sink` / `trust_boundary` / `flow_step` / `unchecked_flow` / `error`。

**来源归属：** 每条注释携带 `metadata.source=human` 或 `metadata.source=llm`。LLM 写入时传递 `overwrite=respect-manual`，因此手动操作员注释永远不会被静默覆盖。操作员使用 `/annotate add` 时默认设置 `source=human`。

**时效性：** 带 `--lines N-M` 的注释携带函数源代码的 `metadata.hash` 短前缀。`/annotate stale` 重新计算并列出源代码已漂移的注释。

**注释来源：**
- `/agentic` —— 为每个分析的发现生成一个注释，位于 `<run_output_dir>/annotations/`。状态由 LLM 的 `is_true_positive` × `is_exploitable` 映射。正文是 LLM 的 `reasoning`。
- `/understand --map` / `--trace` —— 后处理器为入口点、sink、信任边界、未检查流和逐步追踪记录合成注释。
- `/annotate add` —— 操作员驱动的手动输入。

**操作员工作流：**
```
/annotate add src/auth.py check_pw --status clean -m "Constant-time compare, no taint"
/annotate ls --status finding              # 活跃项目中的跨运行视图
/annotate show src/auth.py check_pw
/annotate edit src/auth.py check_pw        # 在 $EDITOR 中打开 .md
/annotate stale --target ~/repos/myproj    # 自注释写入以来源代码已漂移
```

**底层：** `core/annotations/` —— 通过临时文件 + rename 原子写入，防御路径遍历（拒绝 `..` 段和绝对路径），函数名和元数据值验证防止磁盘格式损坏。

---

## 渐进加载

**扫描完成时：** 加载 `tiers/analysis-guidance.md`（对抗性思维）
**验证可利用性时：** 加载 `.claude/skills/exploitability-validation/SKILL.md`（关卡、方法论）
**验证出错时：** 加载 `tiers/validation-recovery.md`（阶段特定恢复）
**开发 exploit 时：** 加载 `tiers/exploit-guidance.md`（约束、技术）
**发生错误时：** 加载 `tiers/recovery.md`（恢复协议）
**应请求时：** 加载 `tiers/personas/[name].md`（专家角色）
**运行 /understand 时：** 加载 `.claude/skills/code-understanding/SKILL.md`（关卡、配置）以及相应模式文件：`map.md`、`trace.md`、`hunt.md` 或 `teach.md`

---

## 二进制分析

**流程：先找漏洞，再检查可利用性。**

1. **分析二进制文件** - 查找漏洞（缓冲区溢出、格式化字符串等）
2. **如果发现漏洞** - 运行利用可行性分析（强制）

```python
from packages.exploit_feasibility.api import analyze_binary, format_analysis_summary

# 强制：发现漏洞后运行此函数
result = analyze_binary('/path/to/binary')
print(format_analysis_summary(result, verbose=True))
```

**不要改用 checksec 或 readelf** —— 它们会遗漏关键约束，例如：
- 经验性 %n 验证（glibc 可能阻止）
- strcpy 的空字节约束（无法写入 64 位地址）
- ROP gadget 质量（0 个可用 gadget = 无 ROP 链）
- 输入处理器的坏字节
- Full RELRO 也会阻止 .fini_array（不仅是 GOT）

**`exploitation_paths` 段会告诉你，在给定系统缓解措施（glibc 版本、RELRO 等）下代码执行是否实际可行。**

**SMT 集成（可选，需要 `pip install z3-solver`）：**

Z3 在两处使用 —— 缺少时都会优雅降级：

1. **二进制 / one-gadget**（`packages/exploit_feasibility/smt_onegadget.py`）：检查给定崩溃状态下 one-gadget 的寄存器/内存约束是否可满足。结果位于 `exploitation_paths[vuln].one_gadget_info.smt_feasibility`。

2. **CodeQL 数据流**（`packages/codeql/smt_path_validator.py`）：检查数据流路径上的分支条件是否联合可满足。`unsat` → 误报，跳过 LLM。`sat` → 具体输入值填入 LLM 提示和 `DataflowValidation.prerequisites`。最佳覆盖：CWE-190、CWE-120/122、CWE-193、CWE-476。

---

## 二进制 Oracle 可达性

默认行为（无标志）：/agentic 和 /codeql 自动检测常见构建目录下的调试二进制文件，过滤为**仅本地构建**（git 未跟踪 —— 已提交二进制文件因来源未验证而被丢弃），并用它们抑制死代码发现。传递 `--no-binary-oracle` 退出。显式传递 `--binary <path>` 时，RAPTOR 通过 DWARF + nm 将源清单与调试二进制文件连接，并为每个原生（C/C++/Rust/Go）函数添加每二进制裁定：

- `symbol_present` / `inlined` / `folded` —— 函数以某种形式保留在编译产物中
- `absent` —— 编译器/链接器将其从分析的二进制文件中移除

`absent` 作为抑制依据的可靠性来自语料积累：**在 6 个迭代调优语料库上 1952/1952 裁定正确（一致性）+ 在保留的 zstd v1.5.6 语料库上未调优分类器即达 187/187 正确（泛化）** —— rule-of-three 95% 上限，首次接触未见数据时漏检率 ≤1.6%。保留集非平凡：工作负载覆盖了 473/1431 个函数，真实活跃函数上零 `absent` 裁定。条件为完整 DWARF 证据 —— 分析集中被 strip 的二进制文件会降级为 `tier="symbol_only"，chokepoint 拒绝抑制。

裁定通过现有可达性 chokepoint 流动：/codeql + /agentic 对 absent-function 发现跳过 LLM 分析（LLM 前硬抑制）；/validate 的降级器钳制攻击路径接近度；/understand --map 用每二进制裁定 + tier 注释入口点和 sink。

**操作员用法**：
- （默认，无标志）—— 自动检测运行，仅过滤本地构建的二进制文件（git 未跟踪），未找到时给出软提示。
- `--binary <path>` —— 传递显式调试二进制文件。对混合目标可重复。路径在解析时验证。绕过 git 跟踪过滤（操作员声明信任）。抑制默认自动检测。
- `--binary-auto` —— 与默认开启路径相同的自动检测 + git 过滤逻辑，但 "未找到" 消息更明显。尊重 `--target-kind`。达到结果上限（8）时警告。自动检测目录：`build/`、`target/release/`、`cmake-build-*/`、`bazel-bin/`、`builddir/`、`Debug/`、`Release/`、`out/`、`dist/`、`bin/`、Rust `target/<triple>/release` 跨目标通配，以及源码根目录。
- `--no-binary-oracle` —— 完全禁用此运行的 binary-oracle 过滤。用于无主二进制文件的纯库目标、希望所有发现都不被过滤以供评审的运行，或构建不匹配导致过度抑制时。若与 `--binary` / `--binary-auto` 同时指定，将覆盖它们并向 stderr 发出警告。
- `--binary-edges` —— Inc 2b Tier 1/2：通过 r2 提取直接调用边 + vtable 解析（单次调用脚本文件模式；按 build-id 缓存并做跨目标碰撞检查）。较慢（每二进制约 10-30 秒，之后缓存）。`binary_call_edge` REACHABLE 提升证据需要此项（挽救源图认为已死的函数）。
- 对于 `--target-kind=hybrid` 部署（同时交付库 + 应用），声明 MULTIPLE 二进制文件 —— 仅当 EVERY 声明二进制文件都缺少某函数时，该函数才为 `absent`。Tier 加权合并：当 full-DWARF 与 symbol-only 不一致时，full-DWARF 胜出（`alive-in-any` 规则仅适用于相同 tier）。

**每项目持久化配置**：
- `/project binary add <path>` —— 在活跃项目上持久化二进制文件路径。后续每次 /agentic / /codeql / /validate 运行自动加载。添加时通过 `is_file()` 验证。
- `/project binary list` / `remove` / `clear` —— 管理持久化列表。

**审计轨迹**：
- 当 chokepoint 硬抑制发现时，会在运行输出目录写入 `suppressions.jsonl`。每条 JSON 记录含 `finding_id`、`rule_id`、`file_path`、`line`、`function`、`verdict`、`reason`。使用 `jq -c . suppressions.jsonl` 查询。/agentic 和 /codeql 写入相同文件格式。
- 分类器的每发现分析记录也携带 `analysis.reachability_suppression: true` + `analysis.reachability_verdict: <verdict>`，便于逐发现检查。

**对抗恶意/错误二进制文件的防护**：
- 自动检测的来源门控：git 跟踪的二进制文件（已提交到源码树）被丢弃 —— 只有本地构建产物（build/、target/release/ 等下的未跟踪文件）进入 oracle。防御攻击者植入的二进制文件和陈旧的已提交预构建产物，后者会悄悄将 `absent` 裁定导向抑制真实发现。操作员知道已跟踪二进制文件可信时可通过显式 `--binary <path>` 绕过。
- 源覆盖率下限（≥5% 的项目源名称匹配，最少匹配 3 个，在项目名称 ≥8 时生效）—— 一个与源码无关的植入 ELF 会被大声警告丢弃，而不是让每个源函数都变成 `absent`。
- 沙箱隔离：r2 在 `core.sandbox.run` 下运行（命名空间 + Landlock + 网络拒绝）；binutils 工具（readelf、nm、objdump、c++filt）在 `core.sandbox.run_trusted` 下运行。

**E2E + 精度验证**：
- `libexec/raptor-binary-oracle-e2e` —— 单次调用审计，构建真实 C 目标并遍历 15 个消费面（54 个断言）。无 LLM 调用。通过 `bin/raptor` 或 `CLAUDECODE=1 libexec/...` 运行。
- `libexec/raptor-binary-oracle-precision --corpus <name>` —— 在任何语料驱动（synthetic/zlib/libsodium/snappy/leveldb/regex-rust/zstd_holdout）上重新测量 absent 精度。报告包含每语料交叉表（分类器 × gcov live/dead）、带 rule-of-three 上限的汇总、n-浓度支配检测，以及工具链块（cc/gcov/llvm-cov 版本），确保精度数字可复现。

**技能位置**：`core/inventory/binary_oracle.py`（分类器）、`core/inventory/binary_oracle_autodetect.py`（自动检测）、`core/inventory/binary_oracle_precision.py`（测量 harness —— `libexec/raptor-binary-oracle-precision` CLI shim 运行它）。设计 + 验证文档：`~/design/binary-oracle-reachability.md` §9-11。

---

## 漏洞利用开发

**在尝试任何技术之前先验证约束。** 许多时间浪费在架构上不可行的方法上。

**强制：先检查 `exploitation_paths` 裁定：**
- Unlikely = 无已知路径，建议环境变更
- Difficult = 原语存在但难以链接，如实说明挑战
- Likely exploitable = 机会较大，按建议技术继续

**遵循 chain_breaks** —— 它们准确告诉你什么行不通。
**遵循 what_would_help** —— 它们告诉你什么可能行得通。

**即使对 Difficult/Unlikely 裁定也要 ALWAYS 提供下一步：**
- 尝试替代目标（如有）
- 仅关注信息泄露
- 在更旧环境中运行（Docker）
- 转向其他目标

**不要直接停下** —— 让用户决定如何继续。

详细约束表和技术替代方案见 `tiers/exploit-guidance.md`。

---

## 结构

Python 编排一切。Claude 简洁展示结果。
永远不要绕过 Python 执行流。
- 绝不在代码、注释、日志等中透露远程 OLLAMA 服务器位置
- **Python 路径安全：** 除 `os.environ["RAPTOR_DIR"]` 外，永远不要向 `sys.path` 添加任何内容。使用硬查找（未设置则 KeyError）—— 无后备、无 `'.'`、无 `os.getcwd()`、无硬编码路径。`libexec/` 脚本通过 `Path(__file__).resolve().parents[1]` 自行处理路径设置，不需要 `RAPTOR_DIR`。
