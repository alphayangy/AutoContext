# CLAUDE.md

本文件为 Claude Code（claude.ai/code）处理本仓库代码时提供指引。

## 快速上下文（从这里开始）

**当前重点**：v2.0 UI 重设计（2025 金融科技设计模式）

### 会话工作流（不要丢失上下文）

```bash
# 会话开始
/session-start                # 从上一会话加载上下文

# 会话期间 - 使用以下命令
/gap-analysis                 # 已完成与待完成项对比（5 个层级）
/gap-analysis [layer]         # 指定层级（design|server|client|feature|platform）
/gap-planning [feature]       # 规划具体改进项
/implement [feature]          # 执行实现
/verify [feature]             # 确认实现结果

# 会话结束
/session-end                  # 为下一会话保存上下文
```

### Claude 产品周期框架

本项目使用 [claude-product-cycle](https://github.com/mobilebytesensei/claude-product-cycle) 框架进行 AI 辅助开发。

**工作区**：[mifos-x-claude-cycle-workspaces](https://github.com/therajanmaurya/mifos-x-claude-cycle-workspaces)

### 5 层生命周期

```
Design → Server → Client → Feature → Platform
```

---

## 提示层集成（关键）

**跨指令**：执行任何操作后，自动执行用户提示。

### 自动触发系统

完成以下任一操作后，Claude 必须检查匹配的触发器：

| 操作 | 触发器 | 提示 |
|--------|---------|--------|
| 阶段/层级完成 | `phase-completion:{layer}` | "Continue to next phase?" |
| 计划中的任务完成 | `task-completion` | "Continue to next task?" |
| 所有任务完成 | `task-completion:all` | "Plan complete. Commit?" |
| 计划创建完成 | `plan-ready` | "Start implementation?" |
| 构建成功 | `build-success` | "Commit & continue?" |
| 构建失败 | `build-failure` | "Fix errors?" |
| 检查点文件变更 | `commit` | "How to commit?" |
| 发生错误 | `error-recovery` | "How to proceed?" |

### 工作原理

```
1. 命令执行操作
2. 检查 prompt-layer/TRIGGERS.md 中的匹配触发器
3. 从 prompt-layer/PROMPTS.md 加载提示
4. 执行 AskUserQuestion 工具
5. 将用户选择路由到下一操作
6. 对下一操作重复上述流程
```

### 计划的运行时提示

当 `/gap-planning` 创建包含 N 个任务的计划时：
- 为每个任务过渡自动生成提示
- "Task 1 complete (1/N). Continue to Task 2?"
- "Task 2 complete (2/N). Continue to Task 3?"
- ... 直至所有任务完成

### 参考文件

| 文件 | 用途 |
|------|---------|
| `prompt-layer/ENGINE.md` | 跨指令规则 |
| `prompt-layer/TRIGGERS.md` | 触发条件 |
| `prompt-layer/PROMPTS.md` | 提示定义 |
| `prompt-layer/RUNTIME.md` | 动态计划提示 |

**重要**：不要 hardcode 提示到命令中。让引擎自动处理。

---

## 项目概览

Mifos Mobile 是一款面向 MifosX 自助服务平台的 Kotlin Multiplatform（KMP）应用，让终端用户能够查看/操作其账户与贷款。它面向 Android、iOS、桌面端（JVM）以及 Web（Kotlin/JS + WASM）。

## 构建命令

```bash
# 构建项目
./gradlew build

# 运行所有预推送检查（推荐在创建 PR 前执行）
./ci-prepush.sh

# 单独检查
./gradlew check -p build-logic                     # 验证 build-logic 配置
./gradlew spotlessApply --no-configuration-cache   # 应用代码格式化
./gradlew dependencyGuardBaseline                  # 生成 dependency-guard 基线
./gradlew detekt                                   # 运行静态分析

# 运行测试
./gradlew testDebug                                # 运行 debug 单元测试
./gradlew :core:data:test                          # 运行指定模块测试

# Lint 检查
./gradlew :cmp-android:lintRelease                 # 对 Android 应用运行 lint

# Android 构建
./gradlew :cmp-android:assembleDemoDebug           # 构建 demo debug APK
./gradlew :cmp-android:assembleProdRelease         # 构建 production release APK
```

## 架构

### 模块结构

**平台入口：**
- `cmp-android/` - Android 应用模块
- `cmp-ios/` - iOS 应用（通过 `cmp-shared` 使用 CocoaPods）
- `cmp-desktop/` - 桌面（JVM）应用
- `cmp-web/` - Web 应用（Kotlin/JS）
- `cmp-shared/` - 编译到所有平台的共享 KMP 模块
- `cmp-navigation/` - 使用 Compose Navigation 的跨平台导航

**核心模块（`core/`）：**
- `data/` - 仓库实现，连接网络与 UI
- `network/` - 基于 Ktorfit 的 API 服务与 HTTP 客户端
- `model/` - 跨功能共享的领域模型
- `datastore/` - 本地数据持久化（DataStore）
- `database/` - Room 数据库（KMP）
- `ui/` - 共享 UI 组件
- `designsystem/` - 设计 token、主题、通用 composable
- `common/` - 共享工具类
- `qrcode/` - 二维码生成/扫描

**核心基础模块（`core-base/`）：** 跨模板系统共享的平台抽象实现。

**功能模块（`feature/`）：** 每个功能都是独立的 KMP 模块，包含页面、ViewModel 和导航。功能包括：auth、home、accounts、loan-account、savings-account、beneficiary、transfer-process 等。

**库模块（`libs/`）：** 内部库，如 country-code-picker、mifos-passcode、material3-navigation。

### 关键模式

**依赖注入：** 所有平台使用 Koin。每个模块在其 `di/` 包中定义 Koin 模块。

**导航：** 使用 Jetbrains Compose Navigation。导航图定义在 `cmp-navigation/`：
- `ROOT_GRAPH` → `AUTH_GRAPH` → `PASSCODE_GRAPH` → `MAIN_GRAPH`

**网络层：** 使用 Ktorfit（Ktor 的 Retrofit 风格方案），服务位于 `core/network/services/`。Base URL：`https://tt.mifos.community/fineract-provider/api/v1/self/`

**状态管理：** ViewModel 配合 StateFlow/SharedFlow。功能使用 `ScreenState<T>` 模式处理加载/成功/错误状态。

### Convention Plugins

`build-logic/convention/` 中的自定义 Gradle 插件用于标准化模块配置：
- `mifos.android.application` - Android 应用配置
- `org.convention.cmp.feature` - KMP 功能模块（应用 Compose、Koin、核心依赖）
- `org.convention.kmp.library` - KMP 库模块
- `mifos.kmp.room` - KMP 的 Room 数据库配置
- `mifos.spotless.plugin`、`mifos.detekt.plugin` - 代码质量

### 构建变体

Android 有两个产品变体：
- `demo` - 开发/测试
- `prod` - 生产

## 开发注意事项

- 需要 JDK 21（见 `build-logic/convention/build.gradle.kts`）
- 拉取请求目标分支为 `development`
- 提交信息格式：`<type>(<scope>): <subject>`（feat、fix、docs、refactor、test、chore）
- Demo 凭据：实例 `gsoc.mifos.community`，用户名 `maria`，密码 `password`

## Git 提交与 PR 规范

- **始终使用功能分支**：不要直接推送到 `development` 分支
  - 创建功能分支：`git checkout -b feature/[description]`
  - 推送到功能分支：`git push origin feature/[description]`
  - 创建目标为 `development` 分支的 PR
- **不要出现 Claude 引用**：不要在提交或 PR 中添加 Claude 署名、co-author 行或 "Generated with Claude Code" 脚注
- 保持提交信息干净，聚焦所做改动
- PR 描述只应包含相关技术信息
