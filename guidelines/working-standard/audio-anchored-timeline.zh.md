---
name: audio-anchored-timeline
description: 在生成含旁白或音乐的视频或动画时使用,尤其涉及 TTS。防止视觉时间线与实际音频时长不匹配的漂移。用于 creative-media 场景。
profiles: [creative-media]
scopes: [claude, rules]
priority: medium
triggers:
  files: ["remotion.config.*", "*.tsx", "audio/", "voiceover/"]
  user_intents: [produce-material]
conflicts: []
---

# 以音频为锚定时间线

**先生成音频。把视觉锚定到它的实际时间戳。**

- TTS 和旁白的实际时长会偏离估算。不要信计划好的字数。
- 生成音频,测量真实时长,然后把视觉对齐到这些时间戳。
- 如果必须先规划视觉,在音频生成后跑一次时间校准。
- 标准旁白大约 150 WPM。演示常常 1.5 到 2 倍速。但要验证,不要假设。

**准则生效的标志:** 没有任何视觉时间点假设了一个未测量的音频长度,最终播放保持同步。
