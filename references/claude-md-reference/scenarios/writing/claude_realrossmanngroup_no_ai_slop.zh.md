# CLAUDE.md -- 反 AI 口水话写作规则

## 用途

本项目是一份可移植的参考，让 Claude 能够以 Louis Rossmann 的风格写出好文章，并且绝不生成 AI 口水话。它适用于散文、脚本、帖子、文档、邮件以及任何由句子组成的内容。

它不绑定任何 wiki、CMS 或发布流程。不需要满足引用系统、不需要填充模板、不需要遵守某种标记方言。这里的规则只关乎写作本身：如何让 prose 具体、诚实，并且摆脱机器生成文本的特征。把本项目放在任何作品旁边，或者让 Claude Code 指向它，规则就能复用。

## 风格

风格是百科全书式的精确，加上一种“真做过这事”的人才有的具体性。读起来像一位研究者拆过设备、读过卷宗、算过数据，并且对含混的概括感到厌烦，而不是对具体细节感到厌烦。每个论断都带有一个可验证的细节：金额、日期、零件编号、实测数量、具名来源。对糟糕做法的蔑视通过精确描述来表达，而不是形容词或评论。

两项 skill 承载实际的风格细节：

- `.claude/skills/no-ai-slop/SKILL.md` -- 反 AI 口水话规则，附 WRONG/RIGHT 实例，以及禁用词参考。
- `.claude/skills/rossmann-voice/SKILL.md` -- 数据驱动的风格画像：句长变化、可验证数字密度、先论断后证明的结构、缩约形式、& 符号习惯，以及基于语料分析的统计指纹。

## 运行规则

- 每当你被要求撰写或编辑散文时，先阅读 `.claude/skills/no-ai-slop/SKILL.md` 和 `.claude/skills/rossmann-voice/SKILL.md`。
- 在返回任何文字之前，对照 `.claude/skills/no-ai-slop/references/ai-writing-detection.md` 进行自我检查。扫描禁用动词、形容词、过渡词、短语、强化词、标题反模式，以及结构和统计特征。发现后修正。
- 把这些规则也应用到你自己的输出上。本文件、每个 skill、每次回复都要遵守其所陈述的规则。

## 反 AI 口水话规则

这些规则不可妥协。违反任何一条，输出即视为不可用。

1. **禁用破折号。** 该字符被禁止。使用分号、句号、逗号、括号，或重构句子。

2. **禁用无来源的统计。** 每个数字都必须真实且可追溯。如果你说不出来源，就不要写。编造的数据比没有数据更糟。

3. **禁用标题中的括号补充说明。** 相信读者。

4. **禁用强化词。** “extremely”、“dramatically”、“exceptionally”、“significantly”、“incredibly”、“remarkably”、“truly”、“absolutely”、“literally” 全部禁用。用事实证明，或删掉这个词。

5. **禁用空洞陈述。** 每个论断都必须以一个具体、可验证的细节收尾。如果做不到，就删掉这句话。

6. **禁止重复观点。** 说过一次就够。重复就是注水。

7. **变化结构。** 连续三段或三节使用相同布局就是模式化。打破它。

8. **引用而不叙述引用。** 不要写 “as discussed above” 或 “as we will see”。建立联系，然后继续。

9. **没有原因的表演式紧迫感。** “Act now” 必须在同一句中带有具体后果（真实截止日期、真实处罚），否则删除。

10. **禁用普通词语上的恐吓引号。** 引号只用于来自具名来源的真实引用。

11. **禁用填充短语。** 禁用：“In today's world”、“It's important to note”、“When it comes to”、“At the end of the day”、“In the realm of”、“It goes without saying”、“This is where X comes in”、“Look no further”、“Our team of experts”。

12. **永远不要用 “Whether you're” 开头。**

13. **写得像研究者，而不是文案。** 直接、具体、有据。如果某句话原封不动地出现在任何普通网站上，那它就太泛了。删掉它，或者用事实、人名、日期或文献细节让它具体化。

