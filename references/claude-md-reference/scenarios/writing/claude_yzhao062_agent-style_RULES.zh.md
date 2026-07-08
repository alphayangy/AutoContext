<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# 智能体文风要素 — 规则

每条规则包含以下内容：

- 元数据（来源引用、智能体指令依据、严重程度、适用范围、执行层级）
- 指令（命令式句子：反模式用否定表达，建设性用法用肯定表达）
- BAD → GOOD 示例（每条规则 5 组以上，至少包含一个非论文场景，如 API 文档、运维手册、提案、发布说明、事后复盘、变更日志或问题报告）
- 面向 AI 智能体的原理说明（该规则为何特别针对大语言模型输出）

## 严重程度分级

每条规则的严重程度按以下四级衡量：

- **critical（致命）** — 违反后读者无法理解或信任这段文字。
- **high（高）** — 外部可见的 AI 痕迹，或反复出现的清晰度问题，破坏速读。
- **medium（中）** — 局部可读性损失，读者能感受到，但不影响信任。
- **low（低）** — 润色或偏好问题；出于一致性标记，而非理解问题。

## 逃生舱（元原则）

> *"宁可打破这些规则，也不要说出任何彻底野蛮的话。"*
> —— George Orwell，《政治与英语》（1946），规则 6

规则是通往清晰的指南，而非目的本身。当规则与句子冲突时，放下规则。

## 12 条核心规则

### 受众与读者状态

#### RULE-01：不要假设读者拥有你的隐性知识（抵御知识的诅咒）

- **source**: Pinker 2014, Ch. 3 "The Curse of Knowledge"（整章都在讨论这一失效模式）。
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞（未验证机械执行）。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: critical。AI 生成技术散文最常见的审稿意见是"读起来像是忘了读者还不了解 X"。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-3 智能体自检（判断型规则，非机械执行）；Tier-4 Codex 审阅作为主要关卡。

##### Directive

不要在与读者背景水平不匹配时使用未经建立的技术术语或缩写。不要在说明目的之前直接进入机制细节。不要在没有先给出单句路线图的情况下写出多段论证。写作前先明确本文的预期读者：研究论文为相邻领域研究生，API 文档为初级工程师，运维手册为值班工程师，提案为跨组审稿人，变更日志为发布读者，或其他具体读者。如果该读者需要停下来推断某个术语的含义，就定义它或改写绕开它。

##### BAD → GOOD

- BAD: `We use contrastive learning with InfoNCE and a momentum encoder.`
- GOOD: `Our method trains a representation to separate similar from dissimilar image pairs (contrastive learning), with InfoNCE as the loss and a slowly-updating momentum encoder to stabilize training.`

- BAD: `The API uses JWT with RS256 refresh tokens rotated via the OIDC flow.`
- GOOD: `Authentication uses short-lived signed tokens (JWT with RS256) issued by our OIDC identity provider. Clients refresh these tokens before expiry through the standard OIDC refresh flow.`

- BAD: `We observed activation collapse in the final layer, resolved by adding LayerNorm before the projection head.`
- GOOD: `Final-layer activations collapsed to a near-constant vector during training (activation collapse). Adding a normalization step (LayerNorm) between the backbone and the projection head restored activation diversity.`

- BAD: `We set dropout=0.1, optimizer=AdamW, lr=3e-4, warmup=2000 steps, cosine decay.`
- GOOD: `We regularize with 10% dropout. Optimization uses AdamW (Adam with decoupled weight decay) at learning rate 3e-4, with a 2000-step linear warmup followed by cosine decay to zero.`

- BAD: `SGD converges faster here because of the Hessian conditioning.`
- GOOD: `SGD converges faster than Adam on this task because the loss surface is well-conditioned — the eigenvalues of the second-derivative matrix (Hessian) do not span many orders of magnitude, so a single learning rate suits all directions.`

- BAD (runbook): `If the queue is backed up, bounce the workers and clear the dead-letter.`
- GOOD (runbook): `If RabbitMQ queue depth exceeds 10k messages for more than 5 minutes, (1) drain and restart the Celery worker pool (bounce the workers) so new brokers pick up the rebalanced connections, then (2) drain the dead-letter queue so failed messages do not replay against the now-fresh workers.`

##### Rationale for AI Agent

大语言模型以接近专家的语体吸收训练语料，并默认复现该语体。当 AI 助手撰写技术内容时，它不知道当前读者是训练分布中的同行，还是初级工程师、跨团队审稿人、外部审计员或基金评审。这种失效模式对作者几乎不可见（作者自己的知识就是基准），但对受众错误的读者却极为刺眼。Pinker 2014 第 3 章深入描述了该现象；实际修正可概括为：想象一位比你自己 expertise 低一级的具体读者，并为其写作。在写任何技术段落之前，具体检验标准是"这句话对还没打开过这个代码库 / 读过这篇论文 / 参加过这场会议的人来说能否落地？" —— 如果不能，重写。

### 语态与直接性

#### RULE-02：当行为主体重要时，不要使用被动语态

- **source**: Orwell 1946, "Politics and the English Language," Rule 3: *"Never use the passive where you can use the active."* Strunk & White §II.14 "Use the active voice."
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞（未验证机械执行）。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: high。反复出现的外部可见 AI 痕迹；被动结构是正式训练分布中生成技术散文的默认语体。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-2 LanguageTool（`PASSIVE_VOICE` 系列）+ Tier-3 智能体自检 + Tier-4 Codex 审阅。不作为 Tier-1 拒绝，因为被动语态正则召回率高、精确率低（会标记大量合理被动；科学归因与真正主体未知的情况仍属合理）。

##### Directive

能用 "Y did X" 表达时，不要写 "X was done by Y"。主动语态点明主体、缩短句子，并让动词承载动作。当主体确实未知或无关紧要时（科学归因、现象观察、普遍真理），被动语态是正确的；要刻意使用，而非默认使用。在每一处被动结构前自问：主体是否已知且值得点明？如果是，改为主动。

##### BAD → GOOD

- BAD: `The experiments were conducted on eight NVIDIA A100 GPUs.`
- GOOD: `We ran the experiments on eight NVIDIA A100 GPUs.`

- BAD: `Errors are logged to /var/log/app.log when the service restarts.`
- GOOD: `The service logs errors to /var/log/app.log on restart.`

- BAD: `A significant improvement in recall was observed after the embedding model was swapped.`
- GOOD: `Swapping the embedding model raised recall@10 by 7 points.`

- BAD (release note): `Memory leaks have been fixed in the worker pool.`
- GOOD (release note): `The worker pool no longer leaks file descriptors on SIGTERM.`

- BAD (postmortem): `The incident was caused by a misconfigured load balancer rule.`
- GOOD (postmortem): ``A misconfigured load balancer rule (typo in the ingress-nginx path-rewrite regex) routed `/auth/*` to the wrong upstream and caused the incident.``

##### Rationale for AI Agent

大语言模型在正式技术散文（摘要、RFC、企业文档）上训练，会过度生成被动结构。训练信号奖励"听起来权威"的语体，而被动结构在该语体中过度出现。实际代价是：被动隐藏主体、推卸责任，并迫使读者重建"谁做了什么"。对于调试类文字（事后复盘、缺陷报告、根因分析），这尤其有害，因为"the error was raised"没点名调用方；"function `parse_token` raised the error at line 47"则能立刻定位缺陷。本规则不禁止被动。科学归因（"participants were recruited"）与真正主体未知的报告（"the service was restarted during the incident, reason unlogged"）可以诚实保留被动。本规则禁止的是主体已知、点明主体能让句子更清晰时的默认被动。

### 用词选择

#### RULE-03：当存在具体、明确的术语时，不要使用抽象或笼统语言

- **source**: Strunk & White §II.16: *"Use definite, specific, concrete language."* Pinker 2014 Ch. 3 将抽象视为知识诅咒的主要传播途径（作者掌握具体信息；读者没有，也无法解析"factors"或"aspects"这类抽象指代）。
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞（未验证机械执行）。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: high。反复出现的清晰度问题；通用名词（`factors`、`aspects`、`considerations`、`issues`、`elements`）是 AI 痕迹，因为模型只给出类别，却没说明类别里有什么。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-2 部分执行（针对 "improved"、"enhanced"、"optimized" 的"有断言无数值"启发式）+ Tier-3 智能体自检 + Tier-4 Codex 审阅作为主要关卡。

##### Directive

能用具体名词时，不要用抽象名词。"The system has performance issues" 等于什么都没说；"the checkout endpoint p95 latency rose from 120ms to 450ms at 14:00 UTC" 才点明了什么、何时、多少。用具体项目替换类别词（"factors"、"aspects"、"considerations"、"issues"、"elements"）。如果你伸手去拿类别词，先问：具体是什么？如果答案需要一个以上的从句才能给出，说明这个句子在隐藏工作量。

##### BAD → GOOD

- BAD: `The model shows improvements across various metrics.`
- GOOD: `The model improves F1 by 3.2 points (0.812 to 0.844) on FEVER and cuts hallucination rate from 11.3% to 6.8% on TruthfulQA.`

- BAD: `Several architectural considerations influenced our design decisions.`
- GOOD: `We chose a two-tower retrieval architecture over cross-encoding because (1) the query-side embedding is cached across sessions, and (2) the document-side index is updated nightly without re-running inference on the query side.`

