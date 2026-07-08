# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在处理本仓库代码时提供指引。

## 这是什么

一个交互式教育网站，通过模拟一个可探索的项目来教授 Claude Code 的功能。纯静态 HTML/CSS/JS —— 零构建步骤，无框架，无打包工具。

## 本地运行

```bash
# 任意静态服务器，指向 site/ 目录
npx serve site
python -m http.server -d site 8080
```

直接打开 `site/index.html` 也可以（通过相对路径获取 manifest）。

## 架构

所有教学内容都以 JSON 字符串形式存储在 `site/data/manifest.json` 中。这个单一文件驱动整个 UI —— 树形结构、文件内容、标签、徽章和功能分组。要添加或修改内容，请编辑 manifest。

**组件类（均为原生 JS，无模块，通过 `<script>` 标签加载）：**

- `App`（app.js）—— 控制器。加载 manifest，连接组件，处理键盘导航（方向键）、哈希路由、交通灯按钮以及虚空彩蛋（最小化按钮 → canvas 粒子动画）。
- `FileExplorer`（file-explorer.js）—— 侧边栏树。在 `.tree-children-guided` 容器内的 `<canvas>` 元素上绘制连接线（├── └──）。`.claude` 目录在加载时自动展开。
- `ContentLoader`（content-loader.js）—— 渲染文件内容。内置手写 markdown 解析器，支持：YAML frontmatter（渲染为表格）、围栏代码块、表格、列表、内联格式和链接。Markdown 文件带有“已渲染/原始”切换。通过 Prism.js 实现语法高亮。
- `Terminal`（terminal.js）—— 右侧面板。交互式斜杠命令模拟器（`/help`、`/init`、`/doctor`、`/diff`、`/compact`、`/model`、`/cost`、`/status`、`/config`、`/memory`）。带动画的输出序列。
- `ProgressTracker`（progress.js）—— 使用键 `tcc-progress` 在 localStorage 中追踪已访问的功能。

**CSS 按关注点拆分：** `variables.css`（设计令牌）、`layout.css`（外壳/侧边栏/内容网格）、`components.css`（树项、徽章、内容面板、frontmatter）、`syntax.css`（Prism 覆盖）、`terminal.css`、`void.css`（彩蛋）。

## 关键不变量

**Canvas DPI 缩放：** `file-explorer.js` 中的 `_createCanvas()` 已经调用 `ctx.scale(dpr, dpr)`。调用方禁止再次缩放上下文，否则树形连接线在高 DPI 显示器上会出现错位（坐标会被乘以 dpr²）。

**静态树线绘制时机：** `.claude` 目录在加载时自动展开。`_drawStaticLines` 使用双 `requestAnimationFrame`，确保浏览器完成布局后再测量 `offsetTop`/`getBoundingClientRect`。如果触发零尺寸保护，则在下一帧重试。

**Frontmatter 处理：** Markdown 渲染器检测内容开头的 `---` 围栏块，并将其渲染为样式化的表格。没有此处理，`---` 会变成 `<hr>`，YAML 的 `#` 注释会被渲染为标题。

**Manifest 节点模式：** 每个树节点包含 `name`、`path`、`type`（"file"|"directory"|"separator"）。文件可拥有：`content`（markdown/代码字符串）、`feature`（对相关文件分组）、`badge`、`label`、`description`、`command`。目录有 `children` 数组。分隔符节点仅有 `type: "separator"`，渲染为虚线分隔线。

**内容标题优先级：** 内容加载器优先显示 `node.label`，其次回退到功能标题，最后是文件名。这对于内置部分很重要，因为多个文件共享一个功能但需要不同的标题（例如，每个捆绑 skill 显示其 `/command` 名称，而不是 "Bundled Skills"）。

**内置部分的相关文件：** `built-in/` 下的文件只链接回概览文件（例如 `BUNDLED-SKILLS.md`），而不是链接到每个共享同一功能的兄弟文件。该过滤逻辑在 `content-loader.js` 中实现。

**代码块首行缩进问题：** 全局 `code` 样式（padding、background、border）被 `.md-code-block` 内的 `<code>` 继承，导致渲染后的代码块第一行出现可见缩进。通过将 `.md-code-block` 内的 `<code>` 重置为 `padding: 0; background: none; border: none` 已修复。

**内容文件行尾：** `site/content/` 中的内容文件始终使用 Unix（LF）行尾。Windows CRLF 可能导致代码块渲染问题，即使 markdown 渲染器会规范化行尾。

## 内容设计原则

- 内容应让人感觉像在探索真实的仓库 —— 自描述样板，能自我说明
- 提供简洁概览便于扫读，需要深入时可展开细节
- 每个 `.claude/` 子文件夹在脚手架之外都有一个基础入口文件（例如 `SKILLS.md`），然后脚手架展示实际结构
- `built-in/` 部分涵盖 Claude Code 内置且无需设置的功能。一条视觉分隔线（虚线）将其与上方的 `.claude/` 项目配置分开。每个内置类别都有一个概览文件和子目录中的独立条目
- 内容中避免使用 em-dash（长破折号）。改用逗号、句号或冒号
