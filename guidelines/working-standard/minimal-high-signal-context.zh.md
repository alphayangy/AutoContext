---
name: minimal-high-signal-context
description: 在 context 受限的 agent 里工作时使用。防止 context 腐烂和稀释,把工作 context 保持在达成目标所需的最小高信号 token 集。适用于所有 profile。
profiles: [all]
scopes: [claude]
priority: high
triggers: []
conflicts: []
---

# 最小高信号 context

**context 是有限资源。最大化每 token 的信号。**

- 只保留当前步骤所需的最小高信号 token 集。
- 按需加载细节:留一个轻量引用(路径、查询、链接),运行时再加载。不要预灌。
- 某个工具结果已被消费、内容已吸收后,把原始结果从 context 里丢掉。
- 如果 context 感觉被污染,或 agent 开始重复犯错,重置,用一个更好的初始 prompt 重新开始。
- token 多不等于能力强。边际收益递减。

**准则生效的标志:** 工作 context 聚焦在当前步骤,陈旧或已消费的内容被丢掉而不是拖着。
