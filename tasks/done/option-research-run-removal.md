---
id: option-research-run-removal
title: Let the research viewer remove and delete runs that are not needed
lane: platform
status: done
assignee: claude
gate:
repo: sophie-option-research
blocker:
next:
probe: none
progress:
probe_status:
stall_flag:
outcome: runs can be removed reversibly from the viewer, and deleted permanently as a separate confirmed step
artifacts: sophie-option-research src/lab/api/removal.py, scripts/check_removal.py, web/scripts/check-removal-ui.mjs, skill option-research-viewer
created: 2026-09-20
updated: 2026-09-20
---

## Goal

The user asked for remove/delete functionality "for the run", meaning runs that are not needed. I read that as being
able to get rid of unwanted runs from the viewer. This reverses the earlier decision that the viewer is read-only,
so it was built to be safe by default and the reversal is recorded here.

## Plan

1. Make the default action lossless and reversible.
2. Make permanent deletion a separate, deliberate, recoverable step.
3. Protect the mutating routes from other websites, since the API has no auth.
4. Test against a scratch copy, then in a real browser.

## Decision log

- 2026-09-20 — Decision on the earlier "read-only" rule: the viewer was read-only by design so it could not race a
  notebook writing the store or lose research. The user explicitly asked for delete, so that rule is relaxed, not
  ignored. The default action, Remove, only writes a sidecar file (`results/removed_runs.json`) and hides the run;
  `runs.parquet` and the trade log are untouched, so it cannot race a notebook and cannot lose data.
- 2026-09-20 — Permanent delete is a second step, allowed only for a run that is already removed and only with the
  run's hash typed as confirmation. It backs up `runs.parquet`, rewrites it atomically, moves the trade log to
  `trades/_deleted/` instead of unlinking it, and refuses (409) if the file changed while it worked, because the
  store's lock only covers threads. It does not touch Postgres. Every action is appended to an audit log. No gate was
  set: this is local and recoverable, unlike a change to published research.
- 2026-09-20 — Browser safety. The API has no auth. A web page open in the same browser can send a "simple"
  cross-site POST to 127.0.0.1 without any CORS preflight (CORS stops the response being read, not the request
  being sent). So the three mutating routes require a custom header plus an allowed Origin, checked on the server.
  Verified in real Chrome: a POST from another origin is blocked by the preflight, and a "simple" one that is sent is
  refused by the server.
- 2026-09-20 — A corrupt sidecar is treated as an error, not as "nothing removed", because the latter would silently
  un-hide every removed run.
- 2026-09-20 — Testing. 40 checks against a scratch copy of the store, ending with proof that the real store was
  untouched. They passed first time, so they were mutation-tested: disabling the mid-write refusal, or the "must be
  removed first" rule, makes them fail (3 and 4 checks respectively). Then 21 checks driving the UI in real headless
  Chrome over the DevTools protocol against a scratch API (dialogs, typed-hash gate, restore, delete, cross-site).
  A live remove and restore on the real store confirmed the same behaviour and left it unchanged.
- 2026-09-20 — Ambiguity handled by default, not by asking: "for the run not needed" could mean several things.
  Reversible removal satisfies every reading, and the destructive step needs an explicit typed confirmation.
  Bulk selection (remove several runs at once) was not built; removal is one run at a time from its page.

## Result

- Code in `sophie-option-research`: `src/lab/api/removal.py`, guarded routes in `src/lab/api/app.py`, hiding in
  `src/lab/api/readmodel.py`; UI: the Remove button on a run page and a `/removed` page.
- Tests: `scripts/check_removal.py` and `web/scripts/check-removal-ui.mjs` (scratch store only, never the real one).
- Operating notes, the safety reasoning and the setup for the browser test are in the `option-research-viewer` skill.
- Not done: removing several runs at once; nothing was pushed for this change.