- BAD: `Ingestion is affected by data quality factors.`
- GOOD: ``When upstream vendors send records with malformed UTF-8, ingestion drops the record and increments the `malformed_input` counter on the `/metrics` endpoint.``

- BAD (API doc): `Authentication handles multiple scenarios.`
- GOOD (API doc): `Authentication supports three flows: OIDC authorization code (first-party web), client_credentials (service-to-service), and refresh-token rotation (long-lived mobile sessions). Each flow returns a signed JWT with a 15-minute TTL.`

- BAD (runbook): `Scale up the backend if traffic is high.`
- GOOD (runbook): ``If p95 latency on `/search` exceeds 300ms for more than 2 minutes, scale the search worker pool from 8 to 16 replicas via `kubectl scale deployment/search-worker --replicas=16`.``

##### Rationale for AI Agent

大语言模型从基金摘要、执行摘要、立场文件等抽象散文中吸收了这种写法，在这些体裁中，具体信息因竞争或修辞原因被隐藏。默认输出携带了这种语体："improvements across metrics"、"multiple factors"、"various considerations"。细心的读者读完这些短语会发现什么都没说，从而贬低文档其余部分。在写任何事实断言句之前，实操检验是：我能指出这句话中每个短语背后的具体数字、文件、提交、用户动作或机制吗？如果不能，这个短语就是填充物，而大语言模型用悦耳的抽象掩盖了实质缺失。Strunk & White §II.16 给出规则；Pinker 2014 第 3 章指出抽象是知识诅咒的主要传播途径之一（作者知道具体信息，所以"factors"对他来说是能解析的指代，但读者没有指代，无法解析）。

#### RULE-04：不要包含多余的词

- **source**: Strunk & White §II.17: *"Omit needless words. Vigorous writing is concise."* Orwell 1946 Rule 3: *"If it is possible to cut a word out, always cut it out."*
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞；填充短语拒绝列表是我们单独的机械执行选择，因为这些短语无需解析即可直接检测。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: high。填充短语是继陈词滥调之后最明显的外部可见 AI 痕迹之一；冗词会向细心的读者立即发出语体偏移信号。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-1 `deny`（填充短语列表见 `enforcement/deny-phrases.txt`："it is important to note that"、"in order to"、"due to the fact that"、"at this point in time"、"may potentially"、"could possibly"、"in the event that"、"it may be necessary to"）+ Tier-2 ProseLint（`terms.denizen_labels`）+ Tier-3 智能体自检。

##### Directive

不要拉长短语。"In order to" 就是 "to"；"due to the fact that" 就是 "because"；"at this point in time" 就是 "now"；"it is important to note that" 就是（删除它，直接陈述事实）；"may potentially" 和 "could possibly" 是冗余的模糊限定（用 "may" 或 "could"，不要两者并用）。每个填充短语都在告诉读者"实质内容马上到"；删掉它，让实质内容直接出现。

##### BAD → GOOD

- BAD: `It is important to note that the learning rate was reduced in order to prevent divergence.`
- GOOD: `We reduced the learning rate to prevent divergence.`

- BAD: `Due to the fact that the data pipeline may potentially fail under high load, we have added retry logic.`
- GOOD: `Because the data pipeline can fail under load, we added retry logic.`

- BAD: `At this point in time, the service is able to process approximately 1000 requests per second.`
- GOOD: `The service processes ~1000 requests per second.`

- BAD (PR description): `This PR makes some minor adjustments in order to fix an issue that was causing failures in certain test cases.`
- GOOD (PR description): ``Fixes a null-pointer crash in `test_checkout_flow` when the cart has a single item.``

- BAD (runbook): `In the event that the database connection pool is exhausted, it may be necessary to restart the service in order to recover.`
- GOOD (runbook): `If the connection pool is exhausted, restart the service.`

- BAD (commit message): `Some small changes have been made that may potentially improve the overall performance of the system in certain scenarios.`
- GOOD (commit message): `Cache product lookups in the hot path; reduces p99 from 310ms to 180ms.`

##### Rationale for AI Agent

大语言模型的训练奖励听起来正式、充满限定的补全，因为它们更接近训练语料中的众数输出（新闻稿、白皮书、学术摘要、企业文档），而非简洁的技术写作。具体填充短语（"in order to"、"due to the fact that"、"it is important to note"、"may potentially"、"could possibly"）是该语体的共识性陈词滥调。它们加长句子却不携带信息。人类读者一扫而过，推断作者没什么可说；下游消费者（搜索引擎、RAG 流水线、摘要链）也会因每 token 信号比被稀释而受损。精确短语拒绝列表可以机械执行（Tier-1），因为这些短语没有合法的技术功能："in order to" 总可被 "to" 替换而不损失含义，因此 outright 拒绝该短语几乎没有误报风险。Strunk & White §II.17 给出原则；Orwell 1946 Rule 3 给出"能删就删"的实操检验。

#### RULE-05：不要使用衰亡隐喻或预制短语

- **source**: Orwell 1946, "Politics and the English Language," Rule 1: *"Never use a metaphor, simile, or other figure of speech which you are used to seeing in print."*
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞；精确短语拒绝列表是我们单独的机械执行选择，因为这些短语可直接检测。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制。
- **severity**: high。生成散文中最外部可见的 AI 痕迹信号。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-1 `deny`（精确短语列表见 `enforcement/deny-phrases.txt`）+ Tier-2 ProseLint（`misc.phrasal_adjectives`、`airlinese.misc`、`cliches.misc`）+ Tier-4 Codex 审阅处理列表遗漏项。

##### Directive

不要使用你在印刷品中经常看到的隐喻、明喻或短语。当某个短语感觉像是现成货架产品 —— 为"一般性的工作"而非"你这项具体工作"准备的框架时 —— 要么用具体数字或具体机制改写成平实技术语言，要么删除该句。如果这句话只是在转述别人对你这类工作的写法，而不是在陈述你这项工作的真实内容，那它就是衰亡隐喻，应被删除。

##### BAD → GOOD

- BAD: `This work pushes the boundaries of what's possible in large language model alignment.`
- GOOD: `This work reduces harmful-completion rate on HarmBench from 14.1% to 3.2% without degrading MMLU accuracy.`

- BAD: `Our system delivers industry-leading performance on the ImageNet benchmark.`
- GOOD: `On ImageNet-1k, our system reaches 88.3% top-1 accuracy, 1.2 points above the previous best (Wang et al. 2025).`

- BAD: `This paves the way for a new era of retrieval-augmented agents.`
- GOOD: （删除该句；如果这项工作真正开创了一种新方法，具体的结果段落已经说明了这一点。）

- BAD: `We leverage state-of-the-art embedding models to unlock the full potential of the retrieval pipeline.`
- GOOD: `We use OpenAI text-embedding-3-large for document embedding. This raised retrieval recall@10 by 7 points over our previous choice (text-embedding-ada-002).`

- BAD: `Our groundbreaking approach to interpretability represents a paradigm shift in the field.`
- GOOD: `Our attention-probing method identifies which transformer layer each factual-recall head first activates. We validate this on 12 known facts from Meng et al. 2022 and observe consistent attribution for 10 of them.`

- BAD (release note): `This release delivers significant improvements to user experience and performance.`
- GOOD (release note): `Reduce p99 dashboard load latency from 820ms to 240ms. Fix a crash in CSV export when a cell contains an embedded newline. Add keyboard shortcut (Shift+E) for the filter-reset action requested in #1847.`

##### Rationale for AI Agent

大语言模型在网页文本 —— 新闻稿、博客、基金引言、论文摘要、企业营销 —— 上训练，会不成比例地复现这些语料中的陈词滥调。读过大量此类来源的读者一见到 "pushes the boundaries"、"paradigm shift" 就会当作填充并跳过整句；AI 写作的独特性会因此成比例下降。Orwell 1946 规则 1 直接命名了这一失效模式，比大语言模型早八十年。Zhang et al. 2026 为将这类规则表述为否定指令提供了实证支持；短语列表拒绝是我们独立的机械执行选择，与 Zhang 论文无关，动机在于观察到这些具体短语无需解析即可直接检测。针对大语言模型的推论 —— 上面六组 BAD/GOOD 示例所说明的 —— 是：如果你不能用具体数字、比较或机制替换这个陈词滥调，那这个陈词滥调就在掩盖实质缺失。删除它之后，如果你发现无法用具体内容替换，这本身就是有用的信息。

#### RULE-06：当存在日常英语词汇时，不要使用可避免的行话

- **source**: Orwell 1946, "Politics and the English Language," Rule 5: *"Never use a foreign phrase, a scientific word, or a jargon word if you can think of an everyday English equivalent."* Pinker 2014 Ch. 2 将具体日常语言视为经典风格的基线；专业术语仅用于承载 distinct 信息时。
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞（未验证机械执行）。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: medium。局部可读性损失；读者仍能理解 "utilize" 和 "methodology"，但把它们当作语体标记而非内容。区分技术行话（必要且承载 distinct 含义）与企业行话（可替换，仅标记语体）。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-1 `ask`（启发式替换："leverage" → "use"、"utilize" → "use"、"methodology" → "method"、"functionality" → "function" 或 "feature"、"operationalize" → "start" 或 "build"）+ Tier-2 ProseLint（`airlinese.misc`）+ Tier-3 智能体自检。

