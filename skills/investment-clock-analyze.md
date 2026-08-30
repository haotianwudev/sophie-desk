---
name: investment-clock-analyze
kind: workflow
role: quant
tier: claude
lines: 242
shared: false
---

# investment-clock-analyze

Analyze a Gemini Deep Research paper + FRED quantitative data to produce a final Investment Clock evaluation and save it to the database.

- **Kind** — does a thing — invoked repeatedly
- **Role** — quant
- **Runs as** — claude
- **Lives in** — `~/.claude/skills`
- **Size** — 242 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.
