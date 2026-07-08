# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在本仓库中工作时提供全面指导。

## 代码审查指南

对 Pull Request 进行代码审查时：

### 反馈结构
- **重要**：对非可执行反馈、说明或背景信息使用可折叠区域（`<details>` 标签）
- 将可执行项（bug、必需修改）默认保持可见
- 对非关键建议使用以下格式：

```markdown
<details>
<summary>💡 建议：[简要描述]</summary>

[详细说明或理由]

</details>
```

### 审查格式示例
```markdown
## 审查总结
✅ **必需修改**（默认可见）
- 修复第 42 行的内存泄漏
- 为 null 情况添加错误处理

<details>
<summary>📚 代码质量观察</summary>

- 考虑使用提前返回以减少嵌套
- 该函数可拆分为更小的单元
- 变量命名可更具描述性

</details>

<details>
<summary>🔍 性能考虑</summary>

虽然并非关键，但你可以考虑：
- 使用 map 替代重复的数组查找
- 缓存编译后的正则表达式

</details>
```

### 审查优先级
1. **始终可见**：安全问题、bug、破坏性变更
2. **可折叠**：风格建议、 minor 优化、教育性内容
3. **重点关注**：建设性、可执行的反馈，避免吹毛求疵

## 项目概览

Antimetal Agent 是一个 Kubernetes 控制器，用于将基础设施连接到 Antimetal 平台进行云资源管理。它收集 K8s 资源、监控系统性能，并通过 gRPC 流式传输数据。

### 关键技术
- **Go 1.24** 与 controller-runtime 框架
- **Kubernetes** 自定义控制器模式
- **gRPC** 用于向 intake 服务流式传输数据
- **BadgerDB** 用于嵌入式资源存储
- **Docker** 支持多架构（linux/amd64、linux/arm64）
- **KIND** 用于本地开发与测试

## 架构概览

### 核心组件

| 组件 | 路径 | 用途 |
|-----------|------|---------|
| **Kubernetes Controller** | `internal/kubernetes/agent/` | 监听资源、调和、 leader 选举 |
| **Intake Worker** | `internal/intake/` | gRPC 流式传输、批量处理、重试逻辑 |
| **Performance Monitoring** | `pkg/performance/` | 从 /proc 与 /sys 采集系统指标 |
| **Resource Store** | `pkg/resource/store/` | BadgerDB 存储、RDF 三元组、事件订阅 |
| **Cloud Providers** | `internal/kubernetes/cluster/` | EKS、KIND、可扩展的 provider 接口 |

### 目录结构
- `cmd/` - 应用入口
- `internal/` - 私有应用代码（intake、kubernetes controller）
- `pkg/` - 公共包（aws、performance、resource store）
- `config/` - K8s 清单与 Kustomize
- `ebpf/` - eBPF 程序与构建系统

## 开发工作流

### 前置条件
- **Docker**（rootless，启用 containerd snapshotter）
- **kubectl** 用于 K8s 操作
- **Go 1.24+**（如 go.mod 所指定）

### 常用命令

运行 `make help` 查看完整列表。关键命令：

| 类别 | 命令 | 用途 |
|----------|---------|---------|
| **Build** | `make build` | 为当前平台构建二进制 |
| | `make build-all` | 为所有平台构建 |
| | `make docker-build-all` | 构建多架构 Docker 镜像 |
| **Test** | `make test` | 运行测试并输出覆盖率 |
| | `make lint` | 运行 golangci-lint |
| | `make fmt` | 格式化 Go 代码 |
| | `make fmt.clang` | 格式化 C/C++/eBPF 代码 |
| **Generate** | `make generate` | 生成 K8s 清单 |
| | `make gen-license-headers` | **提交前务必运行** |
| **KIND** | `make cluster` | 创建本地 KIND 集群 |
| | `make build-and-load-image` | 快速重新构建并部署 |
| | `make destroy-cluster` | 删除 KIND 集群 |

### 关键开发模式

#### 代码生成
在以下修改后**务必**运行 `make generate`：
- 修改 kubebuilder 注解（`+kubebuilder:rbac`）
- 更改 CRD 定义
- 更新 webhook 配置

#### 许可证头
- **务必**在提交前运行 `make gen-license-headers`
- **所有** .go 文件必须包含位于 @tools/license_check/license_header.txt 的 PolyForm Shield 许可证头

#### 测试理念
- 使用标准 Go 测试框架
- 测试与实现文件位于同一目录
- 使用表驱动测试以全面覆盖
- 对外部依赖进行 mock（gRPC、AWS、K8s）

#### Git 提交与 PR
- **务必**在创建提交前运行 `make lint-fix`
- **务必**使用 `commit-author` agent 创建提交信息、审查提交或生成 PR 描述
- 该 agent 确保符合项目提交约定与格式标准

#### Linux 系统与 eBPF 开发
- 在开发或调试 Linux 系统采集器、eBPF 程序或 /proc、/sys 解析器时，**务必**使用 `linux-systems-expert` agent
- 该 agent 对内核接口、CO-RE/BTF、性能监控与跨内核兼容性有深入了解

## 性能采集器