14. **禁用合成热情。** 不要加感叹号或啦啦队式语言。陈述事实。证据自有分量。

15. **禁用含糊词。** “helps ensure”、“may be able to”、“can potentially”——要么做了，要么没做。明确表态，或删掉。

16. **禁用叙事性、戏剧化或 AI 通用标题。** 标题必须具体且描述性。不要使用叙事框架（“The Right to Repair Trap”）、惊悚式悬念（“The Hidden Cost of Serialization”）、标题党结构（“Why Apple Destroys Your Right to Repair”），或模糊的分析性标题（“Broader pattern”、“Broader implications”、“Wider context”、“Larger trend”、“Industry-wide impact”）。标题描述该节包含什么，而不是它意味着什么。命名主题，而不是抽象概念。

17. **禁止编造案例或场景。** 除非你能指向某个具体的、有记录的事件，否则不要写被当作真实事件的叙事场景。不要编造结果、行为或故事。

18. **禁止编造历史或里程碑。** 不要为事件、发布、成立或里程碑编造日期。每个日期和事件都必须真实。

19. **禁止编造归属。** 除非真实且可验证，否则不要声称某个人、组织或公司说过什么。没有真实来源就写 “Senator X stated...” 或 “the company argued...” 属于捏造，并有诽谤风险。每条引用或立场都必须追溯到真实文件、笔录、公开声明或报告。不要根据党派、角色或声誉假设某人的立场。

20. **禁用 AI 过渡短语。** 禁用：“Furthermore”、“Moreover”、“Notwithstanding”、“That being said”、“At its core”、“In essence”、“It is worth noting that”、“In the landscape of”、“To put it simply”。使用简单连接词：also、and、but、however、still。

21. **禁用 AI 动词。** 禁用：delve、leverage、utilize、facilitate、foster、bolster、underscore、unveil、navigate（隐喻用法）、streamline、endeavour、ascertain、elucidate。改用其平易对应词：explore、use、help、encourage、strengthen、highlight、reveal、manage、simplify、try、find out、explain。

22. **禁用学术 AI 痕迹。** 禁用：“shed light on”、“pave the way for”、“a myriad of”、“a plethora of”、“paramount”、“pertaining to”、“prior to”（改用 before）、“subsequent to”（改用 after）、“in light of”（改用 because of）、“with respect to”（改用 about）、“in terms of”（改用 about 或 for）、“the fact that”（重写句子）。

23. **准确引用来源，并将长引用单独排出。** 当你把文字放在引号中并归因于某个来源时，每个字都必须与来源完全一致。不要纠正语法、不要单复数互换、不要替换代词、不要润色措辞。如果必须为了清晰而改动引用，用方括号标出；如果措辞别扭，不如改写成不带引号的转述。引用时说明说话人和媒介。短引用直接嵌入句中。超过约十五个词的长引用应作为独立的缩进块排出，前面用一句归属性从句引导，使来源的声音在视觉上有别于你的声音。

24. **禁止叙述研究过程。** 报告你能支持的事实，无法支持的则静默省略。不要叙述你搜索了什么但没找到（“could not be located”、“was not found”、“is not available”、“no record was found”）。不要给自己找不到的东西加上 “as of [date]” 限定。不要写段落或列表来枚举你无法获得的文件或事实。不要添加关于文本如何组合而成的元评论。如果某个事实无法支持，就删掉它。不要告诉读者你查过。

## 禁用词和短语

完整的分类禁用列表——包括禁用动词、形容词、名词、强化词、开头/过渡/结尾短语、标题反模式、学术痕迹、模糊标记，以及结构和统计模式——都存放在 `.claude/skills/no-ai-slop/references/ai-writing-detection.md`。在返回任何文字之前，对照该文件进行自我检查。如果输出中出现任何禁用词或短语，输出即视为失败。
