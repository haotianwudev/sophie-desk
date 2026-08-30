---
name: option-research-notebook
kind: workflow
role: ops
tier: either
lines: 96
shared: false
---

# option-research-notebook

Start (or reuse) a remote JupyterLab server for sophie-option-research over Tailscale, and hand back a direct link to open on the phone — optionally straight into a named notebook.

- **Kind** — does a thing — invoked repeatedly
- **Role** — ops
- **Runs as** — either
- **Lives in** — `~/.claude/skills`
- **Size** — 96 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.