Antimetal Agent 包含全面的性能监控系统，从 /proc 与 /sys 文件系统收集系统指标。采集器遵循双接口模式（PointCollector 用于一次性采集，ContinuousCollector 用于流式采集），并采用标准化的错误处理与测试方法。

**关键概念：**
- 构造器模式，包含路径验证与能力检查
- 采集器注册表用于管理采集器
- 对可选数据进行优雅降级
- 使用 mock 文件系统进行完整测试

有关性能采集器开发的详细内容（实现模式、测试方法、持续采集器与示例），请参阅 **[docs/performance-collectors.md](docs/performance-collectors.md)**。

### 容器指标采集

Agent 通过 cgroup 采集器支持容器级指标：

- **自动版本检测**：支持 cgroup v1 与 v2
- **多运行时支持**：Docker、containerd、CRI-O、Podman
- **零配置**：无需运行时 API 即可自动发现容器
- **优雅降级**：处理缺失文件与权限不足情况

有关实现细节，请参阅 system-agent wiki 中关于 cgroup 采集器的文档。

## 资源存储架构

### BadgerDB 集成
- 开发/测试使用**内存存储**
- **事件驱动订阅**用于实时更新
- **RDF 三元组关系**（subject、predicate、object）
- **高效索引**用于复杂查询

### 存储模式
```go
// 资源存储
AddResource(rsrc *Resource) error
UpdateResource(rsrc *Resource) error
DeleteResource(ref *ResourceRef) error

// 关系存储（RDF 三元组）
AddRelationships(rels ...*Relationship) error
GetRelationships(subject, object *ResourceRef, predicate proto.Message) error

// 事件订阅
Subscribe(typeDef *TypeDescriptor) <-chan Event
```

## gRPC 集成

### Intake 服务通信
- **流式 gRPC** 用于高效数据上传
- **增量批量**处理，批量大小可配置
- **指数退避**用于连接失败重试
- **流恢复**与自动重连
- **心跳机制**用于连接健康检查

### 数据流
1. K8s 事件 → Controller → Resource Store
2. Resource Store → Event Router → Intake Worker
3. Intake Worker → Batching → gRPC Stream → Antimetal

## 多云 Provider 支持

### Provider 接口
```go
type Provider interface {
    Name() string
    ClusterName(ctx context.Context) (string, error)
    Region(ctx context.Context) (string, error)
}
```

### 支持的 Provider
- **EKS**：完整的 AWS 集成与自动发现
- **KIND**：本地开发支持
- **GKE/AKS**：接口已定义，实现待完成

## 配置管理

### 命令行标志
全面的标志系统，涵盖：
- Intake 服务配置
- Kubernetes provider 设置
- 性能监控选项
- 安全与 TLS 设置

### 环境变量
- `NODE_NAME`：节点标识
- `HOST_PROC`、`HOST_SYS`、`HOST_DEV`：容器化文件系统路径

## 安全考虑

### 许可证管理
- 源代码使用 **PolyForm Shield License**
- 通过 Python 脚本强制添加许可证头
- 自动生成许可证头

### 运行时安全
- **非 root 容器**执行（用户 65532）
- **最小化 distroless 基础**镜像
- gRPC 连接**默认启用 TLS**
- 通过 kubebuilder 注解配置 **RBAC 权限**

## 调试与监控

### 日志
- 使用 logr 进行**结构化日志**
- 使用组件名进行**上下文日志**
- 通过 zap 配置**日志级别**

### 指标与健康检查
- 通过 controller-runtime 暴露 **Prometheus 指标**
- **健康检查**（`/healthz`、`/readyz`）
- 支持 **Pprof** 进行性能分析

### 调试命令
```bash
kubectl logs -n antimetal-system <pod-name>
kubectl get pods -n antimetal-system
kubectl describe deployment -n antimetal-system agent
```

## 构建与发布

### Docker 多架构
- 支持 **linux/amd64** 与 **linux/arm64**
- 使用 **GoReleaser** 自动化发布
- 使用 **Distroless base** 最小化攻击面

### 部署
- 使用 **Kustomize** 进行配置管理
- **Helm charts** 单独发布
- 默认 **antimetal-system** 命名空间

## 测试策略

### 单元测试
- **对外部依赖进行 mock**（gRPC、AWS、K8s）
- **表驱动测试**以全面覆盖
- **临时文件系统**用于隔离
- 使用 **Testify** 进行断言与 mock

### 集成测试
- **KIND 集群**用于 K8s 集成
- **Mock intake 服务**用于 gRPC 测试
- **内存中的 BadgerDB**用于存储测试

#### 集成测试环境假设
集成测试（带有 `//go:build integration` 标签的文件）应始终假设：
- **Linux 环境**：不要检查 `runtime.GOOS` —— 集成测试仅在 Linux 上运行
- **权限正确**：不要检查 `os.Geteuid()` —— 假设测试具备所需权限（root、CAP_BPF 等）
- **所需能力**：对权限相关操作使用 `require.NoError()` 而非跳过
- **内核特性**：检查内核版本以确认特性可用性，但不要因操作系统类型而跳过

