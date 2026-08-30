# The supervisor

A dumb, restartable loop, modeled directly on
`sophie-pipeline/data/autorun_download.sh` — the script that already proved
this pattern out the hard way, across a week of stuck downloads and wedged
Terminal connections. Same idea, generalized past one job: check the real
state of every task, write down what's measured, commit it, repeat.

## What it actually does

Each tick (`supervisor/run.py`):

1. Reads every file in `tasks/*.md`.
2. For any task with a `probe` set, runs it and writes the result straight
   into **that task's own frontmatter** — `progress`, `probe_status`,
   `updated`. Nothing else in the file is touched; the surrounding prose,
   decision log, and plan are yours, not the supervisor's.
3. Builds `supervisor/status.json` — task count, which ones need you
   (`status: blocked` or `status: gate`), which probes came back `STALL`.
4. Commits and pushes, but only if a probe actually changed something. A
   quiet tick with nothing new produces no commit.
5. Logs a line the moment a task newly enters "needs you" — see the gap
   below before assuming that reaches you anywhere.

## What it deliberately does not do

- **It never dispatches work to agy.** Handing a queued task to another AI
  worker means actually invoking it headlessly, and this repo doesn't know
  what agy's CLI or API looks like. Building that means fabricating an
  invocation that might not exist. So today the supervisor only *measures
  and reports* — claiming a task is still `/desk-next`-style, a human or an
  agent editing the frontmatter and pushing. If agy has a scriptable
  entrypoint, this is exactly where it plugs in next.
- **It never advances a gate or promotes a study.** `status: gate` tasks
  stay exactly as blocked as they were — that's a human decision by design,
  see `sophie/work-model.md`.
- **It never touches Neon, Supabase, or any repo but this one.** A probe is
  read-only by contract; the supervisor trusts that contract rather than
  sandboxing it, which is also why a probe script must never be anything
  but a measurement.
- **It doesn't actually send you a notification yet.** The WARN log line in
  step 5 is real, but nothing pushes it anywhere — no email, no Slack, no
  phone alert. Right now, "did anything need me today" means either reading
  `supervisor/supervisor.log`, opening `Desk.md` in Obsidian, or asking the
  chat agent once it can read this vault. Wiring an actual channel is a
  clear next step, deliberately left undone rather than guessed at.

## Running it

```bash
# one tick, real writes + commit + push
python supervisor/run.py --once

# one tick, print what would happen, touch nothing
python supervisor/run.py --once --dry-run

# forever, ticking every 30 minutes (the mode Task Scheduler runs)
python supervisor/run.py --loop
python supervisor/run.py --loop --interval 900   # every 15 min instead
```

It refuses to run a second `--loop` against the same vault — `supervisor/supervisor.pid`
is the lock, checked against the real Windows process table, not just the file's
existence. Safe to kill any time: nothing lives in memory that isn't already on disk.

## Installing it to start at logon

```powershell
.\supervisor\register-task.ps1
```

Registers a Windows Scheduled Task named `sophie-desk-supervisor`: starts at
logon, restarts up to 5 times on failure. See **Runbook.md** for the
check-before-you-touch-it / relaunch / confirm-it-came-back-up commands —
that's the day-to-day entry point, this file is the design.

## Files this owns

| File | What it is | Committed? |
|---|---|---|
| `supervisor/status.json` | Last tick's summary — needs-you list, stalled probes | yes — this is the point, visible from the phone |
| `supervisor/supervisor.log` | Full tick history | no — local, high-churn |
| `supervisor/supervisor.pid` | Singleton lock for `--loop` | no — machine-local |

Task files under `tasks/*.md` get their `progress` / `probe_status` /
`updated` fields overwritten by the supervisor — per `templates/task.md`,
never hand-edit those three fields, they're the whole reason a probe exists.
