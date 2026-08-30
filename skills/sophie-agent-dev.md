---
name: sophie-agent-dev
kind: guide
role: architect
tier: claude
lines: 127
shared: false
---

# sophie-agent-dev

Dev workflow for the Sophie Agent (LangChain tool-calling agent + AG-UI server + chat widget) in sophie-pipeline/sophie_agent. Ensures both dev servers (AG-UI Python server on :8000, Next.js client on :3000) are running, and gives quick CLI commands for iterating on toolkits/profiles/prompts without going through the browser.

- **Kind** — reference — stable, read before building
- **Role** — architect
- **Runs as** — claude
- **Lives in** — `~/.claude/skills`
- **Size** — 127 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.
