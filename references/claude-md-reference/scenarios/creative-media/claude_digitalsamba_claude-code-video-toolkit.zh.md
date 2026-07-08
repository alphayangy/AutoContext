# claude-code-video-toolkit

本文件为 Claude Code（claude.ai/code）在使用此视频制作工具包时提供指导。

## 概述

**claude-code-video-toolkit** 是一个 AI 原生视频制作工作区。它为 Claude Code 提供从概念到最终渲染的专业视频制作所需的技能、命令和工具。

**核心能力：**
- 使用 Remotion（基于 React）进行程序化视频创建
- 使用 ElevenLabs 或 Qwen3-TTS 进行 AI 配音生成
- 使用 ACE-Step 1.5 进行 AI 音乐生成（文本生成音乐、人声、翻唱、分轨）
- 使用 Playwright 进行浏览器演示录制
- 使用 FFmpeg 进行素材处理

## 目录结构

```
claude-code-video-toolkit/
├── .claude/
│   ├── skills/          # Claude 的领域知识
│   └── commands/        # 引导式工作流
├── tools/               # Python CLI 自动化工具
├── templates/           # 视频模板
│   ├── sprint-review/   # 迭代回顾视频模板
│   └── product-demo/    # 营销/产品演示模板
├── brands/              # 品牌配置文件（颜色、字体、声音）
├── projects/            # 你的视频项目存放于此（gitignored）
├── examples/            # 精选展示项目（共享）
├── assets/              # 共享素材（声音、图片）
├── playwright/          # 浏览器录制基础设施
├── docs/                # 文档
└── _internal/           # 工具包元数据与注册表
```

## 注册表

`_internal/toolkit-registry.json` 是技能、命令、工具、模板、组件、转场和云端端点的权威来源——包括它们的路径、状态、选项、预设和环境变量。查询它以获取结构化数据。本文件侧重于注册表无法涵盖的**工作流指导、模式与知识**。

## 快速开始

**首次设置（可选，约 5 分钟）：**
```
/setup
```

它会引导完成云端 GPU、文件传输（R2）和声音配置。大多数功能是免费的。如果你只想用 Node.js 渲染视频，可以跳过。

**处理视频项目：**
```
/video
```

此命令将：
1. 扫描现有项目（继续或创建新项目）
2. 选择模板（sprint-review、product-demo）
3. 选择品牌（或用 `/brand` 创建一个）
4. 交互式规划场景
5. 创建包含 VOICEOVER-SCRIPT.md 的项目

**多会话支持：** 项目可跨越多个会话。运行 `/video` 即可从上次离开处继续。每个项目都会在 `project.json` 中跟踪其阶段、场景、素材和会话历史。

**或手动操作：**
```bash
cp -r templates/sprint-review projects/my-video
cd projects/my-video
npm install
npm run studio   # 预览
npm run render   # 导出
```

> **注意：** 创建或修改命令/技能后，请重启 Claude Code 以加载更改。

## 模板

模板位于 `templates/`。大多数是独立的 Remotion 项目；concept-explainer-short 是纯 Python。完整列表请参见注册表的 `templates` 部分。

### sprint-review
配置驱动的迭代回顾视频，包含主题系统、配置驱动内容（`sprint-config.ts`）、预置幻灯片（Title、Overview、Summary、Credits）、演示组件（单视频、分屏）和音频集成。

### product-demo
营销/产品演示视频，采用深色科技美学、基于场景的镜头组合（标题、问题、解决方案、演示、数据、CTA）、动画背景、旁白画中画（Narrator PiP）、浏览器/终端外壳，以及带弹簧动画的数据卡片。

### concept-explainer-short
9:16 竖屏概念解说短片（TikTok/Reels/YouTube Shorts）。**使用 Python/moviepy，而非 Remotion**——整个视频源自 `scenes.json`（每个场景的旁白 + 视觉素材）。流程：`gen_vo.py`（通过 voiceover.py 按场景生成 TTS，支持克隆或内置声音，`--max-wpm` 语速限制）→ `gen_captions.py`（使用 whisper 将单词时间戳与脚本文本强制对齐，需要 `pip install openai-whisper`）→ `build.py`（以音频为锚点的合成：静态图使用 Ken Burns 效果、循环片段、boomerang 循环片段、嵌入卡拉 OK 字幕胶囊、背景音乐自动 ducking）。每个阶段都会渲染——素材缺失前显示占位卡，音频生成前保持静音。视觉遵循 FLUX/Ideogram/LTX 分工：任何带文字的内容使用 `1440x2560` 的 Ideogram 卡片，动态 B-roll 使用 `576x1024` 的 LTX。

