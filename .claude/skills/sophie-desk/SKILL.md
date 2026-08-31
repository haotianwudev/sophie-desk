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

**This file lives in two places on purpose** — `.agents/skills/sophie-desk/SKILL.md` (canonical,
edit this one) and `.claude/skills/sophie-desk/SKILL.md` (a generated mirror, never hand-edit).
Claude Code's own project-skill discovery reads `.claude/skills/`, not `.agents/skills/` — this
skill was invisible to Claude Code until the mirror was added, confirmed by checking a working
example elsewhere (`ai-stock-suggestion-client`'s real skills live in `.claude/skills/`; its
`.agents/skills.json` is just a pointer config, not skill content). Whichever location agy
reads (if any — never actually confirmed; every dispatch so far has told it the exact file path
explicitly rather than relying on auto-discovery), the `.agents/` copy stays for that. After
editing this file, run `python scripts/gen_skills.py` to re-sync the mirror — it's a plain
file copy regenerated on every run, not a symlink or hard link (a hard link was tried and
rejected: `git checkout` replaces a file's inode rather than editing it in place, which
silently breaks a hard link with no error — worse than a stale copy, which at least shows up
in a diff). **Also open Claude Code with this repo as the working directory** — directory-
scoped skill discovery needs that regardless of which folder the file lives in.

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

## Capturing an idea you don't want to formalize yet

Not every idea deserves a `tasks/<id>.md` file the moment it occurs to you — writing one means
picking a lane, an assignee, deciding on a gate, maybe a probe, and that's real thinking you may
not want to spend right now (e.g. you're low on budget/tokens for this session but don't want to
lose the idea). For that, `Todo.md` at the repo root is a plain, flat checklist — one line per
idea, no frontmatter, not part of the Dataview board, not touched by the supervisor.

Add a line to `Todo.md` and commit it — that's the whole ritual. When you're ready to actually
work it, promote it into a real task per "Creating a task" below, then delete the line from
`Todo.md`. Never let the same idea live in both places at once; whichever file it's in is the
one source of truth for it at that moment.

## Creating a task

Copy `templates/task.md` into `tasks/<id>.md`. Fill in `id`, `title`, `lane`
(`content`/`research`/`platform`), `repo`, `status` (usually `queued`), `assignee`
(`claude`/`agy`/`either`/`none`), and `gate` if this needs a human sign-off before it
can be called done (see `sophie/work-model.md` for what a gate is). Leave `probe` as `none`
unless you're also writing one (see below). Commit it — creating a task is itself a commit,
same as claiming one.

**`ollama` is never a valid `assignee`.** It has no tool use, no file access, and nothing
dispatches to it the way `dispatch_to_agy()` dispatches to agy — it's a plain text/embeddings
API (`scripts/ollama_call.py generate|embed`, confirmed working against the local server on
`:11434` with `qwen3.5` and `bge-m3`), not a worker. If a task benefits from cheap bulk
skimming or embeddings (triaging many candidate papers, say), say so in its `## Plan` — "use
`scripts/ollama_call.py` for the first pass" — and assign the task itself to `claude` or
`agy`, whoever will actually read the output, decide what matters, and close it out.

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

## Every paper note needs frontmatter — classification, not just prose

24 papers deep, plain-prose notes stopped being scannable — no way to filter by area, sort by
relevance, or find what still needs work without opening every file. Fixed by giving each
paper's own `.md` note in `papers/option-writing/` real frontmatter (retrofitted onto all 24
at once; new papers should just write it directly, no separate retrofit pass going forward):

```yaml
---
title: "<paper title>"
authors: "<comma-separated>"
year: <int>
link: "<url>"
area: <one tag -- vrp-measurement | tail-risk | covered-calls | sizing-risk | cross-asset |
       ml-strategy | hedging-mechanics | market-microstructure | option-returns-anomaly |
       event-risk | vrp-timing | return-dynamics-modeling | (add a new one if none fit --
       this list isn't closed, just what's been needed so far)
relevance: High | Medium | Low         # from its own "Relevance to Personal Trading" section
has_pdf: true | false                  # false = recorded-but-not-downloaded (round 4 convention)
has_detailed_summary: true | false     # true only if it has a real "## Detailed Summary" section
citations_surfaced: <int>              # count under "Notable Citations to Follow Up"
gdoc_id: "<drive doc id>"              # optional -- see "Linking papers to your own Google
                                        # Drive research docs" below. Omit if there's no linked doc.
---
```

**Same flat-YAML rule as tasks** — Dataview needs to actually parse this, not just a lenient
regex; this is exactly the class of thing that broke a task's frontmatter once already. Keep
every value a plain scalar, quote strings that contain a colon or start oddly, never nest.

