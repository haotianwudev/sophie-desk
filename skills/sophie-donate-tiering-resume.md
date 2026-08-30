---
name: sophie-donate-tiering-resume
kind: task
role: integrator
tier: claude
lines: 94
shared: false
---

# sophie-donate-tiering-resume

Resume the Stripe donations -> tier promotion feature on Sophie. Implementation is code-complete on both repos; use this to pick up the remaining verification/deployment steps (migration, env vars, end-to-end test).

- **Kind** — **really a task** — belongs in `tasks/`, not here
- **Role** — integrator
- **Runs as** — claude
- **Lives in** — `~/.claude/skills`
- **Size** — 94 lines

> [!warning] Not visible to both agents
> Only in `~/.claude/skills/`, so agy cannot invoke it. Move to the repo's
> `.agents/skills/` to share it.

> [!note] This is a task wearing a skill's clothing
> Move its state to `tasks/` and leave only the reusable how-to behind.
