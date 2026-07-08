# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在操作本仓库代码时提供指引。

## 项目概览

Trigger 是一套成熟的 Python 网络自动化工具包，用于大规模管理网络设备。它最初由 AOL 网络安全团队于 2006 年开发，提供异步命令执行、ACL 解析与管理、以及基于元数据的多厂商设备交互能力，支持 Cisco IOS/NX-OS/ASA、Juniper Junos/ScreenOS、Force10 FTOS、Arista 等平台。

**关键特性：**
- Python 3.10-3.11 代码库（v2.0.0+；v1.6.0 已终止 Python 2.7 支持）
- 基于 Twisted 的异步 I/O 框架
- 企业级网络自动化规模（数百至数千台设备）
- 基于语法的 ACL 解析与格式转换
- 基于 Redis 的 ACL 数据库与部署队列

## 开发命令

### 运行测试

**单元测试：**
```bash
# 运行所有单元测试
pytest

# 以详细模式运行
pytest -vv

# 运行指定测试文件
pytest tests/test_acl.py

# 运行并生成覆盖率报告
pytest --cov=trigger tests/
```

**测试环境变量**（由 conftest.py 自动设置）：
- `TRIGGER_SETTINGS`：指向测试用 settings.py 的路径
- `NETDEVICES_SOURCE`：指向测试用 netdevices.xml 的路径
- `AUTOACL_FILE`：指向测试用 autoacl.py 的路径
- `BOUNCE_FILE`：指向测试用 bounce.py 的路径
- `TACACSRC`：指向测试用 tacacsrc 凭据文件的路径
- `TACACSRC_KEYFILE`：指向测试用 tackf 密钥文件的路径

### 代码检查