`papers/Papers.md` is the live board over this frontmatter (parallel to `Desk.md` for tasks) —
by relevance, by area, which papers still lack a deep summary, which are recorded-but-not-downloaded.
Update it (or at least don't break its queries) if the schema above ever gains a field.

## Tracking papers worth fetching later

`papers/FOLLOWUP-CANDIDATES.md` is the todo list — not a library, a backlog. A paper worth
getting but not yet gathered (surfaced via citation-following, or any other way) goes here as
a row, with who surfaced it and why. **A future `librarian-round-N` gathering pass should
check this file first**, before searching from scratch, and remove (or move to "Passed on")
each entry it actually resolves. This exists because a per-paper "Notable Citations to Follow
Up" section (see the review pattern below) is real, useful information, but 24+ of them
scattered across individual notes isn't an actionable todo list — this file is the
consolidated one.

## Linking papers to your own Google Drive research docs

The user runs a lot of ad-hoc Gemini Deep Research sessions and Drive-syncs the results to
`D:\GoogleDrive` (~335 as of 2026-08-30, growing). Each shows up as a `.gdoc` file — **a
172-byte JSON stub** (`{"doc_id": ..., "resource_key": ..., "email": ...}`), not the actual
content; the filename minus extension is the doc's title. Fetching real content needs the
Google Drive MCP connector (`mcp__claude_ai_Google_Drive__*`), which only a Claude Code
session with that connector attached is confirmed to have — **agy has no proven access to it**,
so this splits into two tasks that must not be merged:

- **`tasks/gdocs-index-sync.md`** (assignee `agy`, no gate) — `scripts/sync_gdocs_index.py`
  scans `D:\GoogleDrive` recursively for `.gdoc` stubs (skipping `.tmp.drivedownload` and any
  `*personal*` directory) and writes `gdocs/index.json` (title, doc_id, resource_key, relpath,
  mtime). `scripts/match_gdoc.py "<query>"` ranks index entries against a title by string
  similarity, no network needed. Pure filesystem work — safe for unattended dispatch.
- **`tasks/gdocs-content-link.md`** (assignee `claude`) — the half that actually reads content:
  run the matcher against each paper's `title`, fetch a candidate's real content via the Drive
  connector, **read it before linking** (a plausible title match can still be the wrong doc),
  and only then add `gdoc_id: "<doc_id>"` to that paper's frontmatter. Cached content goes in
  `gdocs/cache/<doc_id>.md`.

**`gdocs/` is gitignored, deliberately** — it holds the user's personal research-session titles
and cached content, and this repo is public. `gdoc_id` on a paper is fine to commit (an opaque
ID reveals nothing on its own); the index and cache that resolve it to a title/content are not.

If this pattern gets reused for other configs later (article/topic configs, say — see
`sophie-add-to-topic`), the index+matcher in `gdocs/` is already general-purpose; only the
linking step (which frontmatter field, which file) is paper-specific.

**First real run (2026-08-30) found zero links, and that's the correct result, not a failure.**
`gdocs-content-link` matched all 24 papers against the 335-doc index; best scores topped out at
0.65 and every one of the top candidates, once actually read, turned out to be the user's own
independent Gemini research on a broad adjacent topic (its own 20-30+ item Works Cited list),
not a write-up *of* any specific library paper. One paper (Feunou-Jahan-Parvar-Okou 2018,
"Downside Variance Risk Premium") turned up as a single citation inside one such doc's
bibliography — a real overlap, but many-to-many (doc cites paper), not what `gdoc_id` means
(doc is about paper). Don't re-run this exact matching pass expecting a different outcome
unless the Drive corpus has grown with genuinely paper-specific sessions since. If a
citation-overlap relationship (as opposed to "this doc is about this paper") becomes worth
tracking, it needs a different field/mechanism than `gdoc_id` — that hasn't been built.

## Worked pattern: deep-summarize one paper

Confirmed working end-to-end multiple times (single-paper dispatch in ~75s; a 12-paper batch
in one task, resumed once after a timeout, in a few minutes total) — reuse this shape rather
than redesigning it for the next paper. A librarian-round-N paper-gathering pass leaves each
paper with only an abstract-level note; this pattern asks agy to actually read the PDF and add
real depth. Find which papers still need it with:
```bash
for f in papers/option-writing/*.md; do grep -q "## Detailed Summary" "$f" || echo "$f"; done
```

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

**Five things that have actually gone wrong, worth not repeating:**

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
- **`tick()` dispatches every matching task in one pass, not just one — and committing a
  second task doesn't hold it back.** Queuing two `assignee: agy` research-lane tasks and
  running one tick launched both simultaneously, as two separate agy processes racing to
  commit/push to the same repo. Harmless that specific time (different files touched), but
  it was luck. `tick()` reads the live filesystem, not git's committed state, so leaving a
  second task uncommitted does *not* prevent dispatch — draft it somewhere outside `tasks/`
  if you genuinely need to hold it back. See Runbook.md's "Dispatching work" for the actual
  one-at-a-time discipline (not yet enforced in code).
- **A 12-step task can legitimately outlast agy's own 5-minute `--print-timeout`.** The
  dispatched session exits cleanly when it hits that wall — no data lost, whatever committed
  already stays committed — but nothing continues it automatically. Fixed by raising the
  supervisor's own dispatch to `--print-timeout 30m`, and by adding stall detection
  (`stall_flag` in a task's own frontmatter, set when `status: active` but no real commit in
  12+ minutes — see `supervisor/run.py`'s `check_stalled_active()`). It only flags, never
  auto-resumes; check `ps -W | grep agy.exe` before assuming a flagged task actually crashed,
  and if it really did, resume with the same dispatch command, told explicitly to check the
  Decision log for what's already done first.

## What this skill is not

Not a place to track what's currently blocked, running, or done — that's `Desk.md` (Obsidian)
or `tasks/*.md` directly (anywhere else). Not a place for the reasoning behind the lane/gate
design — that's `sophie/work-model.md`. This skill only covers *how to act* inside this repo
without breaking its conventions.
