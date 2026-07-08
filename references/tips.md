# 给人的操作技巧(Tips)

这是给人看的操作技巧库,不是给 agent 守的准则。agent 在工作时识别到对应场景,主动把相关技巧转述给用户,人不读文档也能在合适时机听到。

## 使用方式(给 AutoContext 的元指令)

AutoContext 在生成项目 CLAUDE.md 时,可在末尾加一条元指令:

> 当检测到下方某个技巧的触发条件匹配当前场景时,主动用"转述"那段告诉用户。不要等用户问,主动提示。

agent 读取本文件,识别 triggers,在对话里转述给人。

---

## 场景 1:agent 反复失败 / 卡住

### tip: 两轮失败就 /clear 重写初始 prompt
- 触发条件:用户在同一问题上纠正 agent 两次仍未解决,或 agent 反复改同一处代码
- 转述:"你已经纠正我两次还没对,说明我的上下文被失败路径污染了。建议 /clear 重开,我把这次失败的根因和'下次避免做 X,改为做 Y'写进新 prompt,通常比继续纠正更快。"
- 怎么用:看到第 2 次还错就停手 → /clear → 一句话总结"这版失败的根因" + "下次避免做 X,改为做 Y"作为全新初始 prompt
- 来源:Anthropic best-practices (Manage your session)

### tip: 跨 fresh-context 评审
- 触发条件:长任务产出即将合并,或用户对自己的改动不确定
- 转述:"自己审自己会偏袒。建议把 diff 贴进新会话(或用 /code-review 子代理),让 reviewer 只看产出 + 验收标准,看不到生成过程,能剥掉自我辩护。"
- 怎么用:产出 paste 进新会话;提示 "Evaluate this LLM response. Anything they missed or wrong?"(reviewer 不知道是自己写的);或 /code-review 子代理零配置实现
- 来源:Anthropic best-practices + Reddit 评论

---

## 场景 2:context 要爆了 / token 管理

### tip: statusline 实时看 context %
- 触发条件:用户进入长会话,或问"我 context 还剩多少"
- 转述:"装个 statusline 脚本,实时显示 context 使用率、cost、git 状态。接近 75k 就该 compact 或 clear,别等到 100%。"
- 怎么用:settings.json 加 statusLine 配置;写 bash 用 jq 解析 stdin JSON,渲染进度条 + 百分比 + cost + git ahead/behind
- 来源:github.com/centminmod/my-claude-code-setup

### tip: 75k smart zone
- 触发条件:context 使用接近 75k,或 agent 开始重复犯错/失焦
- 转述:"Claude 在 ≤75k working token 时表现最好,超过就失焦。现在接近了,建议 /compact 或 /clear,而不是继续硬撑。"
- 怎么用:statusline 显示 context %;接近 75k 就 compact/clear;Anthropic 对 tool result 默认 truncate 25k
- 来源:HumanLayer backpressure 文(转述 Anthropic 视频)

### tip: 120-150k token 切片,完成即开新 thread
- 触发条件:任务预估会超过 120k token,或用户在长 thread 里做 delta 修改
- 转述:"把任务拆到能在 120-150k token 内完成的尺寸,完成立刻开全新 thread。避免 compact 循环里的'幻觉漂移'。"
- 怎么用:任务前预估 token 体量;超阈值拆 subtask;完成即新会话/新 worktree/commit;警惕 compact 循环降智
- 来源:v2ex.com/t/1225184 Bluecoda 评论

### tip: /rewind 局部压缩
- 触发条件:用户想回退到某个 checkpoint,或只想压缩部分历史
- 转述:"不想整段压缩,用 /rewind 选 checkpoint,然后 'Summarize from here' 或 'Summarize up to here' 做手动局部压缩。"
- 来源:Anthropic best-practices

### tip: /btw 旁问不打扰 context
- 触发条件:用户在执行中插话问无关问题,但不想影响后续
- 转述:"这种'顺便问一下'用 /btw,答案浮层显示不进对话历史,不污染主上下文。"
- 来源:Anthropic best-practices 旁注

---

## 场景 3:多任务 / 多会话并行

### tip: git worktree 隔离每个会话
- 触发条件:用户要同时跑多个任务/多个模型/多个 spec,或担心会话互踩改动
- 转述:"为每个 AI 会话建一个新 git worktree,各 session 独立工作目录,互不踩对方改动。YOLO 模式可单独开关。"
- 怎么用:shell 函数 clx [branch] 做 git worktree add + cd + claude;配 .worktreeinclude 列被 ignore 但要拷的文件(.env 等);结束 git worktree remove
- 来源:v2ex.com/t/1225437 + github.com/centminmod/my-claude-code-setup