##### Directive

能用 "use" 表达时不要用 "leverage"。能用 "use" 表达时不要用 "utilize"。能用 "method" 表达时不要用 "methodology"。能用 "function" 或 "feature" 表达时不要用 "functionality"。只有当长词携带短词没有的信息时才保留它。有 distinct 含义的技术行话（"backpropagation"、"quantization"、"deserialization"）没问题，且常常必要。企业行话（"leverage"、"utilize"、"operationalize"）可用更短的日常词替换而不损失含义。

##### BAD → GOOD

- BAD: `We leverage transformer architectures to facilitate cross-lingual transfer.`
- GOOD: `We use transformers for cross-lingual transfer.`

- BAD: `The methodology utilized for optimization employs gradient descent techniques.`
- GOOD: `We optimize with gradient descent.`

- BAD: `Functionality for CSV export will be operationalized in the next release.`
- GOOD: `CSV export ships in the next release.`

- BAD (API doc): `This endpoint enables users to interact with the underlying data store through a REST interface.`
- GOOD (API doc): `GET /documents lists documents in the store. Paginated; default 50 per page.`

- BAD (changelog): `The system has been optimized to efficiently utilize available resources in a more performant manner.`
- GOOD (changelog): `Reduce memory footprint from 1.2GB to 380MB at idle by lazy-loading the embedding cache.`

- BAD (proposal): `We will operationalize a novel methodology for the efficient utilization of computational resources.`
- GOOD (proposal): `We will build a scheduler that packs GPU jobs by estimated memory and runtime, aiming for >85% cluster utilization (current baseline: 62%).`

##### Rationale for AI Agent

大语言模型不成比例地复现企业-技术语体，因为它在训练语料中过度出现（白皮书、博客、基金摘要、厂商文档）。像 "leverage"、"utilize"、"operationalize"、"methodology"、"functionality" 这些词并不比 "use"、"use"、"start"、"method"、"feature" 携带更多信息；它们只标记语体。有经验的技术散文读者在阅读时会自动用更短的词替换，这意味着长词什么都没买到，反而花费了阅读时间。本规则并非 outright 禁止多音节术语。有 distinct 含义的技术术语没问题，且必要。本规则禁止的是：较短日常词已承载相同信息，而较长词只增加语体时的替换。

### 断言与校准

#### RULE-07：使用肯定形式表达（肯定词；避免 "X, not Y" 对照）

- **source**: Strunk & White §II.15: *"Put statements in positive form."*
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞；RULE-07 采用肯定指令，因为目标是建设性 placement（选择肯定词）而非标记反模式。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制。
- **severity**: medium。可读性损失而非清晰度失败；读者能正确解析 "not important"，只是比 "trivial" 慢。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-3 智能体自检 + Tier-4 Codex 审阅。没有 Tier-1 deny（需要判断肯定形式是否存在且合适）。空限定短语（"may potentially"、"could possibly"）归 RULE-04，因为它们是冗余限定而非双重否定。

##### Directive

用 "trivial" 替换 "not important"；用 "forgot" 替换 "did not remember"；用 "ignored" 替换 "did not pay attention to"；用 "rarely" 替换 "is not often"；用 "small" 替换 "is not large"；用 "fails" 替换 "does not succeed"。优先用一个肯定词，而非两个否定词。当句子真正在否定某事物时（命题只在否定形式下成立），单个 "not" 没问题且必要。本规则针对的是有单字肯定等价物的两字否定。实操检验：能否用直接命名该状态的单个肯定词替换 "not X"？如果可以，就替换。

同一原则也适用于从句层面。不要为了强调而把断言写成与否定对照物对立："X, not Y"、"It is not X, it is Y"、"Not just X, but Y"、"This is not about X; it is about Y"。直接陈述断言。只有当被拒绝的替代方案具体，且排除它能告知读者新信息时，才保留否定（"The bottleneck is disk I/O, not CPU"）。当替代方案模糊、不言而喻或只是稻草人（"not a hope"、"not the last"、"not just a tool"）时，删除那个尾巴；"not Y" 只是节奏，不是内容。

##### BAD → GOOD

- BAD: `The variance was not large.`
- GOOD: `The variance was small.`

- BAD: `He did not remember to set the flag.`
- GOOD: `He forgot to set the flag.`

- BAD: `This method is not as accurate as the baseline.`
- GOOD: `This method is less accurate than the baseline (81.7% vs 88.3% top-1 on ImageNet-1k).`

- BAD (bug report): `The function does not return a value in some cases.`
- GOOD (bug report): ``The function returns `undefined` when the input array is empty (missing branch in `parse_row` at `utils/parse.py:47`).``

- BAD (release note): `Startup time is not as slow as in the previous release.`
- GOOD (release note): `Startup time drops from 4.2s to 1.8s (57% faster) by deferring the plugin scan to first interactive action.`

- BAD: `The cache is not frequently invalidated.`
- GOOD: `The cache is rarely invalidated, roughly once per deploy.`

- BAD (antithesis, section heading): `Failure Is Committed at the First Token, Not the Last`
- GOOD (antithesis, section heading): `The First Token Commits the Failure`

- BAD (antithesis, proposal): `The signal is our prior art, not a hope.`
- GOOD (antithesis, proposal): `Our prior art is the signal: three shipped systems and two prior awards on this exact problem.`

- BAD (antithesis, release note): `This is not just a bug fix, it is a full rewrite of the export pipeline.`
- GOOD (antithesis, release note): `This release rewrites the CSV export pipeline; the previous version only patched the newline crash.`

##### Rationale for AI Agent

双重否定措辞（"not insignificant"、"not uncommon"、"not unlike"）弥漫于学术和新闻散文，大语言模型从训练中吸收了这个模式。认知成本真实存在：读者在工作记忆中保留 "not"，解析被否定的形容词，再否定一次才能恢复 intended 含义。对于简单肯定状态，这是浪费工作。本规则不禁止诚实的否定；当某事物确实缺失时，"no X" 或 "not X" 是正确的。本规则禁止的是：已有肯定形式词能命名该状态时，可避免的复合否定。

AI 生成散文还有一个下游顾虑：双重否定也会击败下游工具中的语气与情感检测，因此在文本会喂给另一个模型（摘要、分类、审核）的语境中，肯定形式在操作上更安全。

本规则的从句层面针对的是对照（"X, not Y"、"not just X, but Y"、"it is not X, it is Y"），这是大语言模型训练的说理与散文语料中回报很高的模式（评论、宣言、营销文案）。它读起来平衡且可引用，因此模型会在标题、摘要和开篇中使用。这种结构先发明一个替代方案再否定它；当该替代方案模糊或是稻草人时，"not Y" 尾巴只增加节奏不增加信息，细心读者会把它当作 AI 语体而贬低。修复方式与词汇层面相同：直接陈述肯定断言，只在排除具体替代方案能告诉读者新信息时才保留对比。

#### RULE-08：不要在证据基础上过度或不足地陈述断言

- **source**: Pinker 2014 Ch. 6（校准断言；限定语校准被视为一种技能，动词需与证据强度匹配）。Gopen & Swan 1990（科学归因：断言来源应在句中可见，动词应匹配证据）。
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞（未验证机械执行）。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: high。外部可见的 AI 痕迹；过度断言模式（"revolutionary"、"transforms"、"dramatic"）与反射性模糊限定（"it might be worth considering"）都会被技术读者识别为填充语体，只是以不同方式侵蚀信任。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-3 智能体自检 + Tier-4 Codex 审阅作为主要关卡。不作为 Tier-1，因为校准需要判断证据实际支持什么。

##### Directive

不要过度断言（证据是"suggests X"时却说"proves X"）。也不要通过反射性模糊限定来不足断言（意思是"we should do X"时却说"it might be worth considering"）。用动词匹配证据：实验结果用 "suggest" 或 "show"；理论推导用 "imply" 或 "prove"；用户报告用 "indicate"（待验证）；基准测试用 "measure"。只有与最强替代方案比较过才能用 "best"；只有排除过替代方案才能用 "only"。证据不确定时，用一个从句说明；不要把主句动词弱化到证据不支持的程度。

##### BAD → GOOD

- BAD: `Our method revolutionizes language model alignment.`
- GOOD: `Our method reduces harmful-completion rate on HarmBench from 14.1% to 3.2% without degrading MMLU accuracy. (Generalization to other alignment benchmarks is future work.)`

- BAD: `Dramatic improvement in inference speed was observed.`
- GOOD: `Inference latency at batch size 1 drops from 142ms to 118ms (17% faster) on A100. Batch size 32 and larger show no measurable speedup.`

- BAD: `It might be worth considering whether some form of input validation could be beneficial.`
- GOOD: ``Add input validation at `/users`: the endpoint crashes on non-UTF-8 query parameters (observed twice last week).``

- BAD (paper abstract): `Our model proves the superiority of attention-based retrieval over sparse methods.`
- GOOD (paper abstract): `Our attention-based retriever reaches MRR@10 = 0.412 on MS MARCO Dev, compared to 0.395 for BM25 and 0.398 for ColBERT. The improvement is within one standard deviation on out-of-domain queries (BEIR).`

