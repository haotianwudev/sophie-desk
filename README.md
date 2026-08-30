# sophie-desk

The control plane for the Sophie platform and the SPX option research — a plain Obsidian vault
that is also a git repo. Task state lives here as markdown; code lives in the four work repos.

Design rationale (the visual pitch): https://claude.ai/code/artifact/089d0f72-450d-4547-8204-6953842e7f90
The same design in plain English, living in this repo: [sophie/work-model.md](sophie/work-model.md)

```
AGENTS.md          start here if you're an agent (agy or otherwise) working in this repo
Desk.md            the dashboard — all Dataview queries, nothing hand-maintained
Runbook.md         exact commands for recurring operations — relaunch, restart, connect
Skills.md          the skill catalogue, classified by role — generated, clickable
skills/            one card per skill
sophie/            the work model itself, written up in plain English
supervisor/        the probe loop -- run.py, its design doc, Task Scheduler registration
tasks/             one file per in-flight task
tasks/done/        archive — move here on completion
papers/            research library, one note per paper
notes/             durable notes; notes/pipeline/ is supervisor-written
probes/            one script per task, prints OK | RUN | STALL + a measurement
templates/task.md  the task template
```

## What this is *not*

Not a place for how-to instructions. Those stay as **skills** in each repo's
`.agents/skills/`. A skill answers *"how do I do X"* and is stable; a task answers
*"where did I get to on X"* and ends. Five current skills are really tasks and belong here
instead — that migration is the reason this repo exists. See **[Skills.md](Skills.md)** for
the full catalogue, classified by role.

Two numbers from that catalogue worth acting on:

- **3 of 25 skills are shared with agy** (this repo's own `sophie-desk` operating-conventions
  skill among them, in `.agents/skills/`, not `~/.claude/skills/`). The rest sit where only
  Claude Code can see them. Every one moved into a repo's `.agents/skills/` is capability both
  agents get.
- **5 skills are really tasks**, and they are among the largest files — `spx-option-backfill`
  at 597 lines, `sophie-spx-write-conditions` at 499. They grew that way because a task with no
  lifecycle only ever accumulates.

---

## Tools needed

### Obsidian plugins — required

| Plugin | Why | Notes |
|---|---|---|
| **Dataview** | Renders `Desk.md`. Without it the board is just code blocks. | Community plugin. Enable JS queries off; the table queries here are plain DQL. |
| **Obsidian Git** | Commit + pull on a timer, so the vault syncs to GitHub without thinking about it. | Set auto-pull on start, auto-commit every 10–15 min. |

### Obsidian plugins — optional

| Plugin | Why |
|---|---|
| **Templater** | Auto-fills `created`/`updated` when a task is made from the template. Obsidian's built-in Templates covers most of it. |
| **Kanban** | Drag-and-drop board if the Dataview tables ever feel too static. Probably unnecessary. |

### On the workstation

- **git** — already present.
- **Ollama** — the free Reader tier: first-pass paper summaries and embeddings over this vault.
  Not needed until the Librarian exists. Suggested pulls: a small instruct model for summaries,
  `nomic-embed-text` for embeddings.
- **Task Scheduler entry** — runs the supervisor at logon. Not needed until the supervisor exists.

### On the phone

- **Obsidian mobile** + **Obsidian Git** — this vault is small and markdown-only, which is the
  case where mobile git works acceptably. Read the board, edit notes, review results.
- **Tailscale + ConnectBot** — already set up. This is the path that lets you *act*, not just
  read: SSH to the workstation and talk to Claude Code or the supervisor.

---

## Conventions

- **Frontmatter stays flat.** Plain scalars only, no nested YAML — Dataview reads it literally.
- **`progress` and `probe_status` are supervisor-written.** Never hand-edit them; they are the
  measured half, and hand-editing makes the board lie in exactly the way probes exist to prevent.
- **Results are pointers, not copies.** A study tag and a row count, not the Sharpe numbers.
- **Claiming is a commit.** Set `status` + `assignee`, commit, push. Git arbitrates double-claims.
- **Archive on done.** Move to `tasks/done/`, and promote any durable gotcha into the relevant
  skill so the lesson outlives the task.
