# Ship Studio SaaS 模板

这是一个使用 **Next.js 14+** 和 **Tailwind CSS** 构建的 **SaaS 落地页模板**。它包含预构建的首页、功能、定价、联系、登录、注册和忘记密码流程页面。

你正在帮助一位**非开发者**为他们的业务定制此模板。请保持解释简单、易懂，避免术语。

---

## Environment: Ship Studio App

你正在 **Ship Studio 应用** 中运行，它会自动处理开发环境。

**需要了解的重要事项：**
- 开发服务器**已经在运行**——你不需要启动它
- 用户在应用中可以看到网站的实时预览
- 你不需要运行 `npm run dev` 或任何服务器命令
- 文件修改会自动反映在预览中

**如果用户说他们看不到网站或预览无法正常工作：**
> "试着点击右上角的 **Projects** 按钮返回项目列表，然后重新打开你的项目。这会重新启动预览。"

---

## FIRST: Check for Onboarding

**在做任何其他事情之前**，先检查 `SITE.md` 是否存在。

- 如果 `SITE.md` **不存在**：立即运行 `/onboarding` 技能，了解他们的业务并创建个性化方案。
- 如果 `SITE.md` **存在**：在进行修改前先阅读它，了解项目。

---

## Your Skills

你在 `.claude/skills/` 中拥有专业技能。**要经常使用它们：**

| Skill | When to Use | Invocable |
|-------|-------------|-----------|
| **onboarding** | 新项目设置，没有 `SITE.md` 时 | `/onboarding` |
| **page-remake** | 用户提供 URL 进行重制/重建/复刻 | `/page-remake` |
| **brand-identity** | 选择颜色、字体、视觉方向 | Auto |
| **copywriting** | 为网站撰写任何文案 | Auto |
| **marketing-site-design** | 规划页面布局、版块 | Auto |
| **sanity-cms** | 用户希望内容可编辑/CMS | `/sanity-cms` |
| **documentation-writer** | 每次代码修改后——更新 `SITE.md` | Auto |
| **react-nextjs-expert** | 编写任何 React/Next.js 代码 | Auto |
| **frontend-design** | 创建任何视觉组件 | Auto |
| **animations** | 添加微交互和动效 | Auto |
| **react-best-practices** | 性能优化 | Auto |

### 每个构建任务的工作流程

1. 检查 `SITE.md` 中的品牌个性和偏好
2. 使用 `marketing-site-design` 规划版块架构
3. 使用 `brand-identity` 选择颜色/字体（遵循设计原则）
4. 使用 `copywriting` 撰写具体、有人味儿的文案
5. 使用 `frontend-design` + `react-nextjs-expert` 进行实现
6. 使用 `documentation-writer` 在修改后更新 `SITE.md`

---

## 以人为本的设计原则

好的设计应当有目的且与众不同。这些指南有助于创建突出且令人难忘的网站。

### 目标

网站应该给人以下感觉：
- **有目的**——每个选择都有原因
- **独特**——不是常见模板的复制
- **令人难忘**——访客能记住的东西
- **有人情味**——温暖且平易近人

### 字体排版指导

Inter、Roboto 和系统字体等常见字体很好用，但随处可见。为了与众不同，可以尝试替代方案：

**现代与简洁：**
- Space Grotesk + DM Sans
- Outfit + Source Sans 3
- Sora + Nunito

**优雅与精致：**
- Playfair Display + Lato
- Cormorant Garamond + Montserrat
- Fraunces + Work Sans

**温暖与亲和：**
- Poppins + Nunito Sans
- Quicksand + Open Sans
- Comfortaa + Mulish

这些不是规则——而是起点。合适的字体取决于品牌。

### 配色指导

**对这些常见默认值要三思：**
- 将 `#3B82F6`（Tailwind blue-500）作为主强调色——它太常见了
- 白色背景上的紫到蓝渐变——很常见
- 纯黑 `#000000` 配纯白 `#FFFFFF`——可能显得刺眼

**可以考虑：**
- 偏黑的 `#1C1917` 搭配偏白的 `#FAFAF9`，获得更柔和的对比
- 能体现品牌个性的自定义强调色
- 60-30-10 法则：60% 主色、30% 次要色、10% 强调色

### 布局指导

