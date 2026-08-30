---
name: sophie-desk
description: Operating conventions for the sophie-desk control plane (tasks, probes, the supervisor). Read this before creating, claiming, updating, or closing any task, or before touching anything under supervisor/. Shared with agy — this is the one skill both workers must follow the same way.
argument-hint: [optional: what you're doing -- "add a task", "add a probe", "check status", "relaunch supervisor"]
allowed-tools: [Read, Bash, PowerShell, Glob, Grep, Edit, Write]
---

# sophie-desk — operating conventions

The user invoked this with: $ARGUMENTS. If a specific action was named, jump to that
section; otherwise read the whole thing once before touching any file here.

Repo: `F:\workspace\sophie-desk` (GitHub: haotianwudev/sophie-desk, **public**). It is both a
git repo and an Obsidian vault — the same files render as a live board in Obsidian and as plain
markdown on GitHub. This skill is the contract; the actual content lives in a few files this
skill only orients you to, so read those directly rather than expecting this to duplicate them:

- **`sophie/work-model.md`** — the whole design, in plain English. Read this first if you're
  new to why any of this exists (lanes, gates, routing, WIP limits).
- **`Runbook.md`** — exact commands for recurring operations (relaunch the supervisor, restart
  the backfill, launch dev servers). Check here before improvising a command.
- **`supervisor/README.md`** — what the supervisor does and deliberately does not do.
- **`Skills.md`** — the full catalogue of Sophie-platform skills, classified by role.

## The one rule that matters most

**A task's `progress`, `probe_status`, and `updated` fields belong to the supervisor if that
task has a `probe` set. Never hand-edit them.** Everything else in a task file — the prose,
the plan, the decision log, `status`, `assignee`, `next`, `outcome` — is yours. If you find
yourself wanting to write a number into `progress`, that's the signal to re-run the probe
instead (`bash probes/<name>.sh`, or `python supervisor/run.py --once` to refresh every task
at once), not to estimate.

## Creating a task

Copy `templates/task.md` into `tasks/<id>.md`. Fill in `id`, `title`, `lane`
(`content`/`research`/`platform`), `repo`, `status` (usually `queued`), `assignee`
(`claude`/`agy`/`ollama`/`either`/`none`), and `gate` if this needs a human sign-off before it
can be called done (see `sophie/work-model.md` for what a gate is). Leave `probe` as `none`
unless you're also writing one (see below). Commit it — creating a task is itself a commit,
same as claiming one.

**Frontmatter must stay flat** — plain scalars, no nested YAML, no lists-of-objects. Dataview
(the Obsidian plugin that renders `Desk.md`) reads it literally; anything nested breaks the
board silently rather than erroring.

## Claiming a task

Edit its frontmatter: set `status: active` and `assignee:` to whoever's taking it. Commit and
push. **The push is the claim** — if two workers edit the same task at the same moment, git
refuses the second push instead of silently overwriting either one, so a collision surfaces
immediately rather than getting lost. If you hit that, don't force-push past it — re-read the
version that won, and re-apply your change on top of it.

## Writing a probe

A probe is a contract, not a script: **read-only**, measures something real (file counts, a
log's mtime, a row count — never a status message or a "task completed" notification, both of
which have lied on this exact repo's own history), and prints exactly one line ending in:

```
<OK|RUN|STALL|ERROR> <short human-readable measurement>
```

Always exit 0 — a probe reports, it never fails the caller. Put it in `probes/<task-id>.sh`
(or `.ps1`/`.py`, doesn't matter, as long as it's directly runnable), and point the task's
`probe:` field at the exact command to run it. See `probes/spx-option-backfill.sh` for a
working example — it counts real files on disk and checks a log's actual age rather than
trusting either the log's own text or a prior "complete" claim.

**If the probe is a bash script, never write `probe: bash <script>`.** A bare `bash` resolves
differently depending on who launches the supervisor — from Git Bash itself it's Git's
`bash.exe`, but from plain PowerShell or Task Scheduler it can resolve to Windows' WSL launcher
stub instead (`C:\Windows\System32\bash.exe`), which fails outright if WSL isn't set up. Hit
live: a task's `progress` field got overwritten with a raw WSL error message instead of a real
measurement, the moment the supervisor started running from a plain PowerShell window instead
of Git Bash. Write the full path instead:
```
probe: "C:\Program Files\Git\bin\bash.exe" probes/<task-id>.sh
```

## Closing a task

Fill in the `## Result` section (a pointer — a study tag, a commit SHA, a URL — never a copy of
values that live in Postgres and would go stale on re-run), set `outcome` and `artifacts` in
frontmatter, set `status: done`, then move the file to `tasks/done/`. If anything in its
decision log or gotchas would help someone hit the same problem in an unrelated task later,
promote that specific lesson into the relevant *skill* (not this one) before archiving — the
task disappears into the archive folder, the durable lesson shouldn't disappear with it.

## Working with the supervisor

`supervisor/run.py` measures and reports; it never dispatches work, never advances a gate,
never writes outside this repo. Full design in `supervisor/README.md`; exact commands
(check-if-running, relaunch, confirm-it-came-back-up) in `Runbook.md`'s supervisor section —
use those, don't improvise new ones.

**Two things that have actually gone wrong once each, worth not repeating:**

- **On Windows, verify a process is dead with `tasklist`/`Get-Process`, not bash's own
  `kill`/`timeout` exit code.** A test loop survived two kill attempts from Git Bash and kept
  running — and auto-committing — for about ten minutes before anyone noticed. Same class of
  bug `spx-option-backfill` already hit for a different script. Kill with
  `taskkill //F //PID <pid>` (bash) or `Stop-Process -Id <pid> -Force` (PowerShell), then
  confirm with a fresh process listing before assuming it's gone.
- **A script printing success is not success.** `register-task.ps1` printed "Registered" after
  `Register-ScheduledTask` had actually failed with Access Denied, because nothing checked the
  result. Fixed there by calling `Get-ScheduledTask` afterward and refusing to claim success
  unless it's independently confirmed — apply the same instinct anywhere else a command's own
  exit message is the only evidence something worked.

## What this skill is not

Not a place to track what's currently blocked, running, or done — that's `Desk.md` (Obsidian)
or `tasks/*.md` directly (anywhere else). Not a place for the reasoning behind the lane/gate
design — that's `sophie/work-model.md`. This skill only covers *how to act* inside this repo
without breaking its conventions.
