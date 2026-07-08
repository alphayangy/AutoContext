---
name: write-fuzzers-not-hand-tests
description: 在让 LLM 写测试时使用。防止"能过 review 但发现不了真 bug"的表演性手写测试,引导 LLM 写 fuzzer 和 property test。用于 coding 场景。
profiles: [coding]
scopes: [claude, rules]
priority: high
triggers:
  user_intents: [change-project]
conflicts: []
---

# 写 fuzzer,不写 hand-test

**LLM 默认写的测试是表演性的。引导它找真 bug。**

- LLM 默认写"看起来全面到能过人工 review"的测试,但只测 happy path。永远通过,发现不了 bug。
- 不要说"Write tests",改说"找风险点,定义不变量,fuzz 它们"。
- 给 LLM 明确指导怎么变 input 引出问题。不给指导,覆盖很差。
- fuzzer 和 property test 几分钟出真 bug。hand-test 一个都发现不了。

**准则生效的标志:** 生成的测试在对抗性输入上失败,而不只是在 happy path 上通过。
