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
3. **Auto-dispatches to agy.** Any task with `status: queued`, `assignee: agy`,
   and no `gate` set gets claimed (`status: active`) and handed to agy's real
   terminal CLI — `agy.exe -p "<brief>" --add-dir <vault> --dangerously-skip-permissions`
   — launched via `Popen` so it runs in the background without blocking this
   tick. Confirmed live end-to-end twice: agy read the brief, read the task
   file, did the actual work, updated its own Decision log/Result, archived
   itself to `tasks/done/`, committed, and pushed — all with nobody watching.
4. Builds `supervisor/status.json` — task count, which ones need you
   (`status: blocked` or `status: gate`), which probes came back `STALL`.
5. Commits and pushes, but only if a probe or a dispatch-claim actually
   changed something. A quiet tick with nothing new produces no commit.
6. Logs a line the moment a task newly enters "needs you" — see the gap
   below before assuming that reaches you anywhere.

## The one thing worth being deliberate about: `--dangerously-skip-permissions`

Automatic dispatch only works at all because of this flag — without it, agy's
`-p` mode would stall forever waiting for a permission prompt nobody is there
to answer. The consequence is real: **an auto-dispatched task runs with no
per-action approval gate.** This is why the `sophie-desk` skill's `gate`
check matters more than ever — a task that should require your sign-off
before anything happens must carry a real `gate:` value, because dispatch's
only defense against launching something it shouldn't is refusing to touch
any task that has one. Never assign a `gate`-bearing task to `agy` and expect
the supervisor to leave it alone by luck; it leaves it alone because the
code explicitly checks for this, on purpose.

**It also does not do these, still:**

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
existence. **Safe to kill any time, including a hard kill.** Verified live: a graceful
Ctrl+C cleans up the pid file immediately, but a `Stop-Process`/`kill`/Task Scheduler stop
(SIGTERM, or Windows' `TerminateProcess`) skips Python's cleanup entirely and leaves the
pid file behind with a now-dead pid in it. That's fine — the lock check asks the real
Windows process table whether that pid is still alive, not just whether the file exists,
so the very next start correctly ignores the stale file and takes over. Confirmed by
killing a running loop and immediately starting a fresh one against the same vault.

**One caveat found the hard way, testing this from Git Bash on Windows**: bash's own `kill`
and `timeout` don't reliably reach a Windows-native `python.exe` launched as a background job
— the same class of gotcha `spx-option-backfill` already hit for a completely different
script. A test loop survived two separate `kill`/`timeout` attempts and kept ticking,
unnoticed, for about ten minutes before a routine `git log` turned up a commit nobody had
made on purpose. Confirm a supervisor process is actually gone with `tasklist`/`Get-Process`,
and kill it with `taskkill //F //PID <pid>` (or `Stop-Process -Id <pid> -Force`) — not bash
`kill`.

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