## 品牌配置文件

品牌位于 `brands/`。每个品牌定义视觉识别：

```
brands/my-brand/
├── brand.json    # 颜色、字体、排版
├── voice.json    # ElevenLabs 声音设置
└── assets/       # Logo、背景
```

详情请参见 `docs/creating-brands.md`。

## 共享组件

可复用视频组件位于 `lib/components/`。完整列表（含描述）请参见注册表的 `components` 部分。在模板中通过以下方式导入：

```tsx
import { AnimatedBackground, SlideTransition, Label } from '../../../../lib/components';
```

## Python 工具

音频、视频和图像工具位于 `tools/`。完整目录（含描述、选项、预设和环境变量）请参见注册表的 `tools` 部分。每个工具都支持 `--help`。

```bash
# 安装依赖
pip install -r tools/requirements.txt
```

**重要：始终从工具包根目录调用工具。** 在项目内部（`projects/my-video/`）工作时，`python3 tools/upscale.py` 这类工具路径会失败，因为 `tools/` 是相对路径。请始终使用：
```bash
cd /path/to/claude-code-video-toolkit && python3 tools/upscale.py ...
```
这对后台命令尤其关键，因为后台命令的工作目录可能不明确。

### 工具分类

| 类型 | 工具 | 使用场景 |
|------|------|----------|
| **项目工具** | voiceover, music, music_gen, sfx, sync_timing | 视频创建工作流期间 |
| **实用工具** | redub, addmusic, notebooklm_brand, locate_watermark | 对现有视频进行快速转换 |
| **云端 GPU** | image_edit, upscale, dewatermark, sadtalker, qwen3_tts, music_gen, flux2 | 通过 RunPod 或 Modal 进行 AI 处理（`--cloud runpod\|modal`） |
| **发布工具** | youtube_upload | 将成品渲染上传至 YouTube（使用 `/publish` 引导式工作流） |

实用工具可直接作用于任意视频文件，无需项目结构。

### 配音生成

```bash
# 按场景生成（推荐）
python tools/voiceover.py --scene-dir public/audio/scenes --json

# 使用 Qwen3-TTS（自托管，ElevenLabs 的免费替代方案）
python tools/voiceover.py --provider qwen3 --tone warm --scene-dir public/audio/scenes --json

# 单文件（旧版）
python tools/voiceover.py --script SCRIPT.md --output out.mp3
```

### 时间同步（配音后）

```bash
python3 tools/sync_timing.py                          # 仅比较，不应用
python3 tools/sync_timing.py --apply                  # 更新配置（默认 1s 填充）
python3 tools/sync_timing.py --apply --padding 1.5    # 自定义填充
python3 tools/sync_timing.py --voiceover-json vo.json # 使用 voiceover.py 的输出
python3 tools/sync_timing.py --json                   # 机器可读输出
```

### Qwen3-TTS（独立使用）

```bash
python tools/qwen3_tts.py --text "Hello world" --speaker Ryan --output hello.mp3
python tools/qwen3_tts.py --text "Hello world" --tone warm --output hello.mp3
python tools/qwen3_tts.py --text "Hello" --instruct "Speak enthusiastically" --output excited.mp3
python tools/qwen3_tts.py --text "Hello" --ref-audio sample.wav --ref-text "transcript" --output cloned.mp3
python tools/qwen3_tts.py --list-voices   # 9 位说话人：Ryan, Aiden, Vivian 等
python tools/qwen3_tts.py --list-tones    # neutral, warm, professional, excited 等
```

Temperature 控制表现力：`--temperature 1.2`（更具表现力）或 `--temperature 0.4`（更稳定一致）。

