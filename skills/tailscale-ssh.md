---
name: tailscale-ssh
kind: workflow
role: ops
tier: either
lines: 74
shared: false
---

# tailscale-ssh

Confirm Tailscale connectivity and OpenSSH server readiness on this Windows PC, then hand back the exact SSH command to connect from the phone/other device. No JupyterLab/notebook involved — use option-research-notebook for that.

- **Kind** — does a thing — invoked repeatedly
- **Role** — ops
- **Runs as** — either
- **Lives in** — `~/.claude/skills`
- **Size** — 74 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.
