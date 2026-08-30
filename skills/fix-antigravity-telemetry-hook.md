---
name: fix-antigravity-telemetry-hook
kind: workflow
role: ops
tier: either
lines: 81
shared: false
---

# fix-antigravity-telemetry-hook

Fix agy (Google Antigravity / Gemini CLI) being completely frozen -- every tool call blocked by a PreToolUse hook error from the googlecloudtools.datacloud_telemetry plugin. Recurring issue, confirmed to have happened at least twice (2026-08-23, 2026-08-30).

- **Kind** — does a thing — invoked repeatedly
- **Role** — ops
- **Runs as** — either
- **Lives in** — `~/.claude/skills`
- **Size** — 81 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.
