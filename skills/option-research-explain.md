---
name: option-research-explain
kind: workflow
role: quant
tier: claude
lines: 67
shared: false
---

# option-research-explain

Explain a sophie-option-research backtest study - build the structured memo, write the AI narrative, and save both to the option_research_evaluation table in the Sophie DB.

- **Kind** — does a thing — invoked repeatedly
- **Role** — quant
- **Runs as** — claude
- **Lives in** — `~/.claude/skills`
- **Size** — 67 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.