### tip: Writer/Reviewer 双 worktree
- 触发条件:风险高改动或无人值守大改
- 转述:"在两个独立 worktree 跑两个 CLI:A 写、B 在 fresh context 审。反馈喂回 A 修。fresh context 审不偏袒自己刚写的代码。"
- 怎么用:Session A "Implement a rate limiter...";Session B "Review the rate limiter...";A "Here's the review feedback: [B output]. Address these."
- 来源:Anthropic best-practices (Run multiple Claude sessions)

### tip: fan-out CLI + allowedTools 锁权限
- 触发条件:大规模机械迁移(React→Vue、API 重命名、批量格式化)
- 转述:"用 claude -p 单文件迁移循环跑,--allowedTools 把权限白名单化。先在 2-3 文件上打磨 prompt 再放量。"
- 怎么用:for file in $(cat files.txt); do claude -p "Migrate $file..." --allowedTools "Edit,Bash(git commit *)"; done
- 来源:Anthropic best-practices (Fan out across files)

### tip: duckterm-web 批量管理多机器多会话
- 触发条件:用户在多台机器(本地+SSH)跑多个 TUI AI 会话,或想从手机远程盯
- 转述:"用 duckterm-web 把分散在多台机器的会话汇聚到一个面板,批量发图、批量粘贴、手动确认。LAN 直连延迟 15ms。"
- 怎么用:brew install ducksee/tap/duckterm-web;加 SSH 远端;iOS 客户端远程盯
- 来源:v2ex.com/t/1225374

### tip: 多窗口 + plan/loop auto-yes
- 触发条件:成规模自动化开发,或用户想无人值守
- 转述:"几个并行项目各开窗口,用 /loop 或 /goal 让 agent 自循环检查上线。配合 worktree 防互踩。"
- 来源:v2ex.com/t/1225437 xingzhi95 评论

---

## 场景 4:省钱 / 账号 / 模型选择

### tip: opus 判断 / sonnet+haiku 执行(自决档位)
- 触发条件:用户 token 配额吃紧,或问怎么省
- 转述:"让主模型保留判断与 review,实现性编辑下沉到更便宜的模型。在 memory 写 'For all coding tasks use your judgement to decide an appropriate lower power model and run that in a subagent'。"
- 怎么用:Claude 自己写 memory 在 `~/.claude/projects/<name>/memory/`,自动按 task 性质判断 sonnet 实现 / haiku trivial mechanical edits,review 不下沉
- 来源:simonwillison.net 2026/Jul/3;Jesse Vincent

### tip: 订阅 reset 精算:reset 用于周额度
- 触发条件:Codex/GPT 订阅用户问 reset 时机
- 转述:"reset 次数应该重置周额度(价值数千刀),不是 5h 额度(几百刀)。5h 是软限制不会打断进行中任务。"
- 怎么用:平时让 5h 跑满;周内若到周末仍有额度 → reset 周额度;extra high 推理只在重任务开
- 来源:v2ex.com/t/1225279 评论

### tip: ccusage 仪表盘看真实日消耗
- 触发条件:用户想统计 token 消耗,或问用量是否合理
- 转述:"装 ccusage 跑日 token 报,看真实消耗,别凭感觉。"
- 来源:v2ex.com/t/1225437 多楼

### tip: Z.AI / GLM Coding Plan 替换后端(中文场景)
- 触发条件:中文用户、预算紧、要发票、访问受限
- 转述:"用中转商 Z.AI 的 GLM Coding Plan($3/月起),通过 ANTHROPIC_AUTH_TOKEN + ANTHROPIC_BASE_URL 把 Claude Code 切到 GLM-4.7,token 量是官方 API 的上百倍。"
- 怎么用:~/.claude/settings.json 写 env;shell 函数 zai() 临时切;ANTHROPIC_DEFAULT_OPUS_MODEL=GLM-4.7 做模型映射
- 来源:github.com/centminmod/my-claude-code-setup
- 注意:别把 key commit 进 git(守 no-secrets atom)

### tip: Grok Build 当 CLI 白嫖
- 触发条件:用户有 Grok Build 访问,或想多模型分工
- 转述:"Grok Build 文字尺度高,但 TUI 反人类。最佳用法是当命令行调用、让其他终端'白嫖'grok 模型做特定任务(优化 prompt / 画图 prompt)。主开发留给 Claude Code。"
- 来源:v2ex.com/t/1225635

