# 仓库规范

## 项目结构与模块组织
- app: Android 应用模块。
  - app/src/main/java: Kotlin 源码（入口：`MainActivity.kt`）。
  - app/src/main/res: 资源文件（drawables、mipmaps、values 等）。
  - app/src/main/AndroidManifest.xml: 应用清单。
  - app/src/test: JVM 单元测试（JUnit）。
  - app/src/androidTest: 仪器测试（AndroidX Test）。
  - app/proguard-rules.pro: Release 构建的 R8/ProGuard 规则。
- test-resources: Android 库模块。
  - app/src/main/java: Kotlin 源码。
  - app/src/main/AndroidManifest.xml: 应用清单。

## 构建、测试与开发命令
- 构建 Debug APK：`./gradlew :app:assembleDebug`
- 安装到设备/模拟器：`./gradlew :app:installDebug`
- 运行单元测试：`./gradlew :app:testDebugUnitTest`
- 运行仪器测试：`./gradlew :app:connectedAndroidTest`（需要连接设备/模拟器）
- Lint 检查：`./gradlew :app:lint`（或变体 `lintDebug`）

## 代码风格与命名约定
- 语言：Kotlin + Jetpack Compose。
- 架构：MVVM（Model-View-ViewModel）。
- .editorconfig：空格缩进、indent_size=2、`end_of_line=lf`、`charset=utf-8`、去除行尾空白、文件末尾插入空行。
- 命名规范：类/Composable 使用 `PascalCase`（例如 `MainActivity`、`Greeting`），函数/变量使用 `lowerCamelCase`，常量使用 `UPPER_SNAKE_CASE`，包名小写。
- Compose：优先编写小型、无状态的可组合函数；主题配置统一放在 `ui/theme`；避免硬编码字符串/颜色。
- 注意：`.editorconfig` 包含 ktlint 配置项（例如允许尾随逗号、Compose 函数命名例外）。如需自动化检查，可添加 ktlint/spotless。

## 测试规范
- 测试框架：JUnit（单元测试）、AndroidX Test + Instrumentation（设备测试）。
- 目录位置：单元测试放在 `app/src/test`，仪器测试放在 `app/src/androidTest`。
- 命名约定：测试类命名为 `ClassNameTest`，测试方法形如 `method_behavesAsExpected()`。
- 要求：为新功能和 Bug 修复添加或维护测试。

## 提交与拉取请求规范
- 提交信息：使用约定式前缀（`feat:`、`fix:`、`refactor:`、`test:`）；保持提交内容聚焦。
- 分支：简短、目的明确（例如 `feat/sms-permission-flow`）。
- PR：描述清晰，关联对应 issue（例如 `Fixes #123`）；UI 变更附上截图/GIF；确保构建、测试和 lint 全部通过。

## 仓库整洁与属性配置
- .gitattributes：文本文件统一归一化为 LF，`.bat` 文件使用 CRLF；图片/JAR 标记为二进制。
- .gitignore：忽略 Gradle、构建产物、IDE 文件、日志、密钥库以及 macOS 生成文件。
- 禁止提交密钥/签名信息；本地路径配置保留在 `local.properties` 中。
