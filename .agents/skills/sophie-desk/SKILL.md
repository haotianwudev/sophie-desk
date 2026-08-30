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

**If the probe is a bash script, just write `probe: bash <script>` — plain, no quoting.**
A bare `bash` resolves differently depending on who launches the supervisor (from Git Bash
itself it's Git's `bash.exe`; from plain PowerShell or Task Scheduler it can resolve to
Windows' WSL launcher stub instead and fail outright), so the tempting fix is pinning the full
Git Bash path directly in the frontmatter value. **Don't** — a Windows path with spaces,
quoted only around its first token, is not valid YAML (a value starting with `"` must be one
whole quoted scalar), and Dataview uses a *real* YAML parser, unlike this skill's own lenient
one. That exact fix once made a task silently vanish from every Dataview query — `status`
itself failed to parse, not just `probe`. The actual fix lives in `supervisor/run.py`
(`resolve_bash()`): it translates the word `bash` to the real Git Bash binary itself, so the
frontmatter never needs to carry a Windows path at all.

## Closing a task

Fill in the `## Result` section (a pointer — a study tag, a commit SHA, a URL — never a copy of
values that live in Postgres and would go stale on re-run), set `outcome` and `artifacts` in
frontmatter, set `status: done`, then move the file to `tasks/done/`. If anything in its
decision log or gotchas would help someone hit the same problem in an unrelated task later,
promote that specific lesson into the relevant *skill* (not this one) before archiving — the
task disappears into the archive folder, the durable lesson shouldn't disappear with it.

## Worked pattern: deep-summarize one paper

Confirmed working end-to-end 2026-08-30 (dispatch to close, ~75 seconds, unattended) — reuse
this shape rather than redesigning it for the next paper. The library-building pass
(`librarian-test-option-writing`, now archived) leaves each paper with only an abstract-level
note; this pattern asks agy to actually read the PDF and add real depth. Currently 8 papers in
`papers/option-writing/` still only have the shallow note (check each `.md` for a
`## Detailed Summary` heading — its absence means it hasn't had this pass yet).

**Task** (`tasks/summarize-<slug>.md`) — copy the shape, not just the fields:
```yaml
lane: research
assignee: agy
gate:              # empty -- reading/writing a local note is safe for unattended dispatch
probe: bash probes/summarize-<slug>.sh
```
Goal section: name the exact PDF and note path, ask for a new `## Detailed Summary` section
(explicitly: leave the existing `## Summary` untouched), and list what it must cover —
methodology, data/sample period, key quantitative results (real numbers, not vague claims),
and one paragraph connecting it to something concrete already in `sophie-option-research`
(a specific module or notebook, not just "this is relevant").

**Probe** (`probes/summarize-<slug>.sh`) — check for the real thing, not a claim:
```bash
NOTE="papers/option-writing/<slug>.md"
if grep -q "## Detailed Summary" "$NOTE"; then
  words=$(sed -n '/## Detailed Summary/,$p' "$NOTE" | wc -w)
  [ "$words" -ge 80 ] && echo "OK Detailed Summary present, ${words} words" \
                      || echo "RUN Detailed Summary section exists but thin (${words} words)"
else
  echo "RUN no Detailed Summary section yet"
fi
exit 0
```

The 80-word floor is a cheap sanity check, not a quality bar — it exists to catch a task that
added a heading with a one-line placeholder under it, not to certify the summary is actually
good. Read the result yourself before trusting it's genuinely useful.

## Working with the supervisor

`supervisor/run.py` measures and reports, and — confirmed working live, twice —
**auto-dispatches any `status: queued, assignee: agy` task with no `gate` set**
to agy's real terminal CLI (`agy.exe -p`, not the "Antigravity IDE" GUI app,
which opens a window and is the wrong thing — learned that live too). It
never advances a gate or writes outside this repo. Full design in
`supervisor/README.md`; exact commands (check-if-running, relaunch,
confirm-it-came-back-up) in `Runbook.md`'s supervisor section — use those,
don't improvise new ones.

**If you're setting a task's `gate:` field, understand what it actually buys you here**:
dispatch's *only* check before handing a task to an unattended agy session is "does this
task have a gate." Get the field right, or an auto-dispatched task runs with
`--dangerously-skip-permissions` and no human in the loop at all.

**Three things that have actually gone wrong once each, worth not repeating:**

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
- **agy has (at least) two different launchers and only one of them is right for dispatch.**
  `antigravity-ide.exe chat -m agent` looks like a CLI but opens a full GUI window — it works,
  but it's not what "terminal" means here. The actual headless equivalent of Claude Code's
  `-p` flag is a completely separate binary at
  `C:\Users\lswht\AppData\Local\agy\bin\agy.exe`. If agy's behavior ever needs touching again,
  confirm which binary is in play before assuming either one.

## What this skill is not

Not a place to track what's currently blocked, running, or done — that's `Desk.md` (Obsidian)
or `tasks/*.md` directly (anywhere else). Not a place for the reasoning behind the lane/gate
design — that's `sophie/work-model.md`. This skill only covers *how to act* inside this repo
without breaking its conventions.
