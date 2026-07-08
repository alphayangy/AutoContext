# 仓库指南

## 项目结构与模块组织
这是一个 Ruby gem。主入口为 `lib/command_line_reporter.rb`，核心类位于 `lib/command_line_reporter/` 下（表格、行、列、选项校验），格式化器实现位于 `lib/command_line_reporter/formatter/`。RSpec 测试存放于 `spec/`，共享辅助方法与匹配器位于 `spec/support/`。打包与工具文件包括 `command_line_reporter.gemspec`、`Gemfile`、`Rakefile` 与 `Guardfile`。

## 构建、测试与开发命令
- 使用 Ruby 3.4.8（见 `.ruby-version`），运行命令前先执行 `bundle install`。
- `bundle install` 安装开发与运行依赖。
- `bundle exec rspec` 运行完整测试套件。
- `bundle exec guard` 在文件变更时运行测试（依据 `Guardfile`）。
- `bundle exec rubocop` 依据 `.rubocop.yml` 检查代码风格。
- `bundle exec rake build` 构建 gem 包（Bundler gem 任务）。

## 编码风格与命名规范
- Ruby 代码使用 2 空格缩进。
- 使用标准 Ruby 命名：方法/变量用 `snake_case`，类/模块用 `CamelCase`。
- 遵循 `.rubocop.yml`（行长度限制已禁用；默认不要求文档）。
- 将与格式化器相关的代码保留在 `lib/command_line_reporter/formatter/`，公共 API 方法保留在 `CommandLineReporter` 模块内。

## 测试指南
- RSpec 为测试框架；文件使用 `*_spec.rb` 命名模式。
- 通过 `spec/spec_helper.rb` 加载共享辅助方法。
- 新增或更新测试应贴近其所覆盖的功能（例如，`lib/command_line_reporter/table.rb` → `spec/table_spec.rb`）。
- 不强制执行显式的覆盖率阈值。

## 提交与合并请求指南
- 历史提交信息简短且具描述性（通常为小写，例如 "version bump"、"updated documentation"）。保持摘要简洁且聚焦。
- 优先使用小而单一目的的提交，描述意图或受影响范围。
- 合并请求应包含：简短的问题陈述、变更摘要、已运行的测试以及任何行为变更。如适用，请关联相关 issue。