Trigger 使用 [ruff](https://docs.astral.sh/ruff/) 进行快速的 Python 代码检查与格式化。

**自动检查（推荐 - pre-commit 钩子）：**
```bash
# 安装 prek（一次性设置）
uv tool install prek  # 或：pip install prek

# 为本仓库启用钩子
prek install

# 钩子会在 git commit 时自动运行
git commit -m "your changes"
```

**手动检查：**
```bash
# 检查代码风格
ruff check trigger/ tests/ configs/

# 自动修复安全问题
ruff check trigger/ tests/ configs/ --fix

# 检查格式化
ruff format --check trigger/ tests/ configs/

# 自动格式化代码
ruff format trigger/ tests/ configs/
```

**检查内容：**
- Ruff 代码检查（与 CI 配置保持一致）
- Ruff 格式化检查（在 pre-commit 中仅做检查）
- YAML 语法、行尾空白、合并冲突标记
- 防止向 main 分支直接提交

### Pre-commit 钩子

Trigger 使用 [prek](https://prek.j178.dev/) 作为快速的 pre-commit 钩子，在提交前自动检查代码。

**安装 prek：**
```bash
# 使用 uv（推荐，最快）
uv tool install prek

# 使用 pip
pip install prek

# 使用 pipx（隔离环境）
pipx install prek

# 或从 https://github.com/j178/prek/releases 下载独立二进制文件
```

**启用钩子：**
```bash
# 首次设置（从仓库根目录运行）
prek install

# 若更新了 .pre-commit-config.yaml，强制重新安装
prek install -f
```

**使用方式：**
```bash
# 钩子会在 git commit 时自动运行
git commit -m "your changes"

# 对已暂存文件手动运行所有钩子
prek run

# 对所有文件运行所有钩子
prek run --all-files

# 运行指定钩子
prek run ruff

# 跳过本次提交的钩子（请谨慎使用！）
git commit --no-verify
```

**性能：** prek 比传统 pre-commit 快 7-10 倍，且占用约一半的磁盘空间。

### 构建与安装

```bash
# 以开发模式安装，包含开发依赖
pip install -e ".[dev]"

# 生产环境安装
pip install .

# 构建分发包
python -m build

# 使用 uv（更快的包管理器）
uv pip install -e ".[dev]"
```

### 处理 Twisted 插件

修改 `twisted/plugins/trigger_xmlrpc.py` 后，请重新生成 dropin.cache：
```bash
python -c "from twisted.plugin import IPlugin, getPlugins; list(getPlugins(IPlugin))"
```

## 架构

### 核心组件层

**1. 命令执行层（`trigger/cmds.py`）**
- `Commando` 类：异步多设备命令执行的主要抽象
- 继承 `Commando` 并实现 `to_{vendor}()` 方法生成命令、`from_{vendor}()` 方法解析结果
- 根据设备元数据自动分发到厂商专属方法

**2. 设备元数据层（`trigger/netdevices/`）**
- `NetDevices`：所有受管网络设备的单例字典
- `NetDevice`：单个设备对象，包含厂商、型号、类型、ACL、位置等属性
- `Vendor`：规范化厂商映射（例如 "cisco-ios" → "cisco"）
- 可插拔加载器：文件系统（XML/JSON）、MongoDB、RANCID、CSV

**3. 连接与协议层（`trigger/twister.py`、`trigger/twister2.py`）**
- `twister.py`：基于 Twisted 的原始 SSH/Telnet/Junoscript 连接实现（约 2,000 行）
- `twister2.py`：基于 Crochet 的现代实现，桥接同步与异步代码
- 协议处理器：`TriggerSSHChannelFactory`、`TriggerSSHGenericChannel`、`IoslikeSendExpect`
- 负责认证、enable 模式、命令执行与输出捕获

**4. ACL 系统（`trigger/acl/`）**
- 基于 SimpleParse 的语法解析器（BNF 风格语法）
- 对象模型：`ACL` → `Term` → `Matches`（IP 地址、端口、协议）
- 在 Cisco IOS、Juniper JunOS 等格式之间进行转换
- `AclsDB`：基于 Redis 的 ACL 到设备映射
- `ACLQueue`：自动化 ACL 部署队列，支持手动与集成式工作流

**5. 配置（`trigger/conf/`）**
- 类 Django 风格的设置模块，通过 `TRIGGER_SETTINGS` 环境变量加载
- `global_settings.py`：所有默认值（平台、厂商、认证、网络定义）
- 创建自定义 settings.py 并将 `TRIGGER_SETTINGS` 指向它，即可覆盖默认设置

### 关键设计模式

- **单例模式**：`NetDevices` 确保设备元数据只加载一次
- **工厂模式**：`vendor_factory()` 缓存 `Vendor` 对象
- **策略模式**：通过 `to_{vendor}()` / `from_{vendor}()` 方法实现厂商专属行为
- **插件架构**：元数据加载器、Commando 插件
- **异步/Deferred 模式**：全代码库使用 Twisted Deferred 实现非阻塞 I/O

### 数据流：命令执行

```
用户代码（Commando 子类）
    ↓
NetDevices.find() → NetDevice 对象
    ↓
Device.execute() [按厂商动态绑定]
    ↓
凭据获取（.tacacsrc）
    ↓
协议选择（SSH/Telnet/Junoscript）
    ↓
创建 Twisted 通道
    ↓
认证与命令执行
    ↓
from_{vendor}() 结果解析
    ↓
回调用户代码
```

## 重要模块位置

- **`trigger/cmds.py`**：多设备命令执行的 `Commando` 类
- **`trigger/twister.py`**：SSH/Telnet 连接处理与协议实现
- **`trigger/netdevices/__init__.py`**：设备元数据核心（`NetDevices`、`NetDevice`）
- **`trigger/acl/parser.py`**：ACL 语法解析器
- **`trigger/acl/support.py`**：ACL 对象模型（`ACL`、`Term`、`Matches`）
- **`trigger/tacacsrc.py`**：加密凭据存储（GPG/旧版）
- **`trigger/changemgmt/bounce.py`**：维护窗口管理
- **`trigger/utils/`**：CLI 辅助工具、网络工具、通知、模板

## ACL 系统使用

ACL 系统支持解析、校验与格式转换：

```python
from trigger.acl import parse

# 解析任意受支持格式的 ACL
acl = parse("access-list 123 permit tcp any host 10.20.30.40 eq 80")

# 为 term 命名（输出 Juniper 格式前必需）
acl.name_terms()

# 转换为不同格式
junos_output = acl.output(format='junos')
ios_output = acl.output(format='ios')
```

**ACL 数据库集成：**
- Explicit ACLs：手动分配给设备
- Implicit ACLs：根据设备属性自动分配（通过 `autoacl.py`）
- Bulk ACLs：大规模策略集
- Redis 后端存储 ACL 到设备的映射

## CLI 工具（bin/）

- **`acl`**：交互式操作 ACL 对象
- **`aclconv`**：在不同厂商格式之间转换 ACL
- **`check_access`**：测试流量是否会被 ACL 允许
- **`find_access`**：查找符合特定条件的 ACL term
- **`load_acl`**：将 ACL 部署到设备
- **`netdev`**：从 NetDevices 查询设备元数据
- **`run_cmds`**：在多台设备上执行命令
- **`gong`**：交互式设备 shell
- **`gnng`**：高级交互式设备 shell
- **`optimizer`**：优化 ACL（移除冗余 term）

## 依赖与版本约束

- **Python 3.10-3.11**（v2.0.0+；v1.6.0 已终止 Python 2.7 支持）
  - 由于 SimpleParse C 扩展不兼容，Python 3.12+ 尚未支持
- **Twisted>=22.10.0**：异步网络框架
- **crochet>=2.0.0**：同步/异步桥接
- **pyparsing>=3.1.0**：ACL 语法解析器
- **cryptography>=41.0.0**：凭据加密
- **redis>=5.0.0**：ACL 数据库后端
- **SimpleParse>=2.2.0**：ACL 的 BNF 语法解析器（仅支持 Python 3.10-3.11）
- **textfsm>=1.1.0**：基于模板的输出解析
- **pyasn1>=0.4.8**：SSH 的 ASN.1 解析
- **IPy>=1.01**：IP 地址操作

## 测试策略

测试组织在 `tests/` 下：
- `test_acl.py`：ACL 解析、转换与操作（约 25K 行）
- `test_netdevices.py`：设备元数据与加载器
- `test_tacacsrc.py`：凭据存储
- `test_twister*.py`：连接与协议测试
- `tests/data/`：模拟配置文件（settings.py、netdevices.xml 等）
- `tests/acceptance/`：端到端验收测试

**测试用模拟数据**位于 `tests/data/`：
- `netdevices.xml`：模拟设备清单
- `settings.py`：测试配置覆盖
- `tacacsrc` / `tackf`：模拟凭据

## 配置与设置

Trigger 使用环境变量来定位配置：
- **`TRIGGER_SETTINGS`**：指向 settings.py 的路径（覆盖默认值）
- **`NETDEVICES_SOURCE`**：指向 netdevices 数据源的路径（XML/JSON 文件）
- **`AUTOACL_FILE`**：指向 autoacl.py 的路径（隐式 ACL 分配逻辑）
- **`BOUNCE_FILE`**：指向 bounce.py 的路径（维护窗口定义）
- **`TACACSRC`**：指向 .tacacsrc 加密凭据文件的路径
- **`TACACSRC_KEYFILE`**：指向 TACACS 密钥文件的路径

## 厂商支持

Trigger 通过以下方式抽象不同厂商的差异：
1. `global_settings.py` 中的**厂商映射**（例如 "CISCO_LIKE"、"JUNIPER_LIKE"）
2. 各厂商的**提示符模式**，用于检测命令执行完成
3. 在 `NetDevice` 对象上的**动态方法绑定**（例如 `device.execute()` 分派到厂商专属实现）
4. `trigger/acl/` 中**针对各格式的 ACL 语法**

支持的厂商包括：
- Cisco IOS、IOS-XR、NX-OS、ASA
- Juniper Junos、ScreenOS（Netscreen）
- Arista EOS
- Force10 FTOS
- Brocade、Dell、Foundry
- A10、Citrix NetScaler
- F5 BigIP

## 常见注意事项

- **Python 版本**：需要 Python 3.10-3.11（v2.0.0+）；由于 SimpleParse 限制，Python 3.12+ 尚未支持
- **v2.0.0 破坏性变更**：CLI 工具现在使用入口点；凭据/配置文件保持不变
- **Twisted Deferreds**：全代码库使用异步模式；需要正确处理 callback/errback
- **ACL term 命名**：输出 Juniper 格式前必须调用 `acl.name_terms()`
- **设备元数据加载**：`NetDevices()` 是单例；首次实例化时加载所有设备
- **凭据**：设备认证需要正确配置的 `.tacacsrc` 文件
- **厂商识别**：基于设备元数据而非自动发现；元数据必须准确
- **测试隔离**：测试使用 conftest.py 设置环境变量以使用模拟数据

## Git Worktrees

功能分支请始终使用 git worktree。Worktree 存放在 `.worktrees/`（已被 gitignore 忽略）。

```bash
# 为新功能分支创建 worktree
git worktree add .worktrees/<branch-name> -b <branch-name>
```

## 分支策略

- **`main`**：所有开发与发布的主分支。所有 PR 都应以 `main` 为目标。
- **请勿使用或针对 `develop` 分支。** 它是已不同步的遗留分支，应完全忽略。
- 发布标签：特定版本以 tag 形式提供（例如 `v2.0.1`）
- 合并 PR 时请**始终使用 rebase 合并**。不要创建合并提交。
