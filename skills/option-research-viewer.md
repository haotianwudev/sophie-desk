---
name: option-research-viewer
kind: guide
role: architect
tier: claude
lines: 201
shared: false
---

# option-research-viewer

Local, read-only viewer for the sophie-option-research results store — a FastAPI JSON API (127.0.0.1:8010) plus a standalone Next.js UI (127.0.0.1:3010) for drilling strategy → study → parameter grid/scatter → single run. How to start it, how it is built, the store quirks it absorbs, how to verify and extend it, and the mistakes made building it. Use before touching src/lab/api or web/ in sophie-option-research, or when asked "what did we learn about put writing".

- **Kind** — reference — stable, read before building
- **Role** — architect
- **Runs as** — claude
- **Lives in** — `~/.claude/skills`
- **Size** — 201 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.
