---
name: spx-option-chain-unify
kind: workflow
role: ops
tier: either
lines: 340
shared: false
---

# spx-option-chain-unify

Plan to consolidate SPX option chain history into one local, schema-consistent Parquet archive spanning OptionsDX (2010-2023), the ThetaData backfill (2024-2026-08-20), and the live daily ETL (2026-08-21+, currently in GCS only) — with validation across the joins.

- **Kind** — does a thing — invoked repeatedly
- **Role** — ops
- **Runs as** — either
- **Lives in** — `~/.claude/skills`
- **Size** — 340 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.