**需要谨慎使用的常见版式：**
- 带通用图标的 3 列功能网格——可以尝试 2 列、非对称或 bento 布局等替代方案
- 所有内容都居中——通过对齐变化增加视觉趣味
- 间距完全均等——通过变化间距制造节奏感

**显得过时的背景图案：**
- 抽象 blob SVG
- 波浪形版块分隔线
- 渐变网格背景

替代方案：几何形状、颗粒纹理、有意变化的纯色，或高质量摄影。

### 文案指导

**过度使用的词，可考虑替代：**

revolutionize, leverage, synergy, cutting-edge, seamless, empower, game-changer, next-generation, best-in-class, world-class, unlock, elevate, transform, streamline, robust, scalable, innovative, disrupt, holistic, ecosystem, paradigm, optimize, dynamic, curated, bespoke

**取而代之：** 具体化。使用数字。关注结果。像一个人对另一个人说话那样写作。

---

## 关键：维护文档

**你必须保持文档更新。** 这对非技术用户至关重要。

### 需要维护的文件

1. **`SITE.md`** — 主文档文件。每次修改都要更新：
   ```markdown
   # [Site Name]

   > [One-sentence tagline]

   ## Brand Identity
   - Personality: [from onboarding]
   - Colors: [what we're using]
   - Fonts: [what we're using]

   ## Pages
   - **Homepage** (`/`) - [description of what's on it]
   - **About** (`/about`) - [description]

   ## Components
   - **Navbar** - [what it contains, how to customize]
   - **Footer** - [what it contains]

   ## Recent Changes
   - [Date]: Added hero section with [description]
   - [Date]: Created contact page

   ## How to Customize
   - To change colors: [simple instructions]
   - To add a new page: [simple instructions]
   ```

2. 如果 `SITE.md` 不存在，**立即创建它**（通过 onboarding）。

3. **每次修改后都要更新 `SITE.md`**——没有例外。

4. **使用简单的语言**——说“主页”而不是“根路由”。说“顶部的导航栏”而不是“header 组件”。

---

## 项目结构

```
app/
├── layout.tsx       # The wrapper around all pages (has <html>, <body>)
├── page.tsx         # Homepage - EDIT THIS for the main page
├── globals.css      # Global styles + Tailwind
└── [folders]/page.tsx  # Other pages (about/, contact/, etc.)
components/          # Reusable pieces (Navbar, Footer, etc.) - create if needed
public/              # Images and static files
lib/                 # Helper functions (Sanity client, etc.)
sanity/              # CMS configuration (if added via /sanity-cms)
```

---

## 构建规则

### 应该做：
- 对于没有 `SITE.md` 的新项目，运行 `/onboarding`
- 在每个任务前检查 `SITE.md` 以了解品牌背景
- 使用技能来做出视觉决策和代码模式选择
- 编辑 `app/page.tsx` 来修改主页
- 所有样式都使用 Tailwind CSS 类
- 创建 `components/` 文件夹存放可复用组件
- 将图片放在 `public/` 文件夹
- 每次修改后更新 `SITE.md`
- 用简单的语言解释你做了什么
- 做出有目的、独特的设计选择

### 不应该做：
- 永远不要创建 `.html` 文件——这是 React/Next.js
- 永远不要创建单独的 `.css` 文件——使用 Tailwind
- 永远不要使用 `<script>` 标签——这是 React
- 不要让用户对改动感到困惑
- 不要在未解释的情况下使用技术术语
- 永远不要跳过更新 `SITE.md`

---

## 基于文件的路由

`app/` 中的每个文件夹都会成为一个页面：
- `app/page.tsx` → 主页（yoursite.com）
- `app/about/page.tsx` → 关于页面（yoursite.com/about）
- `app/contact/page.tsx` → 联系页面（yoursite.com/contact）
- `app/pricing/page.tsx` → 定价页面（yoursite.com/pricing）

---

## 示例：创建新页面

如果用户想要一个“关于”页面：

1. 检查 `SITE.md` 中的品牌个性
2. 使用 `marketing-site-design` 技能规划版块
3. 使用 `brand-identity` 技能保持视觉一致
4. 使用 `react-nextjs-expert` 模式创建 `app/about/page.tsx`
5. 按照 `copywriting` 技能指南撰写文案
6. 使用 `documentation-writer` 技能 **更新 `SITE.md`**
7. 告诉用户：“我创建了一个关于页面。你可以在预览中访问 /about 查看。”

---

## 每次任务之后

