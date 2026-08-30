---
name: intro-manim
kind: workflow
role: scribe
tier: agy
lines: 203
shared: false
---

# intro-manim

Generate a VideoScribe-style animated intro using Manim. Image/video drags from bottom-left to left side with emphasis, then 4 styled pill banners pop in on the right with GrowFromCenter + Write animation, ending with a three-line final title. Supports both static images and playing videos composited via moviepy. High quality 1080p60 output.

- **Kind** — does a thing — invoked repeatedly
- **Role** — scribe
- **Runs as** — agy
- **Lives in** — `~/.claude/skills`
- **Size** — 203 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.