正确的集成测试设置示例：
```go
//go:build integration

func TestEBPFFeature(t *testing.T) {
    // 不要：if runtime.GOOS != "linux" { t.Skip() }
    // 不要：if os.Geteuid() != 0 { t.Skip() }
    
    // 正确：假设 Linux 且权限正确
    err := rlimit.RemoveMemlock()
    require.NoError(t, err, "Failed to remove memlock - integration tests require proper permissions")
    
    // 正确：检查内核版本以确认特性支持
    kernel, _ := GetCurrentVersion()
    if !kernel.IsAtLeast(5, 8) {
        t.Skip("Feature requires kernel 5.8+")
    }
}
```

### 性能测试
- 对关键路径进行 **Benchmarks**
- 使用真实数据量进行 **负载测试**
- **内存分析**用于优化

## 开发说明

### 代码风格

#### Golang
- 使用**提前返回**减少嵌套
- 在适用处使用**函数式模式**
- 保持**简洁实现**，避免不必要的注释
- 使用上下文进行**错误包装**
- **始终使用 `any` 而非 `interface{}`**
- 提交前**始终使用 `make fmt` 格式化**

#### C/C++ 与 eBPF 代码
- 基础采用 **Google C++ Style**（通过 `.clang-format`）
- **指针对齐**：`Type* variable`（指针紧贴类型）
- **缩进宽度**：2 个空格
- **列限制**：80 字符
- 提交前**使用 `make fmt.clang` 格式化**
- **包含顺序**：vmlinux.h 优先，然后是系统头文件，最后是本地头文件

### 常见陷阱
- 修改注解后务必运行 `make generate`
- 提交前不要忘记许可证头
- 在 AMD64 与 ARM64 架构下均进行测试
- 使用真实数据验证 /proc 文件解析

### 性能优化
- 通过适当索引**高效使用 BadgerDB**
- **批量 gRPC 操作**以提高网络效率
- **上下文取消**用于优雅关闭
- **内存池**用于高频操作

## eBPF 开发

Antimetal Agent 支持基于 eBPF 的采集器，以实现深度内核可观测性，并使用 CO-RE（Compile Once - Run Everywhere）技术，在 4.18+ 内核版本中保持可移植性。

**关键命令：**
- `make build-ebpf` - 构建支持 CO-RE 的 eBPF 程序
- `make generate-ebpf-bindings` - 从 eBPF C 代码生成 Go 绑定

有关 eBPF 开发的详细指导（CO-RE 支持、新增程序、故障排查与最佳实践），请参阅 **[docs/ebpf-development.md](docs/ebpf-development.md)**。

## Wiki 文档集成

项目在 GitHub Wiki 中维护全面文档，以 git submodule 形式位于 `.wiki/` 目录。

### Wiki-Keeper Agent

**重要**：所有 wiki 操作**务必**通过 Task 工具使用 `wiki-keeper` agent。该专业 agent：
- 动态读取 `.wiki/CLAUDE.md` 了解当前约定
- 搜索、分析、更新与创建文档
- 返回简洁摘要，无需加载完整内容
- 显著降低上下文占用

#### 何时使用 Wiki-Keeper

在以下场景使用 wiki-keeper agent：
- 实现功能前**搜索文档**
- **检查功能是否已有文档**
- 代码变更后**更新文档**
- 为新功能**创建新文档**
- **分析文档完整性**
- **查找架构决策与设计模式**

#### 使用示例

```python
Task(
    subagent_type="general-purpose",
    description="Search wiki for [topic]",
    prompt="""
    You are the wiki-keeper agent. Your instructions are in .claude/agents/wiki-keeper.md.
    Work from the .wiki/ directory.
    IMPORTANT: First read .wiki/CLAUDE.md for wiki-specific conventions.
    
    Task: [Your specific task here]
    Context: [Any relevant context about code changes]
    Return: [What you need back - summaries, locations, gaps, etc.]
    """
)
```

wiki-keeper 返回结构化响应，包括文件路径、简要摘要与具体建议。

#### 最佳实践

1. **始终使用 wiki-keeper** 代替直接读取 wiki 文件
2. 请求更新时**提供代码变更上下文**
3. **信任 agent 的摘要** —— 避免请求完整内容

### Git 操作

```bash
# 务必拉取最新 wiki 变更（不固定到特定提交）
git submodule update --remote --merge .wiki

# 首次克隆时初始化 wiki
git submodule init && git submodule update --remote .wiki

# wiki-keeper 修改文档后
cd .wiki && git add -A && git commit -m "docs: [description]" && git push
cd ..

# 重要：避免提交 .wiki submodule 引用
# 如果你在 git status 中看到 .wiki 被修改，不要暂存它
git add .  # 暂存你的变更
git reset .wiki  # 取消暂存 submodule 引用
git commit -m "your changes"  # 提交，不更新 wiki 引用
```

**重要**：wiki 跟踪 `master` 分支，应始终使用最新文档，而非固定提交。使用 `--remote` 标志获取最新变更。

### 代码引用

在代码注释中引用 wiki 文档时：
```go
// See wiki: Cgroup/Memory-Collector.md for algorithm details
```
