# CLAUDE.md

本文件为 Claude Code（claude.ai/code）提供针对本仓库代码的工作指引。

## 开发命令

### 常用命令

```bash
# 安装依赖
npm install

# 运行开发服务器（http://localhost:3000）
npm run dev

# 构建生产版本
npm run build

# 启动生产服务器
npm start

# 运行代码检查
npm run lint

# 类型检查
npm run typecheck
```

## 架构概览

这是一个 Next.js 15 启动模板，集成了 TypeScript、Tailwind CSS 和 Supabase。适用于构建现代落地页、SaaS 应用，或任何需要以下特性的 Web 项目：

- **Next.js 15.3.3**，使用 App Router
- **TypeScript**，已启用严格模式
- **Tailwind CSS**，带有自定义设计系统
- **Framer Motion**，用于动画效果
- 已集成 **Supabase**
- 支持**邮件收集**与数据分析

### 关键架构决策

1. **组件架构**：`src/components/` 下的所有组件均为客户端（`'use client'`）React 函数组件，使用 TypeScript 编写。每个组件自包含动画与样式。

2. **设计系统**：自定义 CSS 变量定义于 `globals.css`：
   - 主色：`rgb(218, 50, 41)`（可自定义）
   - 次色：`rgb(92, 38, 35)`（可自定义）
   - 强调色：`rgb(224, 57, 47)`（可自定义）
   - 深色主题：`rgb(23, 23, 23)`
   - 自定义工具类：`btn-primary`、`btn-secondary`、`gradient-text`、`glass-effect`

3. **路径别名**：`@/*` 映射至 `./src/*`，使导入更简洁。

4. **页面结构**：模块化落地页，由以下可复用区块组成：
   - 导航栏
   - 带动画文字的 Hero 区域
   - 视频预览
   - 功能特性区域
   - 技术栈展示
   - 用户评价
   - 讲师/团队区域
   - 定价方案
   - FAQ 手风琴
   - 邮件收集
   - 行动召唤
   - 页脚

## 自定义指南

### 1. 品牌与配色

更新 `src/app/globals.css` 中的 CSS 变量：

```css
:root {
  --brand-primary: 218 50 41;    /* 你的主色 */
  --brand-secondary: 92 38 35;   /* 你的次色 */
  --brand-accent: 224 57 47;     /* 你的强调色 */
}
```

### 2. Logo 与资源

替换 `/public/assets/logos/` 中的占位 Logo：
- `logo-light.svg` - 浅色主题完整 Logo
- `logo-dark.svg` - 深色主题完整 Logo
- `icon-light.svg` - 浅色主题仅图标（用于移动端）
- `icon-dark.svg` - 深色主题仅图标（用于移动端）

### 3. 内容更新

主要需要自定义的内容文件：
- `src/components/HeroOptimized.tsx` - 带轮播文字的 Hero 区域
- `src/components/Features.tsx` - 产品功能
- `src/components/Pricing.tsx` - 定价方案
- `src/components/Testimonials.tsx` - 客户评价
- `src/components/FAQ.tsx` - 常见问题

### 4. 环境变量

生产环境所需（创建 `.env.local`）：

```bash
# Supabase 配置
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# 邮件集成（可选）
KIT_API_KEY=your_kit_v4_api_key
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_TEMPLATE_ID=your_sendgrid_template_id

# 数据分析（可选）
NEXT_PUBLIC_MICROSOFT_CLARITY_ID=your_clarity_project_id
```

## 模板功能

### ✅ 已包含的组件
- 响应式导航栏与主题切换
- 带动画轮播文字的 Hero 区域
- 视频预览占位
- 可展开卡片的功能展示
- 技术栈展示
- 评价轮播
- 定价对比表
- FAQ 手风琴
- 邮件收集表单
- 行动召唤区域
- 带链接的页脚

### ✅ 技术特性
- 深色/浅色模式，支持系统偏好检测
- 完全响应式设计（移动优先）
- TypeScript 严格模式
- ESLint + Prettier 配置
- Framer Motion 动画
- Supabase 集成配置
- 邮件营销集成就绪
- SEO 优化
- 性能优化

### ✅ 开发体验
- 热重载开发服务器
- TypeScript IntelliSense
- 组件测试配置
- 自动代码格式化
- Git 预提交钩子就绪

## 快速开始

1. **安装依赖**
   ```bash
   npm install
   ```

2. **更新品牌信息**
   - 替换 `/public/assets/logos/` 中的 Logo
   - 更新 `src/app/globals.css` 中的配色
   - 自定义组件文件中的内容

3. **配置集成**
   - 创建 Supabase 项目
   - 添加环境变量
   - 配置邮件服务（可选）

4. **启动开发服务器**
   ```bash
   npm run dev
   ```

5. **自定义内容**
   - 更新 Hero 文案与信息
   - 添加你的功能与定价
   - 自定义评价与 FAQ

## 部署

本模板针对以下平台优化部署：
- **Vercel**（推荐）
- **Netlify**
- **AWS Amplify**
- 任意 Node.js 托管服务商

构建命令：`npm run build`
启动命令：`npm start`

## 支持

如有关于本模板的问题：
1. 查看组件文档
2. 查看示例实现
3. 查阅 Next.js 与 Tailwind CSS 官方文档
4. 在你的项目仓库中提交 issue

---

**注意**：这是一个启动模板。请根据你的品牌和需求进行自定义。所有占位内容都应替换为你的实际内容。