- BAD (issue report): `Everything is broken; nothing works.`
- GOOD (issue report): ``/auth/login returns 500 for all requests after the 2026-04-18 deploy. /auth/logout and /auth/refresh unaffected. Logs show a KeyError on `iat` in token parsing.``

- BAD (grant proposal): `This research will transform our understanding of neural network interpretability.`
- GOOD (grant proposal): `This research tests whether attention-probing generalizes beyond the 12 factual-recall circuits reported in Meng et al. 2022. If yes, the method applies to a class of interpretability questions currently intractable; if no, we localize the method's scope.`

##### Rationale for AI Agent

大语言模型在混合语体语料（研究摘要、新闻稿、基金引言、营销文案）上训练，同时吸收了过度断言和反射性限定的体裁模式。每种都会可预测地失败：过度断言触发读者的校准警报（技术读者会在摘要中扫描无根据的 "proves" 或 "best"，并据此贬低整篇论文）；反射性不足断言把显然为真的主张膨胀得听起来很重要；过度限定则把谨慎拖延到两个从句的形式化缓冲中。在写任何结果句之前，实操检验是：(a) 什么证据支持它，(b) 动词是否匹配？"We observed" 弱于 "we showed"，"we showed" 又弱于 "we proved"。精确选择与你证据匹配的动词。Pinker 2014 第 6 章给出校准词汇；Gopen & Swan 1990 将科学归因框定为结构性写作问题（断言来源应可见，动词应匹配证据）。

### 句子结构

#### RULE-09：用相似形式表达并列观点（平行结构）

- **source**: Strunk & White §II.19: *"Express coordinate ideas in similar form."*
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞；RULE-09 采用肯定指令，因为平行结构是建设性 placement（跨项目保持形式一致）而非反模式标记。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制。
- **severity**: medium。局部可读性损失；读者会重新解析不匹配项并失去节奏，但仍能恢复含义。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-2 部分执行（列表项词性检查）+ Tier-3 智能体自检 + Tier-4 Codex 审阅。

##### Directive

用相同语法形式表达并列观点。三个项目的列表中，如果第 1 项是名词短语，第 2、3 项也应是名词短语；如果第 1 项是动词开头的小句，第 2、3 项也应是动词开头的小句。本规则适用于项目符号列表、平行谓语（"we measure X, improve Y, and validate Z"）以及由 "and" / "or" / "but" 连接的并列句。形式不匹配会迫使读者针对新的预期结构重新解析每一项。

##### BAD → GOOD

- BAD: `The pipeline cleans the data, feature extraction, and then trains the model.`
- GOOD: `The pipeline cleans the data, extracts features, and trains the model.`

- BAD: `We benchmark against three baselines: BM25, a sparse lexical retriever; dense retrieval using DPR; ColBERT.`
- GOOD: `We benchmark against three baselines: BM25 (sparse lexical), DPR (single-vector dense), and ColBERT (multi-vector dense).`

- BAD (API doc): `The endpoint accepts JSON input, you get XML back, and pagination is via cursor.`
- GOOD (API doc): `The endpoint accepts JSON input, returns XML output, and paginates by cursor.`

- BAD (runbook checklist item, in a list of verb-initial items): `Memory usage`
- GOOD (runbook checklist item, matching surrounding items): `Check memory (`free -h`)`

- BAD (changelog entry, in a list of verb-initial entries): `Faster startup`
- GOOD (changelog entry, matching surrounding entries): `Reduce startup time from 4.2s to 1.8s.`

##### Rationale for AI Agent

大语言模型常产出这样的列表：前一两项确立了结构，后续项目却漂移，因为模型按主题而非已确立的结构条件采样下一项。漂移很微妙：读者扫过第 1 项，对第 2、3 项形成预期形状，然后撞上不匹配并回退。简单情况可机械检查（第 1 项以动词 X 开头的列表，第 2、3 项应以相同时态的动词开头；名词短语列表应保持名词短语），但一般情况需要解析。针对 AI 生成的实际补救：生成列表时，先确定结构（全动词短语？全名词短语？主谓宾？），然后按该结构逐项生成，而不是自由采样。Strunk & White §II.19 给出规则和诊断法：用 "that" 连接各项读一遍；如果任何一项读不通，平行结构就被破坏了。

#### RULE-10：保持相关词语彼此靠近

- **source**: Strunk & White §II.20: *"Keep related words together."* Gopen & Swan 1990 将动词-主语距离视为科学散文中特殊的结构性可读性问题（长主语-动词间隔是科学写作不可读的最常见原因之一）。
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞；RULE-10 采用肯定指令，因为目标是建设性 placement（让 X 靠近 Y）而非反模式标记。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制。
- **severity**: medium。局部可读性损失；长主语-动词间隔会导致读者工作记忆溢出并回退，但含义仍可费力恢复。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-2 部分执行（主语与动词之间的依存解析距离）+ Tier-3 智能体自检 + Tier-4 Codex 审阅。

##### Directive

主语靠近动词，动词靠近宾语，修饰语靠近被修饰语。当长插入语或关系从句必须出现在主语和动词之间时，把从句移到句末或拆成两句。实操检验：数主语和动词之间的词数；如果间隔超过 8 个词，就拆分。读者会在工作记忆中保留主语直到动词出现；每个插入从句都占用记忆槽并增加误解析风险。

##### BAD → GOOD

- BAD: `The model, which was pre-trained on a mixed corpus of English Wikipedia, Common Crawl, and a 400-million-token curated scientific dataset assembled by the authors over eight months, achieves 87.2% accuracy.`
- GOOD: `The model achieves 87.2% accuracy. It was pre-trained on a mixed corpus of English Wikipedia, Common Crawl, and a 400-million-token scientific dataset the authors curated over eight months.`

- BAD: `Users of the legacy authentication flow, which is being deprecated in Q3 2026 in favor of the new OIDC-based system described in the migration guide, must update their client libraries before the end-of-life date.`
- GOOD: `Users of the legacy authentication flow must update their client libraries before end-of-life. The legacy flow is being deprecated in Q3 2026; the replacement is OIDC-based (see migration guide).`

- BAD (API doc): `The /users endpoint returns, subject to the rate-limit and access-control constraints described below, a paginated list of user objects.`
- GOOD (API doc): `The /users endpoint returns a paginated list of user objects. Rate limits and access controls apply (see below).`

- BAD (postmortem): `The database replica, which had been failing its health checks intermittently for three days before the outage but was never promoted to primary during that period because of a misconfigured priority setting, was the direct cause of the outage.`
- GOOD (postmortem): `The database replica was the direct cause of the outage. It had been failing health checks intermittently for three days; a misconfigured priority setting prevented promotion to primary during that period.`

- BAD: `We found that the retrieval recall of our system, compared against the previously strongest baseline across all five evaluation datasets and using the same pre-processing pipeline, improved by 7 points at k=10.`
- GOOD: `Retrieval recall@10 improved by 7 points over the previously strongest baseline. The comparison used the same pre-processing pipeline across all five evaluation datasets.`

##### Rationale for AI Agent

大语言模型基于前文条件逐 token 生成文本，这鼓励完整性（每个限定都内联加入）而非可读性（限定推迟到主句落地之后）。结果是：主语和动词之间被 20+ 词的插入限定隔开。读者体验为工作记忆溢出：等动词出现时，读者已经忘了主语，必须回退。同样逻辑适用于动词-宾语和修饰语-被修饰语。Gopen & Swan 1990 将长主语-动词间隔框定为科学散文不可读的最常见原因之一；Strunk & White §II.20 给出一般形式的原则。针对 AI 生成的具体补救是拆分句子：主句在前落地，支撑限定随后跟一句。

#### RULE-11：把新信息或重要信息放在句末的强调位置

- **source**: Gopen & Swan 1990, "The Science of Scientific Writing"（强调位置框架；对读者期望新信息落在句末的实证处理）。
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞；RULE-11 采用肯定指令，因为强调位置 placement 是建设性结构规则而非反模式标记。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制。
- **severity**: medium。局部可读性损失；读者能从前置句中恢复断言，但代价是重读，而速读者会把句末标点前的话当作 takeaway，因此强调位置误用会稀释句子冲击力。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-3 智能体自检 + Tier-4 Codex 审阅。不作为 Tier-1，因为识别句中"关键事实"需要判断。

##### Directive

把你希望读者记住的信息放在句末。句首（主题位置）承接前文；句末（强调位置）是新信息或重要信息落地时最具强调力的位置。如果关键事实在句中，就把它移到句末或重新平衡。本规则尤其适用于论文中的结果句、设计文档的结论、事后复盘中的根因句。

##### BAD → GOOD

- BAD: `A 3.2-point improvement in F1 over the previous best model was demonstrated by the new architecture on the SQuAD 2.0 test set.`
- GOOD: `On the SQuAD 2.0 test set, the new architecture improves F1 by 3.2 points over the previous best model.`

- BAD: `The outage was caused by a cron job that ran at the wrong time.`
- GOOD: ``The outage was caused by a cron job firing every minute instead of every hour (typo in the crontab: `* * * * *` instead of `0 * * * *`).``

- BAD (commit message): `Fix for issue where users occasionally see a blank page in the dashboard when their session has expired and they try to navigate to a protected route.`
- GOOD (commit message): `On expired-session navigation to protected routes, redirect to /login instead of rendering the blank dashboard frame.`

