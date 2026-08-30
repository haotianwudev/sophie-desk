---
name: sophie-spx-write-conditions
kind: task
role: architect
tier: claude
lines: 499
shared: false
---

# sophie-spx-write-conditions

Build or resume the SPX Write Conditions tab — a fourth Options Viewer sub-tool showing SPX price/volume/range indicators plus a backtest-derived premium-selling verdict. Covers the research gate in sophie-option-research, the spx_tape_data ETL, GraphQL, and frontend.

- **Kind** — **really a task** — belongs in `tasks/`, not here
- **Role** — architect
- **Runs as** — claude
- **Lives in** — `~/.claude/skills`
- **Size** — 499 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.

> [!note] This is a task wearing a skill's clothing
> Move its state to `tasks/` and leave only the reusable how-to behind.