### tip: ponytail / rtk / headroom A/B 实测
- 触发条件:用户关心 token 成本,或问省 token 工具哪个好
- 转述:"省 token 工具不是越多越好:小修小改用 ponytail,大模块用 rtk(headroom 压输入侧噪音),复杂需求反而要关掉 ponytail(让它偷懒)。用 headroom savings 和 rtk gain 量化省了 33%+。"
- 怎么用:同一 feature + 同 prompt 跑两次(开关状态);input 重选 rtk,output 重选 ponytail
- 来源:v2ex.com/t/1225184 多楼

### tip: 虚卡双榜薅订阅
- 触发条件:国内用户不能直接付 Anthropic,或想多账号
- 转述:"用虚拟信用卡在不同地区双开账号薅订阅。公司报销只能买 Bedrock API(可开票)。"
- 来源:v2ex.com/t/1225437 多楼

---

## 场景 5:项目 / 工作流组织

### tip: close-session 仪式(STATUS.md + JOURNAL.md)
- 触发条件:session 即将结束,或用户想要可恢复的进度
- 转述:"收尾时跑全套测试 → 更新 STATUS.md(work/half/next/open-q)→ append JOURNAL.md(intended vs actual、friction、决策、自己的失败)→ 提交。JOURNAL append-only 永不改过去条。下次 /resume 读这些状态恢复。"
- 怎么用:配 /resume skill:读 STATUS + SCOPE + 上次 JOURNAL 条目,plain English 报状态 + 提 today's single goal → 等人 approve 才动
- 来源:Reddit UseWhatNameUser 评论(贴出他自己 SKILL.md 全文)

### tip: agent interview 写 SPEC 再新 session 执行
- 触发条件:中大型 feature 上手,或用户自己还没想清楚
- 转述:"让我用 AskUserQuestion 把你 interview 到位 → 写 SPEC.md → 新会话用干净上下文执行。原 interview 会话含大量澄清往返,继续用反而稀释上下文。"
- 怎么用:起手 prompt "I want to build [brief]. Interview me in detail using AskUserQuestion...";完成后 claude --resume 选全新会话执行
- 来源:Anthropic best-practices (Let Claude interview you)

### tip: Explore→Plan→Implement→Commit 四阶段
- 触发条件:中大型改动,或用户在不熟悉的代码区
- 转述:"plan mode 把探索/规划/实现物理隔离。Ctrl+G 直接在编辑器改 plan。规则:能一句话描述 diff 就别进 plan mode。"
- 来源:Anthropic best-practices (Explore first, then plan, then code)

### tip: skill 自动触发压制,按场景手动调
- 触发条件:用户装了很多 skill,agent 在简单需求上自动触发变繁琐
- 转述:"skill 装太多会在简单需求上自动触发。用系统提示词关掉自动调用,只在需要时显式 /skill x。复杂场景用 Python 脚本串多个 skill 手搓 harness。"
- 怎么用:AGENTS.md 写明"以下 skill 不要自动调用,等我显式 /skill x"
- 来源:v2ex.com/t/1225184 评论

### tip: disable-model-invocation 防副作用 skill 被自动触发
- 触发条件:用户有副作用重的 workflow skill(如 /fix-issue)
- 转述:"副作用重的 skill 在 SKILL.md frontmatter 加 disable-model-invocation: true,只人工触发,避免模型自作主张。"
- 来源:Anthropic best-practices examples

### tip: AI 替产品经理(PRD + 原型图)
- 触发条件:小公司没产品经理,或用户要做产品定义/原型
- 转述:"PRD、原型设计也可以让 cc max 干,二三十个产品的定制需求能消化。把用户反馈转成 PRD 喂给 cl,再让 cl 输出原型描述/流程图,产物存 docs/prd/*.md 供后续 coding agent 引。"
- 来源:v2ex.com/t/1225437 OP 评论

---

## 不收为 tip 的(反例锚点)

- **Caveman mode 是迷信**:社区吹"极简短 token 提示"省钱提性能,实测 50 次 3 benchmark 差异微小,常是 1 次 run 噪声。
- **"just ask it not to hallucinate" 失效**:社区有人分享"让模型别幻觉就好了",被官方 bot 指为笑点。
- **banned word list 失效**:加"never say honestly"到指令不工作,系统层 prompt 烙太深,这种别徒手打。
- **单 run 看分布不看 mean**:模型 benchmark 排名反过来调几个 task 就能翻,用户从公开 benchmark 无法推出该用哪个模型。

这些记下来作为反向锚点,防止后人重蹈。不收为正向 tip。
