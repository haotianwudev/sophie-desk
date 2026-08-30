---
name: spx-option-backfill
kind: task
role: ops
tier: claude
lines: 597
shared: false
---

# spx-option-backfill

Resume/run the free-tier ThetaData backfill of the SPX option chain gap (2024-01-02 through the live ETL's 2026-08-21 seed), filling the same Postgres table the live spx_option_snapshot ETL writes plus a local Parquet archive on F: — no cloud infra involved.

- **Kind** — **really a task** — belongs in `tasks/`, not here
- **Role** — ops
- **Runs as** — claude
- **Lives in** — `~/.claude/skills`
- **Size** — 597 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.

> [!note] This is a task wearing a skill's clothing
> Move its state to `tasks/` and leave only the reusable how-to behind.