- BAD (release note): `Performance improvements in the search pipeline are included in this release, with p95 query latency improving from 340ms to 95ms and p99 from 870ms to 180ms.`
- GOOD (release note): `p95 search latency drops from 340ms to 95ms; p99 drops from 870ms to 180ms.`

- BAD (paper sentence): `The approach is to first train a contrastive embedder, and then the retrieval performance can be measured across the five benchmarks.`
- GOOD (paper sentence): `We first train a contrastive embedder, then measure retrieval performance across five benchmarks: MS MARCO, FEVER, HotpotQA, NQ, and TriviaQA.`

##### Rationale for AI Agent

Gopen & Swan 1990 通过实证研究（American Scientist 对句子清晰度的研究）表明，读者会无意识地期望新信息落在强调位置。当句子把新信息前置、末尾淡入背景时，读者会觉得句子平淡并回退以恢复断言。大语言模型常产出 BAD 模式，因为逐 token 生成奖励用最流畅的内容完成句子，而末尾通常是已经建立的话题性介词短语，而非引入新信息。实际改写：先确定句子的关键断言，然后重构句子让断言落在末尾。对于多句单元（段落），同一逻辑适用于段落层面：首句框定；末句落地要点；中句支撑。

#### RULE-12：拆分长句；变化长度（将超过 30 词的句子拆分）

- **source**: Strunk & White §II.18（句子排列；段落内长度变化）。Pinker 2014 Ch. 4（句法与工作记忆限制；带嵌套从句的长句消耗读者的解析预算）。
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞；RULE-12 采用肯定指令，因为拆分句子和变化长度是建设性结构选择而非反模式标记。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制。
- **severity**: high。长句是反复出现的 AI 痕迹和清晰度失败；时间受限的技术读者（值班工程师、审稿人、发布说明速读者）无法可靠解析 40+ 词的句子。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-1 `ask`（句子 > 30 词时建议拆分）+ Tier-2 句子长度方差指标 + Tier-3 智能体自检。

##### Directive

将超过 30 词的句子拆成两句或更多。在段落内变化句子长度：五个 25 词句子的段落，不如 8、18、22、14、30 词_sentence 分布的同样内容读起来好。短句落地观点；长句承载限定和细节。只使用其中一种的段落会显得单调。当长句不可避免（单个逻辑单元无法拆分）时，让前后句保持简短以平衡。

##### BAD → GOOD

- BAD (43 words, single sentence): `We evaluate our model on five standard benchmarks covering natural-language inference, reading comprehension, and factual-recall tasks, reporting both in-distribution accuracy on held-out splits of the training corpora and out-of-distribution accuracy on benchmarks not seen during training or fine-tuning.`
- GOOD (three sentences, 15 + 12 + 11 words): `We evaluate our model on five standard benchmarks: NLI, reading comprehension, and factual-recall. In-distribution accuracy uses held-out splits of the training corpora. Out-of-distribution accuracy uses benchmarks not seen during training.`

- BAD (monotone paragraph, four 22-word sentences): `The ingestion pipeline processes incoming records in batches of one thousand items and stores them in the primary document store. Each batch is processed by the ingest worker which runs on a schedule of every five minutes. The document store maintains an index on the timestamp field which enables range queries. Query performance is acceptable for batch sizes up to fifty thousand records per minute.`
- GOOD (varied, 8 + 22 + 14 + 11 words): `The ingest worker handles incoming records in batches. Every five minutes, it pulls up to a thousand records and writes them to the primary document store. The store keeps a timestamp index that supports range queries. At fifty thousand records per minute, performance holds.`

- BAD (runbook, 34 words): `If the primary database instance becomes unavailable for more than two minutes due to either a network partition or a full restart cycle, initiate failover to the replica using the promote_replica.sh script in the ops directory.`
- GOOD (split): ``Fail over to the replica if the primary is unavailable for more than two minutes. Unavailability includes both network partition and full restart cycle. Run `ops/promote_replica.sh` to promote.``

- BAD (paper abstract, 54 words): `In this work we investigate whether large language models pre-trained on code exhibit emergent understanding of algorithmic concepts, testing this hypothesis by measuring zero-shot performance on a suite of algorithm-design tasks and comparing the pattern of successes and failures to human performance on the same tasks collected from online programming forums over a period of six months.`
- GOOD (four sentences): `Do code-pretrained LLMs exhibit emergent understanding of algorithmic concepts? We test this by measuring zero-shot performance on a suite of algorithm-design tasks. We compare performance to human baselines collected from online programming forums over six months. We report the pattern of shared successes and failures across model size and task difficulty.`

- BAD (changelog, monotone): `This release adds support for OAuth 2.0 device flow authentication. This release also adds a new audit log for all API requests. This release introduces rate limiting on the free tier at 100 requests per minute. This release fixes a crash in CSV export when a cell contains an embedded newline.`
- GOOD (varied): `OAuth 2.0 device flow authentication ships in this release. A new audit log now captures all API requests. Free-tier clients see rate limiting at 100 req/min. CSV export no longer crashes on cells containing embedded newlines.`

##### Rationale for AI Agent

大语言模型解码奖励结构良好的补全；下一 token 目标鼓励句子继续添加限定，而不是停下来重新开始。结果是趋向 30+ 词、带多个从属从句的句子。读者，尤其是时间受限的技术散文读者，按块阅读；超过工作记忆容量的块会导致理解失败和重读。短句还能承载长句稀释的强调；一个句子长度从不变化的段落读起来像平面，读者会扫过那些本应落地的要点。针对 AI 生成的操作指南：起草后，统计每个技术散文段落中每句的词数；超过 30 词就拆分；在段落内变化长度（不要连续五个长度相近的句子）。Pinker 2014 第 4 章框定了句法/工作记忆权衡；Strunk & White §II.18 给出变化原则。

## 9 条来自现场观察的规则

以下九条规则（RULE-A 至 RULE-I）来自我对 2022 至 2026 年间数十个写作项目和代码发布中大语言模型输出的观察。它们并非引自写作权威著作；每条规则都命名了我在不同项目中频繁观察到、值得单独成文的反复模式。它们在所有适配文件中被视为 12 条核心规则的同级输入；当智能体消费该规则集时，两组均具有约束力。

### 观察到的大语言模型模式

#### RULE-A：除非内容是真列表，否则不要把散文转成项目符号

- **source**: 我对 2022–2026 年间数十个写作项目和代码发布中大语言模型输出的观察。邻近 `agent-config` / `anywhere-agents` AGENTS.md 格式默认："Do not convert paragraphs into bullet points unless the user asks for that format."
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞（未验证机械执行）。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: medium。反复出现的结构性 AI 痕迹；项目符号化会碎片化推理，并在提案、设计文档和研究论文引言中发出"AI 摘要"语体信号。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-2 启发式（标记超过 4 项且开头模式相同的连续列表，或若将项目用主谓流连接成散文则标记）+ Tier-3 智能体自检 + Tier-4 Codex 审阅。

##### Directive

当观点通过因果、论证或叙事连接时，保留为段落。仅当项目是真正平行的枚举（API 端点、配置选项、检查清单步骤）时才使用项目符号。检验标准：如果读者只读每个项目的开头几个词，能否恢复含义？对于真列表，可以（每个项目命名一个事物）；对于碎片化散文，不行（项目是剥离了连接组织的句子碎片）。不要强行凑出 3 项列表，当 2 项或一句话更合适时；大语言模型会过度生产 "first, second, third" 三元组，而自然表达其实只需 2 项。抵制这种模式。

##### BAD → GOOD

- BAD (proposal, bullet-ified argument):

    ```text
    Our approach consists of:
    - Training a contrastive embedder
    - Because this improves retrieval recall
    - Which is important for RAG pipelines
    - And enables downstream applications
    ```

- GOOD (proposal): `Our approach trains a contrastive embedder, which improves retrieval recall for downstream RAG pipelines.`

- BAD (design doc, bullet-ified causal chain):

    ```text
    The architecture decision:
    - We chose two-tower retrieval
    - Rather than cross-encoding
    - Because query embeddings cache across sessions
    - And document index updates nightly without re-inference
    ```

- GOOD (design doc): `We chose two-tower retrieval over cross-encoding because the query embedding caches across sessions, and the document index updates nightly without re-running inference on the query side.`

- BAD (API doc, fragmented single sentence):

    ```text
    Rate limits:
    - Free tier
    - 100 requests
    - Per minute
    - Per user
    ```

- GOOD (API doc): `Rate limits: the free tier allows 100 requests per minute per user.`

- BAD (postmortem, forced 3-item triad):

    ```text
    The outage had three causes:
    - A misconfigured load balancer rule
    - An outdated auth-v1 service
    - And insufficient alerting on auth-v1
    ```

- GOOD (postmortem): `A misconfigured load balancer rule routed /auth/* traffic to the outdated auth-v1 service. Insufficient alerting on auth-v1 delayed detection by 37 minutes.`

- BAD (README, forced "three strengths" triad):

    ```text
    Our framework has three key strengths:
    - It is fast
    - It is accurate
    - It is easy to use
    ```

- GOOD (README): `Our framework is fast (~2ms per query), accurate (94.3% top-1 on the benchmark suite), and ships as a drop-in Python library.`