### 云端 GPU 提供商

所有云端 GPU 工具都通过 `--cloud runpod|modal` 支持两个提供商。RunPod 是默认选项。Modal 是在 RunPod 故障后作为可靠性备选项加入的，冷启动更快。

```bash
# --- RunPod 设置（自动化，每个工具只需一次） ---
echo "RUNPOD_API_KEY=your_key_here" >> .env
python tools/image_edit.py --setup
python tools/upscale.py --setup
python tools/qwen3_tts.py --setup
python tools/music_gen.py --setup

# --- Modal 设置（部署你需要的每个应用） ---
pip install modal && python3 -m modal setup
modal deploy docker/modal-upscale/app.py        # 然后将 URL 保存到 .env
modal deploy docker/modal-image-edit/app.py
# 完整指南请参见 docs/modal-setup.md
```

### AI 图像生成（FLUX.2 与 Ideogram 4）

工具包内置**两个**文本生成图像器。它们几乎没有重叠——选择的关键因素是
**图像是否需要清晰可读的嵌入文字**。

```bash
# FLUX.2 — 无文字背景 + 图像编辑（自托管、免费、Apache-2.0/可商用）
python tools/flux2.py --preset title-bg --brand digital-samba   # 用于 Remotion 文字叠加的背景
python tools/flux2.py --prompt "Abstract tech background, no text"

# Ideogram 4 — 清晰嵌入文字 + 精确颜色/布局（托管 API，约 $0.03-0.09/张，可商用）
python3 tools/ideogram4.py --json caption.json --output title.png   # 文字烘焙到图像中
python3 tools/ideogram4.py --prompt "Thumbnail: 'SHIP FASTER' bold" --output thumb.png
```

**关键区别——嵌入文字 vs. 用于叠加的背景：**

- **FLUX.2 预设刻意生成无文字背景**（`title-bg`、`cta`、`thumbnail`
  都以 "no text, no words, no letters" 结尾）。预期模式是 **FLUX 背景 →
  Remotion 在上方渲染文字**，这样文字保持可编辑、可按字母动画化，且精确到帧。这是 sprint-review **标题卡/下三分之一字幕** 的默认选择。
- **Ideogram 4 将清晰的设计文字烘焙进平面 PNG。** 一次生成即可获得像素级精确的字体 + 精确十六进制颜色，但它是静态的。当 **文字本身就是设计** 时选择它：YouTube/社媒缩略图（本来就是静态的）、引用/数据卡、场景内标牌/Logo、Remotion 叠加难以实现的风格化文字效果。它填补了一个真实空白——FLUX 和 LTX-2 都会在图像内文字上产生乱码。

| 需求 | 使用 |
|------|------|
| 动画/可编辑标题文字、下三分之一字幕、sprint-review 标题卡 | **FLUX.2 背景 + Remotion 文字** |
| 氛围/抽象背景、问题/解决方案插图、演讲者背景 | **FLUX.2** 预设 |
| 字体即设计的成品图像——缩略图、引用卡、场景内标牌 | **Ideogram 4** |
| 编辑现有照片（服装、重新构图、风格、背景） | **image_edit**（两个生成器都不支持编辑） |

Ideogram 4 可像其他生成器一样链接处理器：`ideogram4 → upscale.py`（清晰 4K）、
`ideogram4 → ltx2.py --input`（让静态图动起来），或直接将 PNG 放入 Remotion 的 `<Img>` 中。
Ideogram 4 在这里仅支持生成（不支持编辑）。JSON caption 格式请参见 `.claude/skills/ideogram4/`——Claude 将 caption 作为 "magic prompt" 扩展器编写；需要在 `.env` 中设置 `IDEOGRAM_API_KEY`。

### AI 图像编辑

```bash

# 图像编辑（Qwen-Image-Edit）
python tools/image_edit.py --input photo.jpg --prompt "Add sunglasses"
python tools/image_edit.py --input photo.jpg --prompt "Add sunglasses" --cloud modal
python tools/image_edit.py --input photo.jpg --style cyberpunk
python tools/image_edit.py --input photo.jpg --background office
python tools/image_edit.py --list-presets  # 完整预设列表

# 超分辨率放大（RealESRGAN）
python tools/upscale.py --input photo.jpg --output photo_4x.png --cloud runpod
python tools/upscale.py --input photo.jpg --scale 2 --model anime --face-enhance --cloud runpod
```

