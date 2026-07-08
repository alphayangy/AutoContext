# claude-obsidian — Claude + Obsidian Wiki Vault

本文件夹同时是一个 Claude Code 插件和一个 Obsidian vault。

**插件名称：** `claude-obsidian`（v1.7+ "Compound Vault" — 参见 [docs/compound-vault-guide.md](docs/compound-vault-guide.md)；v1.8+ 新增 methodology modes — 参见 [docs/methodology-modes-guide.md](docs/methodology-modes-guide.md)）
**Skills：** `/wiki`、`/wiki-ingest`、`/wiki-query`、`/wiki-lint`、`/wiki-cli`（v1.7）、`/wiki-retrieve`（v1.7，可选）、`/wiki-mode`（v1.8）
**Vault 路径：** 本目录（直接用 Obsidian 打开）

## 这个 Vault 的用途

这个 vault 演示了 LLM Wiki 模式 —— 一个为 Claude + Obsidian 打造的持久化、可复合增长的知识库。放入任意来源，提出任意问题，wiki 会在每次会话中变得越来越丰富。

## Vault 结构

```
.raw/           源文档 —— 不可变，Claude 读取但永不修改
wiki/           Claude 生成的知识库
_templates/     Obsidian Templater 模板
_attachments/   wiki 页面引用的图片和 PDF
```

## 使用方法

将源文件放入 `.raw/`，然后告诉 Claude："ingest [filename]"。

提出任何问题。Claude 会先读取索引，再深入相关页面。

运行 `/wiki` 来搭建新 vault 或检查设置状态。

每进行 10-15 次 ingest 后运行 "lint the wiki"，以发现孤立页面和缺失内容。

## 跨项目访问

要从另一个 Claude Code 项目引用本 wiki，请在该项目的 CLAUDE.md 中添加：

```markdown
## Wiki Knowledge Base
Path: /path/to/this/vault

When you need context not already in this project:
1. Read wiki/hot.md first (recent context, ~500 words)
2. If not enough, read wiki/index.md
3. If you need domain specifics, read wiki/<domain>/_index.md
4. Only then read individual wiki pages

Do NOT read the wiki for general coding questions or things already in this project.
```

## 插件 Skills

| Skill | Trigger |
|-------|---------|
| `/wiki` | 设置、搭建、路由到子 skills |
| `ingest [source]` | 单个或批量源文档 ingestion |
| `query: [question]` | 基于 wiki 内容回答问题 |
| `lint the wiki` | 健康检查 |
| `/save` | 将当前对话归档为结构化 wiki 笔记 |
| `/autoresearch [topic]` | 自主研究循环：搜索、获取、综合、归档 |
| `/canvas` | 可视化层：将图片、PDF、笔记添加到 Obsidian canvas |
| `/wiki-cli`（v1.7） | Obsidian CLI transport 包装器；桌面端默认 mutation 路径 |
| `/wiki-retrieve`（v1.7） | 混合上下文 + BM25 + cosine-rerank 检索（通过 `bash bin/setup-retrieve.sh` 可选启用） |
| `/wiki-mode`（v1.8） | Methodology modes（LYT / PARA / Zettelkasten / Generic）。通过 `bash bin/setup-mode.sh` 设置；由 wiki-ingest / save / autoresearch 用于路由新页面 |
| `/think`（v1.9） | 可调用工作流的 10 原则思考循环（OBSERVE-OBSERVE-LISTEN-THINK-CONNECT-CONNECT-FEEL-ACCEPT-CREATE-GROW）。应用于架构决策、审计、事后复盘、模糊的用户请求。每个其他 skill 都附有 "How to think" 附录，将此框架映射到其具体工作 |

## Transport（v1.7+）

`scripts/detect-transport.sh` 在首次运行时写入 `.vault-meta/transport.json`，并每周刷新一次。Skills 在修改 vault 前会查询该文件。回退链：Obsidian CLI → mcp-obsidian → mcpvault → filesystem（始终可用的兜底方案）。决策树见 [wiki/references/transport-fallback.md](wiki/references/transport-fallback.md)。

## 并发控制（v1.7+）

`scripts/wiki-lock.sh` 提供 per-file advisory locks，确保多写入方 ingest 安全。每次 wiki 页面写入都应由 `wiki-lock acquire`/`release` 保护。默认 stale-after 为 60 秒；跨进程 release 是设计允许的。PostToolUse hook 在持有锁期间会推迟 `git add`。修复了 v1.6 中潜在的多写入方损坏问题。

## Methodology Modes（v1.8+）

通过 `bash bin/setup-mode.sh` 为 vault 选择组织风格。提供四种模式：**generic**（v1.7 默认 —— 无特定主张）、**LYT**（Linking Your Thinking —— MOC + 原子笔记）、**PARA**（Projects/Areas/Resources/Archives）、**Zettelkasten**（时间戳 ID、扁平、密集链接）。模式写入 `.vault-meta/mode.json`（默认被 gitignore；需要提交时请用 `git add -f`）。`wiki-ingest`、`save` 和 `autoresearch` 在归档新页面之前会咨询 `python3 scripts/wiki-mode.py route <type> "<name>"` —— 消费端 skills 无需特殊处理。完整指南见 [docs/methodology-modes-guide.md](docs/methodology-modes-guide.md)。解决了 2026 年 5 月 compass artifact 中优先级缺口 5 的问题。

## Pre-commit verifier（v1.7.1+）

在为非平凡的 workstream 暂存更改之后、但在运行 `git commit` 之前，派遣 `verifier` agent（`agents/verifier.md`）。它会读取 `git diff --cached`，应用 /best-practices 六切分 + agent kernel，并按四个等级返回发现（BLOCKER / HIGH / MEDIUM / LOW），附带 file:line 引用。该 agent 仅拥有只读工具（Read、Grep、Glob、Bash）—— 只能检查而不能修改，因此其输出纯粹是建议性的。这闭环了 v1.7 审计发现的问题：代码从 worker 直接到 commit，缺少独立的 verifier 环节，导致 BLOCKER B1（数据外泄同意缺口）被遗漏。回顾见 `docs/audits/v1.7.0-audit-2026-05-17.md` §10。

## MCP（可选）

如果你配置了 MCP server，Claude 可以直接读写 vault 笔记。

设置说明见 `skills/wiki/references/mcp-setup.md`。

## Release Blog Post

在发布新版本（git tag + `gh release create`）后，运行：

```
/release-blog
```

这会在 https://agricidaniel.com/blog/ 生成博客文章，处理封面图生成、SEO 元数据、FAQ schema、内链、sitemap/llms.txt 更新、Vercel 部署以及 Google 索引。