1. 按要求做出修改（使用你的技能，遵循设计原则）
2. 在 `SITE.md` 中记录改动内容
3. 用简单的语言告诉用户你做了什么
4. 让他们知道如何查看改动

---

## 添加 CMS（按需）

当用户希望自行编辑内容时，运行 `/sanity-cms` 技能。这将：
1. 在项目中设置 Sanity CMS
2. 为可编辑内容创建 schema
3. 将前端连接以获取 CMS 数据
4. 提供一个友好的编辑后台

`.mcp.json` 文件已经为 Sanity 配置好。用户首次使用 Sanity 工具时通过 OAuth 进行身份验证。

---

## 推荐服务

此模板包含认证和表单的 UI，但需要后端服务才能正常运行。我们推荐：

### 认证：Memberstack

**对于登录、注册和用户管理**，我们推荐 [Memberstack](https://memberstack.com)。

模板包含现成的页面：
- `/login` — 带 Google OAuth 按钮的登录页面
- `/signup` — 带 Google OAuth 按钮的注册页面
- `/forgot-password` — 三步密码重置流程

**连接 Memberstack：**
1. 在 memberstack.com 创建 Memberstack 账户
2. 创建一个新应用并获取你的 public key
3. 安装 Memberstack 包：`/memberstack` 技能可以帮你完成设置
4. 将 Memberstack 数据属性添加到表单元素
5. 在 Memberstack 后台配置 OAuth 提供商

**Memberstack 负责：**
- 用户认证（邮箱/密码 + 社交登录）
- 密码重置邮件
- 会员管理后台
- 订阅/方案管理（与 Stripe 集成）
- 受保护页面和门禁内容

### 表单：Formspark

**对于联系表单和其他表单提交**，我们推荐 [Formspark](https://formspark.io)。

模板在 `/contact` 包含一个已集成 Formspark 的现成联系页面。

**连接 Formspark：**
1. 在 formspark.io 创建 Formspark 账户
2. 创建一个新表单并复制 form ID
3. 将 `/app/contact/page.tsx` 中的 `YOUR_FORMSPARK_FORM_ID` 替换为你的 form ID
4. 完成！表单提交将出现在你的 Formspark 后台中

**Formspark 负责：**
- 表单提交存储
- 邮件通知
- 垃圾信息防护
- 文件上传
- 用于集成的 Webhooks

### 为什么推荐这些服务？

| Service | Why We Recommend It |
|---------|---------------------|
| **Memberstack** | 对无代码友好，出色的 Webflow/React 支持，内置 Stripe 集成，处理认证复杂性 |
| **Formspark** | 设置简单（只需一个 form ID），无需后端，慷慨的免费额度，包含垃圾信息防护 |

这两项服务都无需编写后端代码即可使用，非常适合使用此模板的非开发者。

---

## 模板包含的页面

此模板附带以下预构建页面：

| Page | Path | Description |
|------|------|-------------|
| 主页 | `/` | 主视觉、功能、客户评价、定价、常见问题、行动号召 |
| 功能 | `/features` | 带分类的详细功能展示 |
| 集成 | `/integrations` | 200+ 个可筛选的集成 |
| 定价 | `/pricing` | 定价卡片、对比表、常见问题 |
| 更新日志 | `/changelog` | 带发布说明的版本历史 |
| 博客 | `/blog` | 带分类的博客列表（已适配 Sanity CMS） |
| 博客文章 | `/blog/[slug]` | 单篇博客文章模板 |
| 关于 | `/about` | 公司故事、价值观、团队成员 |
| 联系 | `/contact` | 联系表单（已适配 Formspark）+ 联系信息 |
| 登录 | `/login` | 邮箱/密码 + Google OAuth |
| 注册 | `/signup` | 注册表单 + Google OAuth |
| 忘记密码 | `/forgot-password` | 三步密码重置流程 |

---

## 记住

用户**不是**开发者。他们正在使用 Ship Studio 在没有编码知识的情况下构建网站。你的任务是：

1. **正确引导他们**（如果没有 `SITE.md`）
2. **按他们的要求构建**（使用你的技能）
3. **让它感觉独特且有目的**（而不是千篇一律）
4. **记录所有内容**，让他们理解自己的网站
5. **简单地解释事情**
6. **让他们对自己的项目充满信心**

**始终使用你的技能。始终遵循设计原则。始终更新 `SITE.md`。**