##### Rationale for AI Agent

大语言模型在呈现多个想法时默认使用项目符号，因为项目符号看起来结构化，并发出"我正在组织"的信号。但项目符号会碎片化推理：每个项目变成孤立的碎片，连接组织（because、therefore、however）消失，读者必须从碎片中重建论证。特定的 3 项三元组尤其常见；大语言模型学到 "first, second, third" 结构感觉平衡完整，因此即使底层内容只有 2 项或一句流畅的话，也会强行生产三元组。修正：仅当项目是真正独立的枚举时使用项目符号；当观点相互连接时使用散文。起草任何列表后的检验句：这个列表能否无损地变成散文？如果可以，它很可能应该变成散文。

#### RULE-B：不要把 em dash 或 en dash 当作随意的句子标点

- **source**: 我对 2022–2026 年间数十个写作项目和代码发布中大语言模型输出的观察。邻近 `agent-config` / `anywhere-agents` AGENTS.md 格式默认："Avoid heavy dash use. Do not use em dashes or en dashes as casual sentence punctuation. Prefer commas, semicolons, colons, or parentheses instead."
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞；破折号作为标点的正则标记是我们单独的机械执行选择（Zhang 未验证机械执行）。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: medium。反复出现且外部可见的 AI 痕迹；大语言模型使用 em dash 的频率显著高于优秀人类技术写作者，产生人类读者能识别为 AI 节奏的韵律。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-1 `ask`（em dash 与 en dash 正则，排除范围和成对名称）+ Tier-3 智能体自检 + Tier-4 Codex 审阅。

##### Directive

不要把 em dash 或 en dash 当作随意的句子标点。同位语用逗号，连接独立从句用分号，展开说明用冒号，插入语用括号。en dash 在数字范围（`1-3`、`2020-2026`）、成对名称（"the Stein-Strömberg theorem"）和书目页码范围中仍然正确。复合词和技术术语中的普通连字符（`command-line`、`co-PI`、`zero-shot`）不是 dash，不应被标记。

##### BAD → GOOD

- BAD: `The model converges quickly — typically within 5000 training steps — on most datasets.`
- GOOD: `The model converges quickly, typically within 5000 training steps, on most datasets.`

- BAD: `We use three optimizers — AdamW, Lion, and SGD — in the ablation.`
- GOOD: `We use three optimizers in the ablation: AdamW, Lion, and SGD.`

- BAD (release note): `This release fixes the CSV export crash — the one reported last week — and adds a filter-reset shortcut.`
- GOOD (release note): `This release fixes the CSV export crash reported in issue #1847 and adds a filter-reset shortcut.`

- BAD (paper): `The method works well on in-distribution data — our primary evaluation target — and degrades gracefully on out-of-distribution inputs.`
- GOOD (paper): `The method works well on in-distribution data (our primary evaluation target) and degrades gracefully on out-of-distribution inputs.`

- BAD (blog post): `This is important — and somewhat surprising — because earlier work suggested the opposite.`
- GOOD (blog post): `This is important, and somewhat surprising, because earlier work suggested the opposite.`

##### Rationale for AI Agent

大语言模型从长篇新闻和散文语体（杂志散文和重散文博客的语体）中吸收了 em dash 作为偏好的连接符，在那里它承载节奏和强调。在密集技术散文中，每个 em dash 都是读者必须在插入语完成前保持在工作记忆中的停顿；一句两个 em dash 就接近多数读者的工作记忆上限。最近公众意识到 em dash 过度使用是 AI 痕迹，部分原因是大语言模型使用 em dash 的频率是优秀人类技术写作者的几倍，产生人类读者能识别为 AI 节奏的韵律。逗号、分号、冒号和括号各携带更清晰的语义信号（列表分隔、独立从句断开、展开、插入语）；用实际匹配关系的标点替换 em dash，能让句子的逻辑结构显式化，而非依赖节奏。复合词和技术术语中的普通连字符仍然正确；本规则针对的是充当标点的 dash，而非连接单词的 hyphen。

#### RULE-C：不要连续用相同单词或短语开头

- **source**: 我对 2022–2026 年间数十个写作项目和代码发布中大语言模型输出的观察。邻近 `agent-config` / `anywhere-agents` AGENTS.md 格式默认："Prefer not to start several consecutive sentences with the same word or phrase."
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞（未验证机械执行）。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: medium。局部韵律问题；相同开头累积时，段落读起来单调且像模板填充。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-2（段落内连续句子的首词检查；标记两个或以上连续相同开头）+ Tier-3 智能体自检 + Tier-4 Codex 审阅。

##### Directive

不要用同一个词连续开头两个或更多句子。这种模式标志着生成过程锁定了一个起草模板（常见模式是 `This ... This ... This ...`、`The ... The ... The ...` 或 `We ... We ... We ...`）。变化开头方式：话题前置、主语前置、连接词前置。代词主语（`It`、`We`、`They`）是大语言模型输出中最常见的违规者，因为模型按主题条件采样下一句时会重新选择最流畅的主语。

##### BAD → GOOD

- BAD (paper): `The method uses a contrastive loss. The method also applies dropout. The method converges in 5000 steps.`
- GOOD (paper): `The method uses a contrastive loss with 10% dropout, converging in 5000 steps.`

- BAD (release note): `This release adds OAuth support. This release fixes a CSV export bug. This release improves startup time.`
- GOOD (release note): `OAuth support lands in this release. A CSV export bug is fixed. Startup time drops from 4.2s to 1.8s.`

- BAD (paper, we-starts): `We trained the model. We evaluated on five benchmarks. We found improvements across all metrics.`
- GOOD (paper): `We trained the model and evaluated it on five benchmarks, finding improvements across all metrics.`

- BAD (API doc): `The API returns JSON. The API supports pagination. The API rate-limits at 100 req/min.`
- GOOD (API doc): `The API returns paginated JSON and rate-limits at 100 req/min.`

- BAD (postmortem, it-starts): `It started at 14:00 UTC. It lasted 37 minutes. It affected 12% of users.`
- GOOD (postmortem): `The incident started at 14:00 UTC, lasted 37 minutes, and affected 12% of users.`

##### Rationale for AI Agent

大语言模型逐 token 生成文本时，常会锁定一个成功的开头并重复它。一旦 "The method ..." 有效，下一句的开头分布往往又选中 "The method ..."，因为给定主题后该前缀条件概率变高。结果是：段落里三四句开头完全相同。人类读者读起来会觉得这是模板填充而非论证；即使内容正确，形式也发出机器模式信号。生成时的修正：写完一句后，下一句的开头应变化，要么把新信息移到主语位置，要么合并两句，要么使用连接词。本规则与 RULE-12（句子长度变化）相互作用；两者都针对段落层面的韵律。

#### RULE-D：不要过度使用过渡词（"Additionally"、"Furthermore"、"Moreover"）

- **source**: 我对 2022–2026 年间数十个写作项目和代码发布中大语言模型输出的观察。邻近 `agent-config` / `anywhere-agents` AGENTS.md 格式默认："Avoid overusing transition words like 'Additionally' or 'Furthermore.'"
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞（未验证机械执行）。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: medium。反复出现的外部可见 AI 痕迹；连续两句或三句以 "Additionally" / "Furthermore" / "Moreover" 开头，是识别 AI 生成文本最鲜明的节奏特征之一。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-1 `ask`（句首过渡词列表："Additionally"、"Furthermore"、"Moreover"、"In addition"、"What's more"、"Notably"；结合段落级频率标记）+ Tier-2 ProseLint + Tier-3 智能体自检。

##### Directive

除非下一句确实以前面从句为基础、且句号或 `And` 无法表达这种关系，否则不要用 "Additionally"、"Furthermore"、"Moreover"、"In addition"、"What's more" 或 "Notably" 开头。大多数情况下，前一句用句号结束，下一句靠内容本身建立连接。仅在逻辑推进（补充、对比、让步）需要向读者显式标记的罕见情况下，才保留显式过渡。

##### BAD → GOOD

- BAD (paper): `The model outperforms BM25 on MS MARCO. Additionally, it outperforms DPR on Natural Questions. Furthermore, it reaches state-of-the-art on BEIR.`
- GOOD (paper): `The model outperforms BM25 on MS MARCO and DPR on Natural Questions, and reaches state-of-the-art on BEIR.`

- BAD (proposal): `The project addresses retrieval accuracy. Moreover, it addresses latency. In addition, it addresses interpretability.`
- GOOD (proposal): `The project addresses three targets: retrieval accuracy, latency, and interpretability.`

- BAD (design doc): `We cache embeddings for 24 hours. Additionally, we invalidate on source-document update. Furthermore, we rebuild the cache nightly.`
- GOOD (design doc): `We cache embeddings for 24 hours, invalidate on source-document update, and rebuild the cache nightly.`

- BAD (release note): `This release adds OAuth support. Additionally, it fixes the CSV export crash. Furthermore, it improves startup time.`
- GOOD (release note): `OAuth support lands in this release. The CSV export crash is fixed. Startup time drops from 4.2s to 1.8s.`

- BAD (blog): `The method is simple. Additionally, it is fast. Furthermore, it generalizes.`
- GOOD (blog): `The method is simple, fast, and generalizes to new domains.`

##### Rationale for AI Agent

