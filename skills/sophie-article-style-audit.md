---
name: sophie-article-style-audit
kind: hybrid
role: auditor
tier: agy
lines: 124
shared: false
---

# sophie-article-style-audit

Audit and restyle existing Sophie articles against the current visual design spec, article by article, keeping each article's wiki entry in sync — for re-running across a quarter's worth of articles (e.g. "audit Sophie articles for style", "restyle Sophie article <slug> to the design spec", "check Sophie Q<N> <year> articles against style").

- **Kind** — **mixed** — stable guide plus a rotting status block; split it
- **Role** — auditor
- **Runs as** — agy
- **Lives in** — `~/.claude/skills`
- **Size** — 124 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.

> [!note] This is a task wearing a skill's clothing
> Move its state to `tasks/` and leave only the reusable how-to behind.
