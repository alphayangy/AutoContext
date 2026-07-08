---
name: audio-anchored-timeline
description: Use when generating video or animation that includes voiceover or music, especially with TTS. Prevents timeline drift where visual timings don't match actual audio duration. Use in creative-media contexts.
profiles: [creative-media]
scopes: [claude, rules]
priority: medium
triggers:
  files: ["remotion.config.*", "*.tsx", "audio/", "voiceover/"]
  user_intents: [produce-material]
conflicts: []
---

# Audio-Anchored Timeline

**Generate audio first. Anchor visuals to its actual timestamps.**

- TTS and voiceover durations drift from estimates. Don't trust planned word counts.
- Generate the audio, measure its real duration, then align visuals to those timestamps.
- If you must plan visuals first, run a timing-sync pass after audio is generated.
- Standard narration is roughly 150 WPM. Demos often play at 1.5 to 2x. But verify, don't assume.

**This is working if:** no visual timing assumes an audio length that wasn't measured, and final playback stays in sync.