大语言模型在正式散文语料（学术散文、维基百科、社论写作）上训练，显式过渡词过度出现。"Additionally"、"Furthermore"、"Moreover" 在大语言模型输出中的频率高于优秀技术散文，产生 AI 生成文本被识别的独特句首节奏。修正：连接组织通常应隐含（下一句明显是补充，因为其内容已说明）而非显式标记。当逻辑推进不明显，或段落级对比需要向读者显式标记时，显式过渡仍然合理。相关：RULE-04 处理词汇级填充短语（"in order to"、"due to the fact that"）；RULE-D 处理 RULE-04 短语列表未针对的特定句首过渡模式。两条规则都在删减多余词；它们针对句子中的不同位置。

#### RULE-E：不要每段都以总结句收尾

- **source**: 我对 2022–2026 年间数十个写作项目和代码发布中大语言模型输出的观察。邻近 `agent-config` / `anywhere-agents` AGENTS.md 写作默认："Not every paragraph needs a tidy summary sentence at the end."
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞（未验证机械执行）。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: medium。结构性废话；增加长度却不增加信息。该模式外部可见，因为博览技术文献的读者会一扫而过，并将其标记为机器生成或未编辑。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-3 智能体自检（段落级判断）+ Tier-4 Codex 审阅。

##### Directive

不要以重述段落要点的句子结束每个段落（"In summary, ..."、"Thus, the contribution is ..."、"Overall, this means ..."、"In conclusion, ..."）。总结收尾适用于全文最后一段，或读者会速读而非顺序阅读的冗长章节。对于正文段落，相信内容自己能落地要点；用不同措辞重述同一主张的收尾句是噪音。检验标准：如果删除收尾句，段落是否仍能表达要点？如果可以，删除收尾句。

##### BAD → GOOD

- BAD: `We trained the model on 50k query-passage pairs and evaluated on five benchmarks. The model reaches 0.79 recall@10 on our held-out set. Overall, these results demonstrate that our method is effective.`
- GOOD: `We trained the model on 50k query-passage pairs and evaluated on five benchmarks. The model reaches 0.79 recall@10 on our held-out set.`

- BAD (design doc): `We chose two-tower retrieval because query embeddings cache across sessions. Thus, the architecture is well-suited to our caching strategy.`
- GOOD (design doc): `We chose two-tower retrieval because query embeddings cache across sessions.`

- BAD (proposal): `The proposed work advances retrieval-augmented generation for medical question answering. In summary, the project combines several research directions into a unified framework.`
- GOOD (proposal): `The proposed work advances retrieval-augmented generation for medical question answering.`

- BAD (blog): `The bug was a single-character typo in the crontab (five asterisks instead of "0 hour"). In conclusion, this small typo caused a large outage.`
- GOOD (blog): `The bug was a single-character typo in the crontab: five asterisks instead of the intended hourly schedule.`

- BAD (paper): `Our method reaches 88.3% top-1 on ImageNet-1k, 1.2 points above Wang et al. 2025. Overall, our approach sets a new benchmark on ImageNet.`
- GOOD (paper): `Our method reaches 88.3% top-1 on ImageNet-1k, 1.2 points above Wang et al. 2025.`

##### Rationale for AI Agent

大语言模型常添加段落结尾总结，因为学术和说明语料中显著包含"主题句 + 主体 + 总结句"结构。收尾句发出"我正在结束这个思路"的信号，但不增加新信息。速读的技术读者反正会跳过收尾（他们读主题句和第一个具体主张）；细心读者会觉得这种冗余是填充。相关：RULE-04 处理词汇级填充短语；RULE-E 处理 RULE-04 词汇拒绝列表无法触及的段落级填充模式。两条规则都在删减多余内容；它们作用于不同结构层级（词 vs 段落）。

#### RULE-F：使用一致术语；不要在文档中途重新定义缩写

- **source**: 我对 2022–2026 年间数十个写作项目和代码发布中大语言模型输出的观察。邻近 `agent-config` / `anywhere-agents` AGENTS.md 写作默认："Use consistent terms. If an abbreviation is defined once, do not define it again later."
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞（未验证机械执行）。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: medium。长文档中反复出现的清晰度问题；术语变化会迫使读者检查每个新词是指同一概念还是新概念。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-2（跨文档首次使用缩写追踪；标记后续再次展开，以及无原因用释义替换已定义缩写时的同义词漂移）+ Tier-3 智能体自检 + Tier-4 Codex 审阅。

##### Directive

一旦引入某个术语或缩写，就持续使用它。不要交替使用 "large language model"、"LLM"、"language model"、"LM"、"neural language model"、"foundation model" 作为同一事物的同义词。不要重新定义缩写：如果引言中 "LLM" 被定义为 "large language model"，第 3 节不要再展开它。对读者而言，一致的术语发出"这是我前面见过的同一概念"的信号；变化的术语发出"我应该检查这是否是新东西"的信号。

##### BAD → GOOD

- BAD (paper, term drift): 第 1 节引入 "large language models (LLMs)"，第 3 节写成："Neural language models achieve..."
- GOOD (paper): 第 1 节引入 "large language models (LLMs)"，第 3 节写成："LLMs achieve..."

- BAD (doc, expansion re-emerges): "We use retrieval-augmented generation (RAG). ... / later / Retrieval-augmented-generation architectures..."
- GOOD (doc): "We use retrieval-augmented generation (RAG). ... / later / RAG architectures..."

- BAD (API doc, drift across synonyms): "The `/users` endpoint returns user objects. ... / later / The user endpoint supports filtering. ... / later / Our user resource accepts query parameters ..."
- GOOD (API doc): "The `/users` endpoint returns user objects. ... / later / `/users` supports filtering. ... / later / `/users` accepts query parameters ..."

- BAD (proposal, specific-aim drift): "Aim 1 focuses on retrieval. ... Aim 1 addresses document selection. ... The first aim investigates retrieval-augmented generation."
- GOOD (proposal): "Aim 1 focuses on retrieval. ... Aim 1 addresses document selection. ... Aim 1 investigates retrieval-augmented generation."

- BAD (runbook, system synonyms): "If the service is down, restart the service. If `app-v2` is offline, bounce the worker pool. If the backend stops responding, failover."
- GOOD (runbook): "If `app-v2` is offline, restart via `systemctl restart app-v2.service`. If `app-v2` still fails, failover to the replica."

##### Rationale for AI Agent

大语言模型常在文档内变化术语，因为训练分布中轻微奖励多样性（审稿人和编辑会把重复词汇标记为需要变化的散文，大语言模型因此学会交替）。但在技术写作中，同一实体的术语变化会掩盖实体身份，迫使读者检查每个新词是否指同一概念。RULE-01 覆盖术语的首次引入；RULE-F 覆盖之后的持续一致。Gopen & Swan 1990 在"topic continuity"下讨论这一点，即主语和实体应以相同的语言形式跨句重现。对于多回合生成的文档，风险尤其高，因为模型采样每个新段落时无法保证看到前面引入的术语，从而导致漂移。生成时的修正：定义术语后，智能体应为文档维护一份运行术语表，并始终复用已定义形式。

#### RULE-G：章节和子章节标题使用 Title Case

- **source**: 我对 2022–2026 年间数十个写作项目和代码发布中大语言模型输出的观察。大语言模型默认对 Markdown 和 LaTeX 标题使用 sentence case；在需要 title case 的学术和工程语境中，sentence case 漂移是明显的 AI 痕迹。
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞；RULE-G 采用肯定指令，因为应用 title case 是建设性 placement 而非反模式标记。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: low。润色而非理解问题；读者从两种大小写中都能恢复含义。但模式可见度很高，因为标题是速读者首先看到的东西。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 及类似结构标题表面。
- **enforcement**: Tier-1 `ask`（标题样式检查；以 sentence case 模式开头的 H2/H3/H4 标记为需转为 title case，排除意图使用 sentence case 的问句式或完整句标题）+ Tier-3 智能体自检。

##### Directive

章节和子章节标题中，首词、尾词以及所有主要词（名词、动词、形容词、副词、代词）大写。冠词（`a`、`an`、`the`）、并列连词（`and`、`but`、`or`、`nor`）和短介词（`of`、`in`、`on`、`to`、`for`、`by`、`at`、`with`）小写。适用于 Markdown（H1 至 H6）、LaTeX（`\section`、`
\subsection`、`
\subsubsection`）、reStructuredText 及类似结构标题表面。不适用于意图使用 sentence case 的句型标题（问句式标题或完整句文章标题）。

##### BAD → GOOD

- BAD (Markdown): `## Experimental results and analysis`
- GOOD (Markdown): `## Experimental Results and Analysis`

- BAD (LaTeX): `\subsection{Limitations and future work}`
- GOOD (LaTeX): `\subsection{Limitations and Future Work}`

- BAD (README): `## Getting started with the API`
- GOOD (README): `## Getting Started with the API`

- BAD: `### Related work in medical image retrieval`
- GOOD: `### Related Work in Medical Image Retrieval`

- BAD: `## Evaluating on out-of-distribution data`
- GOOD: `## Evaluating on Out-of-Distribution Data`

##### Rationale for AI Agent