提示词指导请参见 `docs/qwen-edit-patterns.md` 和 `.claude/skills/qwen-edit/`。

### AI 音乐生成（ACE-Step 1.5）

默认提供商是 **acemusic**（官方云端 API，免费密钥可从 [acemusic.ai/api-key](https://acemusic.ai/api-key) 获取）。使用 XL Turbo 4B 模型，5Hz LM thinking 模式。可回退到 Modal/RunPod 以使用自托管 2B 模型。

```bash
# 背景音乐（默认使用 acmusic 云端 API）
python tools/music_gen.py --prompt "Upbeat tech corporate" --duration 60 --bpm 128 --key "G Major" --output music.mp3

# 生成 4 个变体，挑选最佳
python tools/music_gen.py --prompt "Subtle corporate tech" --duration 60 --variations 4 --output bg.mp3

# 快速模式（禁用 thinking）
python tools/music_gen.py --no-thinking --prompt "Quick draft" --duration 30 --output draft.mp3

# 视频制作场景预设
python tools/music_gen.py --preset corporate-bg --duration 60 --output bg.mp3
python tools/music_gen.py --preset tension --duration 20 --output problem.mp3
python tools/music_gen.py --preset cta --brand digital-samba --output cta.mp3

# 带人声和歌词的歌曲（使用结构标签划分段落）
python tools/music_gen.py \
  --prompt "Indie pop anthem, male vocal, bright guitar, studio polish" \
  --lyrics "[Verse]\nWalking through the morning light\nCoffee in my hand feels right\n\n[Chorus - anthemic]\nWE KEEP MOVING FORWARD\nThrough the noise and doubt\n\n[Outro - fade]\n(Moving forward...)" \
  --duration 60 --bpm 128 --key "G Major" --output song.mp3

# 翻唱 / 风格迁移
python tools/music_gen.py --cover --reference theme.mp3 --prompt "Jazz piano version" --output cover.mp3

# 重绘较弱段落（仅 acmusic）
python tools/music_gen.py --repaint --input track.mp3 --repaint-start 15 --repaint-end 25 --prompt "Guitar solo" --output fixed.mp3

# 从现有音频续写（仅 acmusic）
python tools/music_gen.py --continuation --input track.mp3 --prompt "Continue with jazz piano" --output extended.mp3

# 分轨提取
python tools/music_gen.py --extract vocals --input mixed.mp3 --output vocals.mp3

# 回退到自托管
python tools/music_gen.py --cloud modal --prompt "Background music" --duration 60 --output bg.mp3

# 列出预设
python tools/music_gen.py --list-presets
```

8 个场景预设：`corporate-bg`、`upbeat-tech`、`ambient`、`dramatic`、`tension`、`hopeful`、`cta`、`lofi`。提示词工程模式和视频制作集成指南请参见 `.claude/skills/acestep/`。

### 水印去除

```bash
# 定位水印坐标
python tools/locate_watermark.py --input video.mp4 --grid --output-dir ./review/
python tools/locate_watermark.py --input video.mp4 --preset notebooklm --verify

# 去除水印（RunPod）
python tools/dewatermark.py --input video.mp4 --region 1080,660,195,40 --output clean.mp4 --runpod
python tools/dewatermark.py --setup  # 一次性设置
```

**工作流：** 网格叠加 → 记录坐标 → 用 `--region` 验证 → 用 dewatermark 去除。

**本地模式** 需要 NVIDIA GPU（8GB+ 显存）。Mac 用户应使用 `--runpod`。

### 数字人视频生成（SadTalker）

```bash
# 基本用法
python tools/sadtalker.py --image portrait.png --audio voiceover.mp3 --output talking.mp4

# NarratorPiP 集成（推荐设置）
# 注意：--preprocess full 会保留图像尺寸（否则输出为正方形裁剪）
python tools/sadtalker.py \
  --image presenter_16x9.png \
  --audio voiceover.mp3 \
  --preprocess full --still --expression-scale 0.8 \
  --output narrator.mp4
```

**NarratorPiP 的关键参数：**
- `--preprocess full` — **关键！** 保留输入尺寸（默认 `crop` 输出正方形）
- `--still` — 减少头部移动，呈现专业效果
- `--expression-scale 0.8` — 表情更沉稳（默认 1.0）

**图像要求：** 面部占画面 30-70%，正面朝向，NarratorPiP 使用 16:9，建议 512px 以上。

详细选项和故障排除请参见 `docs/sadtalker.md`。

### Redub 同步模式

```bash
python tools/redub.py --input video.mp4 --voice-id VOICE_ID --sync --output dubbed.mp4
```

`--sync` 标志启用单词级时间重映射——当 TTS 语速与原始音频不同时至关重要。没有它，音频到结尾可能会漂移 3-4 秒以上。

**工作原理：** Scribe 转录原始音频 → TTS 生成带时间戳的新音频 → 分段映射（每段 15 个词）→ FFmpeg 每段变速。

### NotebookLM 品牌化

使用自定义品牌对 NotebookLM 视频进行后处理。解决重新配音的 TTS 音频超出安全视觉裁剪点的问题。

```bash
python tools/notebooklm_brand.py \
    --input video_synced.mp4 \
    --logo assets/logo.png \
    --url "mysite.com" \
    --output video_final.mp4
```

裁剪 NotebookLM 视觉内容，保留完整音频，用定格画面衔接，添加品牌化片尾。

### 发布到 YouTube

通过 Data API v3 将成品渲染上传至 YouTube。使用 `/publish` 命令进行引导式工作流（它会自动从 `project.json` 填充标题/描述/标签），或直接调用工具。

```bash
# 一次性登录（打开浏览器，在 _internal/.youtube/ 下缓存刷新令牌）
python3 tools/youtube_upload.py --auth

# 私有上传（安全默认）
python3 tools/youtube_upload.py --video out/video.mp4 --title "My video" \
    --description-file DESCRIPTION.md --tags "ai,agents,explainer" --json-out

# 定时公开上线
python3 tools/youtube_upload.py --video out/video.mp4 --title "My video" \
    --publish-at 2026-06-10T09:00:00Z --thumbnail out/thumb.png --json-out

# 验证所有内容而不上传（同时报告授权状态）
python3 tools/youtube_upload.py --video out/video.mp4 --title "Test" --dry-run --json-out
```

**设置使用 OAuth，而非 API 密钥**（上传代表某个频道执行）。一次性 Google Cloud Console 操作和 `.env` 中的 `YOUTUBE_CLIENT_SECRETS_FILE` 请参见
`docs/youtube-upload.md`。关键事实：
- 默认配额为每天 10,000 单位；`videos.insert` 约消耗 1,600 单位 → **每天约 6 次上传**。
- **未审核的 API 项目可能会将公开上传强制锁定为私有**——但这主要影响上传到*他人*频道的情况。第一方上传（你自己的项目 + 频道 + 账号）通常无需审核即可正常公开/定时发布。工具会报告实际返回的隐私状态。"Testing" 模式的刷新令牌约 7 天后过期（重新运行 `--auth`）。
- 缓存令牌保存在 `_internal/.youtube/` 中（gitignored——它们授予频道上传权限）。

## 视频制作工作流

1. **创建/继续项目** - 运行 `/video`，选择模板和品牌（或继续现有项目）
2. **审阅脚本** - 编辑 `VOICEOVER-SCRIPT.md` 规划内容
3. **收集素材** - 使用 `/record-demo` 录制演示或添加外部视频
4. **场景审阅** - 运行 `/scene-review` 在 Remotion Studio 中验证视觉效果
5. **设计优化** - 使用 `/design` 或在 scene-review 中选择 "Refine" 改进幻灯片视觉效果
6. **生成音频** - 使用 `/generate-voiceover` 生成 AI 旁白
7. **同步时间** - 运行 `python3 tools/sync_timing.py --apply` 更新配置时长
8. **预览** - 在项目目录中运行 `npm run studio`
9. **迭代** - 使用 Claude Code 调整时间、内容、样式
10. **渲染** - 运行 `npm run render` 生成最终 MP4
11. **发布** - 运行 `/publish` 将渲染结果上传至 YouTube（元数据自动从 `project.json` 填充）

## 项目生命周期

项目经历多个阶段，记录在 `project.json` 中：

```
planning → assets → review → audio → editing → rendering → complete
```

| 阶段 | 描述 |
|------|------|
| `planning` | 定义场景、撰写脚本 |
| `assets` | 录制演示、收集素材 |
| `review` | 在 Remotion Studio 中逐场景审阅（`/scene-review`） |
| `audio` | 生成配音、音乐 |
| `editing` | 调整时间、预览 |
| `rendering` | 最终渲染中 |
| `complete` | 完成 |

项目系统详情请参见 `lib/project/README.md`。

## 视频时间控制

时间控制至关重要。请记住以下准则：

### 节奏规则
- **配音驱动时间** — 旁白长度决定场景时长
- **阅读语速** — 标准旁白约 150 词/分钟（2.5 词/秒）
- **演示节奏** — 实时演示通常需要 1.5-2 倍加速（`playbackRate`）
- **转场** — 场景之间添加 1-2 秒填充
- **帧率** — 所有视频使用 30fps（帧数 = 秒数 × 30）

### 语速等级

| 语速 | WPM | 适用场景 |
|------|-----|----------|
| 慢速 | 120-130 | 技术解释、复杂概念 |
| 标准 | 140-160 | 一般旁白、演示、概述 |
| 快速 | 160-180 | 充满活力的开场、回顾、CTA |

### 按场景类型的旁白密度

| 场景类型 | 时长 | 旁白密度 | 说明 |
|----------|------|----------|------|
| 标题 | 3-5s | 0-10% | Logo + 标题，让画面有呼吸感 |
| 概述 | 10-20s | 70-90% | 3-5 个要点，以旁白为主 |
| 演示 | 10-30s | 30-50% | 让演示本身说话，只在关键时刻旁白 |
| 数据 | 8-12s | 70-90% | 读出亮点，跳过明显数字 |
| 片尾 | 5-10s | 0-20% | 快速淡出，可能加一句结束语 |
| 问题/解决方案 | 10-15s | 80-90% | 旁白推动叙事 |
| CTA | 5-10s | 60-80% | 清晰的行动号召，结尾留一拍 |

### 字数预算

撰写脚本前，先为每个场景预算字数：

```
目标时长 × 2.5 = 字数预算（标准语速）
停顿秒数 × 2.5 = 需从预算中减去的字数

示例：15 秒场景，含 1 秒停顿
  15 × 2.5 = 37 字预算
  1 × 2.5 = 3 字用于停顿
  可用：约 34 字旁白
```

在脚本中使用 `[pause 1.0s]` 标记。每秒停顿会从预算中消耗约 2-3 字。

### 时间计算
```
脚本字数 ÷ 150 = 配音分钟数（估算）
原始演示长度 ÷ playbackRate = 演示时长
场景总和 + 转场 = 视频总时长
```

### 何时检查时间
- **场景规划期间** — 在撰写前为每个场景预算字数
- **脚本撰写后** — 统计每个场景字数，与预算对比
- **生成音频后** — 运行 `sync_timing.py` 比较实际与估算时长
- **渲染前** — 确保每个场景的 `durationInFrames` 与实际音频匹配

### TTS 时长漂移（真正的时间问题）

TTS 引擎并不能稳定输出 150 WPM。实际中：
- **ElevenLabs** 倾向于压缩停顿并快速读完短句。50 秒脚本可能生成 40-45 秒音频。
- **Qwen3-TTS** 因说话人和语气预设而异。Ryan 使用 "professional" 语气比 "warm" 快约 10%。
- **短场景漂移更大** — 5 秒场景可能偏差 30%，而 30 秒场景偏差约 10%。

**TTS 生成后的反馈循环：**

1. 生成按场景音频文件
2. 运行 `python3 tools/sync_timing.py` 比较实际时长与配置时长
3. 运行 `python3 tools/sync_timing.py --apply` 自动更新配置
4. 对于演示场景：重新计算 `playbackRate = rawDemoDuration / actualNarrationDuration`
5. 渲染前在 Remotion Studio 中重新预览

**常见漂移模式与修复：**

| 问题 | 现象 | 修复 |
|------|------|------|
| 音频短于场景 | 结尾出现死寂/尴尬沉默 | 将 `durationInFrames` 减少以匹配音频 |
| 音频长于场景 | 旁白被截断 | 增加 `durationInFrames` 或修剪脚本 |
| 演示对旁白来说太快 | 观众跟不上 | 降低 `playbackRate` 或删减旁白 |
| 演示对旁白来说太慢 | 等待演示跟上 | 提高 `playbackRate`（通常 1.5-2 倍） |
| TTS 丢失停顿 | 脚本感觉有空间，音频感觉仓促 | 在 SSML 中添加显式 `<break time="1s"/>` 或延长场景填充 |
| 克隆声音语速过快 | 场景超过 170 wpm；重录也快（temperature 无效） | 语速继承自参考音频。使用 `--max-wpm 165`（保音调的 atempo 限制，voiceover.py 和 qwen3_tts.py 均支持），并以叙述语速录制 12-25 秒多样化句子的克隆参考 |

**语速 QC：** voiceover.py 和 qwen3_tts.py 会为每个生成文件报告 `wpm` 和 `pacing` 标签
（fast/slow/ok）——合成前请检查。舒适的旁白为 140-160 wpm；超过约 170 需标记。`--max-wpm` 可将检查转为自动修复。

### 修复不匹配
- **配音太长**：加快演示、修剪停顿、删减内容
- **配音太短**：放慢演示、添加场景、扩展旁白
- **演示太长**：提高 `playbackRate`（通常 1.5x-2x）
- **演示太短**：降低 `playbackRate`，或循环/延长

### 以音频为锚点的时间线（预防方法）

`sync_timing.py` 是反应式的——它在事后修复漂移。你可以通过**先生成音频，然后将视觉元素锚定到已知时间戳**而非预先估算时长来完全避免漂移。

**模式：**

1. 撰写脚本并拆分为按场景分段
2. 生成按场景 VO 文件：`voiceover.py --scene-dir public/audio/scenes --json`
3. 从 JSON 输出中读取实际时长
4. 将每个视觉元素锚定到时间线上的绝对时间戳

这在 Python/moviepy 构建中尤为清晰，每个片段都自带 `start=` 参数：

```python
# 以音频为锚点的场景时间线（总计 25s）：
#   Scene 1 tired      0.3 → 3.74  （音频 3.44s）
#   Scene 2 worries    4.0 → 8.88  （音频 4.88s）
#   Scene 3 introduce  9.1 → 11.90 （音频 2.80s）

text_clip("TIRED OF",     start=0.5,  duration=1.2)
text_clip("THIRD-PARTY",  start=1.0,  duration=1.8)
vo_clip("01_tired.mp3",   start=0.3)
vo_clip("02_worries.mp3", start=4.0)
```

顶部的注释块是事实来源。每个 `start=` 都引用它。漂移不可能发生，因为时长不是估算的——而是从已渲染音频中读取的。

**与 `<Series>` 式自动链式对比：**

| 方法 | 最适用于 | 缺点 |
|------|----------|------|
| 以音频为锚点的绝对开始 | 紧凑的广告式剪辑、30 秒以内短片、任何需要精确时间的场景 | 重新调整某场景时间时需要手动记账 |
| `<Series>` / 自动链式时长 | 相邻场景可灵活伸缩的长篇 sprint review | 漂移会在整个时间线上累积；需要 `sync_timing.py` 恢复 |

对于 Remotion 项目，你可以混合使用：对紧凑部分使用 `<Sequence from={...}>` 绝对帧，让 `<Series>` 处理其余部分。对于纯 Python 构建（`build.py` + moviepy），以音频为锚点是自然默认选择。

## 关键模式

### 动画（Remotion）
```tsx
const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
```

### 序列编排
```tsx
<Series>
  <Series.Sequence durationInFrames={150}><TitleSlide /></Series.Sequence>
  <Series.Sequence durationInFrames={900}><DemoClip /></Series.Sequence>
</Series>
```

### 媒体

**切勿使用原始 HTML `<video>` 标签** — Remotion 需要自己的组件以实现逐帧精确渲染。

工具包模板使用 `remotion` 包中的 `<OffthreadVideo>` 和 `<Audio>`。为与现有模板保持一致，请继续使用这些组件。上游 Remotion 现在也在较新的 `@remotion/media` 包中记录了 `<Video>` 和 `<Audio>`（请参见 `.claude/skills/remotion-official/`）——它们增加了修剪属性、通过 `toneFrequency` 的音高变换以及更丰富的循环行为。仅当需要这些功能时才按模板迁移；两种 API 都能正确渲染。

```tsx
<OffthreadVideo src={staticFile('demo.mp4')} />
<Audio src={staticFile('voiceover.mp3')} volume={1} />
<Audio src={staticFile('music.mp3')} volume={0.15} />
```

## 场景转场

工具包在 `lib/transitions/` 包含一个转场库。完整列表（含选项和最佳使用描述）请参见注册表的 `transitions` 部分。

### 使用 TransitionSeries

```tsx
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { glitch, lightLeak, zoomBlur } from '../../../lib/transitions';

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <TitleSlide />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={glitch({ intensity: 0.8 })}
    timing={linearTiming({ durationInFrames: 20 })}
  />
  <TransitionSeries.Sequence durationInFrames={120}>
    <ContentSlide />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

### 转场选项示例

```tsx
glitch({ intensity: 0.8, slices: 8, rgbShift: true })      // 科技/赛博朋克
lightLeak({ temperature: 'warm', direction: 'right' })       // 温暖庆祝
zoomBlur({ direction: 'in', blurAmount: 20 })                // 高能量
rgbSplit({ direction: 'diagonal', displacement: 30 })        // 色差效果
```

### 时间函数

```tsx
linearTiming({ durationInFrames: 30 })                                      // 匀速
springTiming({ config: { damping: 200 }, durationInFrames: 45 })            // 物理弹跳
```

### 转场时长指南

| 类型 | 帧数 | 说明 |
|------|------|------|
| 快速切换 | 10-15 | 快速、有力 |
| 标准 | 20-30 | 最常见 |
| 戏剧性 | 40-60 | 缓慢揭示 |
| 故障效果 | 15-25 | 应感觉突然 |
| 漏光 | 30-45 | 需要扫过的时间 |

预览所有转场：`cd showcase/transitions && npm run studio`

完整文档请参见 `lib/transitions/README.md`。

## 使用 frontend-design Skill 进行设计优化

`frontend-design` skill 可将幻灯片视觉效果从普通提升到独特。

### 用法
- **场景审阅期间**（`/scene-review`）：选择 "Refine" 进行视觉改进
- **专注会话**（`/design`）：深入优化特定场景——`/design title`、`/design cta`

### 何时使用
- 感觉普通的幻灯片场景
- 需要在场景间建立视觉对比时（例如平静标题 → 尖锐问题）
- 动画感觉太基础或太花哨时

### 视觉叙事弧线
考虑视觉强度如何在场景中递进：
- **标题**：设定基调，埋下视觉种子
- **问题**：制造张力（强烈对比）
- **解决方案**：缓解与希望回归
- **演示**：中性，以内容为主
- **数据**：建立可信度
- **CTA**：高潮 - 最大视觉能量

## 工具包工作与项目工作

**工具包工作**（工具包本身的演进）：
- 技能、命令、模板、工具
- 记录在 `_internal/ROADMAP.md`

**项目工作**（创建视频）：
- 位于 `projects/`
- 每个项目包含 `project.json`（机器可读状态）和自动生成的 `CLAUDE.md`

请将两者分开。不要将工具包改进与视频制作混在一起。

## 文档

- `docs/getting-started.md` - 首个视频 walkthrough
- `docs/creating-templates.md` - 构建新模板
- `docs/creating-brands.md` - 创建品牌配置文件
- `docs/optional-components.md` - 可选 ML 工具设置（ProPainter 等）
