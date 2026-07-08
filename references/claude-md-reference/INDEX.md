# CLAUDE.md 参考集

这个目录只放核心参考样本：真实项目里的 `CLAUDE.md` / `AGENTS.md`，并且内容是写给 agent 的长期上下文。

现在只收样本，不在这里抽取准则。后续抽取出来的内容应进入原子化准则库。

## 收录边界

保留：

- 真实项目的 `CLAUDE.md` / `AGENTS.md`。
- 能说明项目结构、工作流、验证方式、边界条件的 agent-facing 内容。
- 通用行为准则或高价值场景样本。

不保留：

- README、博客、awesome list、工具介绍、纯模板集合。
- 不是写给 agent 的项目说明。
- 低信号、重复、过度膨胀、不可直接参考的样本。

看过但不进核心的材料放在 `../reviewed-out/`。

## 样本概览

| 目录 | 数量 | 用途 |
| --- | ---: | --- |
| `universal/` | 5 | 通用 agent 行为、验证、简洁性、代码审查准则参考。 |
| `scenarios/coding/` | 12 | 代码项目的命令、测试、仓库结构、语言/框架约定。 |
| `scenarios/frontend-product/` | 2 | 前端产品 / SaaS 落地页模板，面向非技术用户的品牌化定制。 |
| `scenarios/product-design/` | 1 | 产品设计方法论、阶段门控、WHY-first 与 PRD 工作流。 |
| `scenarios/research/` | 2 | 学术研究生命周期、文献调研流程与写作辅助。 |
| `scenarios/data-analysis/` | 1 | 数据分析 agent 工作流、ticket 驱动开发与验证。 |
| `scenarios/creative-media/` | 1 | AI 原生视频制作工作流、模板、品牌与发布。 |
| `scenarios/agent-tooling/` | 3 | agent 工具、CLAUDE.md 生成器、多 runtime 项目上下文。 |
| `scenarios/context-engineering/` | 2 | context 生成、同步、token 分层、模板维护。 |
| `scenarios/docs-and-knowledge/` | 2 | 文档/知识库项目的组织和资料约束。 |
| `scenarios/memory/` | 2 | 自动记忆、反思学习、人工审核和记忆路由。 |
| `scenarios/security/` | 3 | 安全/链上项目的危险操作边界、完成 gate 与通用安全准则包。 |
| `scenarios/writing/` | 2 | 写作场景的事实约束、风格规则、反 AI 味与通用写作准则包。 |

## 样本清单

### 通用

- `universal/karpathy-inspired_CLAUDE.md`
- `universal/token-efficient_CLAUDE.md`
- `universal/agents_anbeeld_global.md`
- `universal/claude_sumit_gstack_starter.md`
- `universal/claude_leopiney_linus_torvalds.md`

### 代码项目

- `scenarios/coding/agents_jaredsburrows_android-gif-search.md`
- `scenarios/coding/agents_meltano_meltano.md`
- `scenarios/coding/agents_shane-kercheval_flex-evals.md`
- `scenarios/coding/agents_wbailey_command_line_reporter.md`
- `scenarios/coding/claude_antimetal_system-agent.md` — Go/Kubernetes 控制器，含性能采集、eBPF、Wiki 子代理约定
- `scenarios/coding/claude_browser-use_browser-use.md` — Python 异步 AI 浏览器库，含测试反 mock 哲学与 CDP 集成
- `scenarios/coding/claude_cssdao_batch-call-runner.md`
- `scenarios/coding/claude_openmf_mifos-mobile.md`
- `scenarios/coding/claude_trigger.md`
- `scenarios/coding/claude_workos-python.md`
- `scenarios/coding/agents_apache_superset.md` — 数据可视化平台，含前后端现代化迁移中的明确禁区
- `scenarios/coding/copilot_home-assistant_core.md` — 真实项目的 GitHub Copilot 指令文件（跨 agent 参考）

### 前端产品

- `scenarios/frontend-product/claude_tesseract-creator_nextjs-supabase-2025-starter.md` — Next.js 15 + Supabase 落地页/SaaS 启动模板
- `scenarios/frontend-product/claude_ship-studio_saas-template-1.md` — Ship Studio SaaS 落地页模板，面向非技术用户的品牌与文档维护

### 产品设计

- `scenarios/product-design/claude_ilandahan_aid.md` — AID 人工智能开发方法论，WHY-first、阶段门控与质量自检

### 学术研究

- `scenarios/research/claude_galaxy-dawn_claude-scholar.md` — 学术研究全生命周期配置（idea 到发表）
- `scenarios/research/claude_snl-ucsb_literature-survey-skill_SKILL.md` — 文献调研 Skill，Intent → Triage → Deepen → Synthesize

### 数据分析

- `scenarios/data-analysis/claude_jetbrains_databao-agent.md` — YouTrack 驱动的数据分析 agent 工作流

### 创意媒体

- `scenarios/creative-media/claude_digitalsamba_claude-code-video-toolkit.md` — AI 原生视频制作工具包（Remotion、语音、音乐、发布）

### Agent 工具

- `scenarios/agent-tooling/agents_greyhaven_autocontext.md`
- `scenarios/agent-tooling/claude_alirezarezvani_claudeforge.md`
- `scenarios/agent-tooling/claude_lukerenton_explore-claude-code.md`

### Context 工程

- `scenarios/context-engineering/claude_aspenkit_aspens.md`
- `scenarios/context-engineering/claude_solanabr_solana_ai_kit_meta.md`

### 文档和知识库

- `scenarios/docs-and-knowledge/claude_johnlindquist_mdflow.md`
- `scenarios/docs-and-knowledge/claude_oldwinter_knowledge-garden.md`

### 记忆

- `scenarios/memory/claude_bayramannakov_reflect.md`
- `scenarios/memory/claude_severity1_auto_memory.md`

### 安全

- `scenarios/security/claude_agamm_claude-code-owasp_SKILL.md` — OWASP 2025-2026 安全准则包（Skill 形式，高价值通用参考）
- `scenarios/security/claude_gadievron_raptor.md`
- `scenarios/security/claude_solanabr_solana_builder.md`

### 写作

- `scenarios/writing/claude_realrossmanngroup_no_ai_slop.md`
- `scenarios/writing/claude_yzhao062_agent-style_RULES.md` — 21 条写作风格准则包（agent-style，高价值通用参考）
