# Claude Code 智能体说明

## YouTrack 工单工作流

### 开始工作前

1. **询问用户 YouTrack 工单的 ID 或编号**（例如 "DBA-123" 或仅 "123"，你可以将其扩展为 "DBA-123"）。如果 YouTrack MCP 不可用，请引导用户查看 [DEVELOPMENT.md](DEVELOPMENT.md) 以获取设置说明。

2. **如果提供了工单：** 使用 `get_issue` 读取工单，以了解范围、上下文以及任何相关讨论，然后再继续。

3. **如果不存在工单：** 在创建之前先向用户提议一个——展示人类可读的预览信息（摘要、描述、类型、状态、Sprint），并等待批准。仅在确认后创建。

### 提交信息

提交信息中务必包含工单 ID：
```
[DBA-123] Add support for Snowflake authentication
```

### 创建 Pull Request 后

使用 `update_issue` 将关联的 YouTrack 工单移动到 **Review** 状态。

## 完成工作后

完成变更实现后：

1. **运行 pre-commit 检查：**
   ```bash
   make check
   # or directly: uv run pre-commit run --all-files
   ```

2. **运行测试：**
   ```bash
   make test
   # or directly: uv run pytest -v
   ```

3. **检查通过后**，告知用户你可以帮助创建分支、提交变更并创建 pull request。

在继续操作之前，等待用户确认。

### 如果用户确认

1. **检查 GitHub CLI 是否已安装：**
   ```bash
   gh auth status
   ```

   如果未安装或未通过身份验证，请引导用户查看 [DEVELOPMENT.md](DEVELOPMENT.md) 以获取设置说明。他们也可以选择手动创建 PR。

2. **确定分支名称前缀：**
   - 从现有远程分支中提取分支前缀，过滤掉系统前缀（dependabot、revert-*、HEAD）
   - 使用最常见的匹配前缀作为用户的昵称
   - 如果找不到现有分支，请询问用户的昵称
   - 分支格式：`<nickname>/<descriptive-branch-name>`

   策略：
   ```bash
   # Extract and count branch prefixes, excluding system prefixes
   git branch -r | sed -nE 's|^ *origin/([^/]+)/.*|\1|p' | grep -vE '^(dependabot|HEAD|revert-)' | sort | uniq -c | sort -rn
   ```

3. 使用合适的前缀**创建一个独立分支**（切勿直接提交到 main）

4. 使用清晰、描述性的提交信息**提交变更**

5. 按以下格式**创建 Pull Request**：

### Pull Request 格式

```markdown
## Summary
Brief overview of what was changed and why.

## Changes

### Change 1: [Feature/Fix Name]
Brief description of this specific change.

<details>
<summary>Affected files</summary>

- `path/to/file1.py`
- `path/to/file2.py`
- `path/to/file3.py`

</details>

### Change 2: [Another Feature/Fix Name]
Brief description of this specific change.

<details>
<summary>Affected files</summary>

- `path/to/file4.py`
- `path/to/file5.py`

</details>

## Test Plan
- How the changes were tested
- Any manual testing steps required
```

### 指南

- 每个逻辑变更应作为独立的小节
- 在可折叠的 `<details>` 块中列出所有受影响文件
- 保持描述清晰简洁
- 为审查者提供相关上下文
