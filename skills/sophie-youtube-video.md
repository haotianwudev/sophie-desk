---
name: sophie-youtube-video
kind: workflow
role: scribe
tier: agy
lines: 130
shared: false
---

# sophie-youtube-video

Find the latest video on the Sophie YouTube channel, match it to its companion article, and wire it into that article's ArticleFrame Watch card -- including the Bilibili cross-post when one exists.

- **Kind** — does a thing — invoked repeatedly
- **Role** — scribe
- **Runs as** — agy
- **Lives in** — `~/.claude/skills`
- **Size** — 130 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.
