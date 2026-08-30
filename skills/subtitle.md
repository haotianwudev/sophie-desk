---
name: subtitle
kind: workflow
role: scribe
tier: agy
lines: 113
shared: false
---

# subtitle

Generate English and Chinese SRT subtitles from a video file using faster-whisper (large-v3, CUDA) and Google Translate. Also generates bilingual SRT and social media copy for YouTube, 小红书, and Bilibili.

- **Kind** — does a thing — invoked repeatedly
- **Role** — scribe
- **Runs as** — agy
- **Lives in** — `~/.claude/skills`
- **Size** — 113 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.
