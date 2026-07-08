---
publish: true
---

# 仓库规范

本仓库是一个基于 Obsidian 的数字花园。笔记为带有 YAML frontmatter 的 Markdown，采用 Zettelkasten/PARA 方式组织。发布由 `publish: true` 标志控制，并通过 Python 脚本自动完成。

## 项目结构与模块组织
- 笔记：`🍀 花园导览/`、`📥 Inbox/`、`Atlas/`、`Cards/`、`Calendar/`、`Extras/`、`Sources/`、`Spaces/`。
- 脚本：仓库根目录下的 `publish_by_frontmatter.py`。
- 元数据：每篇笔记使用 YAML frontmatter；通过 `[[...]]` 建立反向链接；通过 `#标签` 添加标签。

## 构建、测试与开发命令
- 执行发布：`python publish_by_frontmatter.py` —— 选择带有 `publish: true` 的笔记，复制到发布仓库，并执行 Git 操作。
- 在脚本内配置：`VAULT_PATH`、`SHOWCASE_PATH`、`FORCE_INCLUDE_DIRS`。
- 链接检查：在 Obsidian 中，使用“检查失效链接”在发布前验证反向链接。

## 代码风格与命名约定
- Markdown：中文正文；技术术语使用英文。标题层级为 `#` → `####`。使用 `[[双链]]`、`#标签`、原子笔记和 MOC。允许使用表情前缀（例如 `🧰`、`📂`）。Frontmatter 字段包括 `publish`、`title`、`date created`、`date modified`、`tags`。
- Python：遵循 PEP 8，4 空格缩进，使用描述性名称。将配置常量集中管理，避免硬编码敏感信息。

## 测试规范
- 发布流程：(1) 确保设置 `publish: true`，(2) 运行脚本，(3) 确认敏感文件已被排除，(4) 验证 Git 操作成功，且发布仓库中仅出现预期文件。
- 链接：使用 Obsidian 的“检查失效链接”；抽查已编辑笔记中的外部 URL。

## 提交与合并请求规范
- 提交：使用祈使语气，范围聚焦。示例：`Cards: add MOC for AI notes`、`script: filter sensitive files`。
- PR：描述清晰，关联问题，针对 MOC/Canvas 提供修改前后的截图，并说明任何脚本或配置变更。

## 安全与配置提示
- 不要在笔记中存放个人数据和密钥；`.gitignore` 应排除敏感产物。
- 发布脚本会过滤敏感文件，但在推送前务必审查变更。