大语言模型默认对 Markdown 和 LaTeX 标题使用 sentence case，因为其训练数据包含大量现代博客和文档站点 Markdown，那里 sentence case 是惯例（大型平台开发者文档和文档站点散文）。但学术和工程场所（多数会议、多数 IEEE 和 ACM 期刊、多数研究组的 README 惯例）使用 title case。在需要 title case 的语境中出现 sentence case 标题，读起来像机器生成或未编辑。修正很简单：写标题时就应用 title case。本规则在理解层面属于低严重度（读者无论如何都能恢复含义），但在 AI 痕迹检测层面可见度很高，因为标题是速读者首先看到的东西，大小写错误会发出疏忽信号。

#### RULE-H：用事实证据或具体证据支撑断言；不要含糊

- **source**: 我对 2022–2026 年间数十个写作项目和代码发布中大语言模型输出的观察。邻近 `agent-config` / `anywhere-agents` AGENTS.md 写作默认："If citing papers, verify that they exist." 本规则是反对含糊散文的三规则簇（RULE-03 针对模糊名词、RULE-08 针对未校准动词、RULE-H 针对无证据断言）中的旗舰。
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞（未验证机械执行）。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: critical。无引用断言是信任失败；伪造引用更糟（一旦被发现，对读者信任造成永久伤害）。大语言模型既默认给出无引用限定（"prior work shows"、"recent studies suggest"），也会主动 hallucinate 看起来合理但实际不存在的引用（Ji et al. 2023 对 NLG 中幻觉的综述；Agrawal et al. 2024 的实证测量）。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-3 智能体自检（判断什么需要归属）+ Tier-4 Codex 审阅作为主要关卡。智能体的辅助实践：在写任何 `Author Year` 引用前，通过搜索（DBLP、arXiv、Google Scholar 或被引论文自身的参考文献）验证引用存在且支持被引主张；否则标记 `[UNVERIFIED]` 占位或重写句子。绝不要未经验证生成引用。

##### Directive

当句子断言一个需要归属的事实主张（实验结果、已发表方法、社区共识、比较基准、历史事实）时，提供可验证的引用，或点明具体来源（按作者和年份的论文、基准、数据集、观察到的实验）。不要在没有点名具体工作的情况下写含糊归属（"prior work shows"、"it is well known that"、"recent studies suggest"、"many researchers believe"）。当主张是作者自己的观察时，陈述具体证据（数字、数据集、实验、条件）。绝不要编造引用；如果无法验证被引论文，删除主张、弱化为作者自己的观察，或标记 `[UNVERIFIED]` 并提请审阅。

##### BAD → GOOD

- BAD (paper): `Prior work has shown that late-interaction retrieval improves over lexical retrieval.`
- GOOD (paper): `Khattab and Zaharia 2020 (ColBERT) report MS MARCO passage-ranking MRR@10 of 0.360 for ColBERT versus 0.187 for BM25-Anserini, using contextualized late interaction over BERT token embeddings.`

- BAD: `It is widely accepted that longer context improves RAG performance.`
- GOOD: `Liu et al. 2023/2024 (TACL, "Lost in the Middle") show that models answer less accurately when the relevant evidence is in the middle of a long context than near the beginning or end; Dsouza et al. 2024 report the same lost-in-the-middle pattern for GPT-4 and Claude 3 Opus.`

- BAD (paper): `Several studies have demonstrated the effectiveness of this approach.`
- GOOD (paper): `In our reproduced evaluation, the model improves GSM8K exact-match accuracy from 92.1% to 95.2% and MATH exact-match accuracy from 48.0% to 51.4% under the same decoding settings.`

- BAD (grant proposal): `Our pilot results look promising.`
- GOOD (grant proposal): `Our pilot (N=30 cohort, 3-month follow-up) shows AUROC 0.84 for the primary endpoint versus 0.72 for the standard-of-care baseline (p=0.012).`

- BAD (blog post): `Many researchers believe that contrastive learning produces better embeddings.`
- GOOD (blog post): `Chen et al. 2020 (SimCLR) report 76.5% ImageNet top-1 linear-evaluation accuracy for a self-supervised ResNet-50, a 7% relative gain over prior self-supervised methods and comparable to a supervised ResNet-50 baseline in their setup.`

- BAD (commit message): `Fix based on user feedback.`
- GOOD (commit message): `Fix null-pointer crash reported in issue #1847 (reproducible with empty cart).`

##### Rationale for AI Agent

大语言模型默认产出含糊、无引用的断言，这是从训练语料中公式化摘要和综述散文吸收的默认语体。"prior work shows"、"recent studies suggest"、"it is well known that"、"many researchers believe" 等短语在学术引言和综述文章中高频出现，它们在具体断言之间充当过渡填充。大语言模型以 comparable 频率采样它们，却没有人类作者写作时心中的具体归属。此外，大语言模型会 hallucinate 看起来合理的引用（匹配作者惯例、年份范围、会议模式），但指向不存在的论文；幻觉率在各领域都有充分记录。两种失败会叠加：无引用断言不可验证，而伪造引用比无引用更糟，因为一旦被发现会永久损害读者信任。在写任何事实断言句之前的实操检验：这背后是否有具体、可验证的来源、观察或数字？如果有，按作者和年份陈述，或按数据集和测量陈述。如果没有，要么在写之前找到来源，要么把句子重写为关于作者自身经验的主张（仍需具体：数字、数据集、条件）。针对大语言模型：绝不要未经 DBLP、arXiv、Google Scholar 或被引论文自身参考文献验证就生成引用。如果当前会话无法验证，标记 `[UNVERIFIED]` 并提请审阅。相关：RULE-03 对抗模糊名词；RULE-08 对抗未校准动词；RULE-H 对抗无证据断言。三条规则都指向具体、可验证、诚实的散文；一句 sloppy 的句子往往同时触发三条规则。

#### RULE-I：技术散文中优先使用完整形式而非缩略形式

- **source**: 我对 2022–2026 年间数十个写作项目和代码发布中大语言模型输出的观察。邻近 `agent-config` / `anywhere-agents` AGENTS.md 格式默认："Prefer full forms such as 'it is' and 'he would' rather than contractions."
- **agent-instruction evidence**: Zhang et al. 2026 支持在编码智能体指令文件中对反模式指令使用否定措辞；RULE-I 采用肯定指令，因为优先使用完整形式是建设性 placement 而非反模式标记。Bohr 2025 支持将指令与示例配对，以在配对式两回合代码生成工作流中加强对初始风格的控制（不适用于开放式散文）。
- **severity**: low。语体而非理解问题；读者能正确解析缩略形式。出于一致性标记，因为语体漂移（正式散文中出现缩略）读起来像粗心。
- **scope**: `.md`、`.tex`、`.rst`、`.txt` 以及源文件中的散文段落。
- **enforcement**: Tier-1 `ask`（缩略列表："it's"、"doesn't"、"don't"、"won't"、"can't"、"I'm"、"you're"、"we're"、"they're"、"that's"；标记并给出展开建议）+ Tier-3 智能体自检。

##### Directive

在正式技术散文（研究论文、基金提案、API 规范、技术文档）中，优先使用 "it is" 而非 "it's"、"does not" 而非 "doesn't"、"cannot" 而非 "can't"、"will not" 而非 "won't"、"I am" 而非 "I'm"、"you are" 而非 "you're"。缩略在非正式语体（博客文章、发布说明、提交信息、随意文档）中可接受，但即使在那里也要有意识：缩略设定了一种语体，如果周围散文是正式的，缩略就会读起来像语气断裂。实操检验：如果周围句子使用完整形式，缩略会显得突出；如果周围句子使用缩略，完整形式会显得突出。选定语体并在文档内保持一致。

##### BAD → GOOD

- BAD (paper): `It's worth noting that the model doesn't converge when the learning rate is too high.`
- GOOD (paper): `The model does not converge when the learning rate is too high.` （"it is worth noting that" 本身也是填充短语，应按 RULE-04 删除。）

- BAD (proposal): `We've shown in prior work that this approach isn't sensitive to initialization.`
- GOOD (proposal): `We have shown in prior work that this approach is not sensitive to initialization.`

- BAD (API spec): `If the request body can't be parsed, the endpoint won't return a 200 response.`
- GOOD (API spec): `If the request body cannot be parsed, the endpoint does not return a 200 response.`

- BAD (technical spec): `The client shouldn't retry on 4xx errors.`
- GOOD (technical spec): `The client must not retry on 4xx errors.`

- BAD (register drift in paper abstract): 以完整形式开头，然后出现：`Our results show it's possible to achieve this with less compute.`
- GOOD (paper abstract): `Our results show that it is possible to achieve this with less compute.`

##### Rationale for AI Agent

大语言模型在技术散文中使用缩略的频率高于优秀人类写作者，因为训练语料混合了正式语体（论文、规范、政府文件）和非正式语体（博客、论坛回答、发布说明），而大语言模型在采样时不会与周围散文进行语体匹配。结果是：在一个正式段落中，会出现一两个细心写作者本会使用完整形式的缩略。缩略本身没错；它们是语体标记。在正式技术散文（本规则集的目标范围）中，完整形式是预期语体。在非正式表面（发布说明、博客、提交信息）中，缩略可接受，有时甚至因声音而更受青睐。本规则关乎与周围语体保持一致：选定一种并在文档内保持，而不是在段落中途漂移。
