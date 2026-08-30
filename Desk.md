# The Desk

New here? Read [sophie/work-model.md](sophie/work-model.md) first — the whole design, in plain
English, one page. Need to relaunch or restart something? [Runbook.md](Runbook.md). Looking
for the research paper library specifically, not tasks? [papers/Papers.md](papers/Papers.md).

Live board over `tasks/`. Everything here is a query — nothing is hand-maintained.
`progress` and `probe_status` are written by the supervisor after it runs each task's probe;
treat any other field as declared state, not measured state.

---

## Needs you

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS "Task",
  lane AS "Lane",
  choice(stall_flag, "stalled: " + stall_flag, choice(gate, "gate " + gate, "blocked")) AS "Why",
  progress AS "Progress",
  next AS "Next step"
FROM "tasks"
WHERE status = "blocked" OR status = "gate" OR stall_flag
SORT lane ASC
```

## Running

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS "Task",
  lane AS "Lane",
  assignee AS "Who",
  progress AS "Progress",
  updated AS "Updated"
FROM "tasks"
WHERE status = "active"
SORT updated DESC
```

## Queued

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS "Task",
  lane AS "Lane",
  assignee AS "Who",
  next AS "Next step"
FROM "tasks"
WHERE status = "queued"
SORT lane ASC
```

---

## WIP check

Lane limits: **content 2 · research 1 · platform 1**. Over the limit means you have become the queue.

```dataview
TABLE WITHOUT ID
  lane AS "Lane",
  length(rows) AS "In flight"
FROM "tasks"
WHERE status = "active" OR status = "blocked"
GROUP BY lane
```

---

## Recently finished

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS "Task",
  lane AS "Lane",
  outcome AS "Result",
  updated AS "Done"
FROM "tasks/done"
SORT updated DESC
LIMIT 12
```

---

## Pipeline

Written by the supervisor from Neon + Cloud Scheduler — the one section here that survives
the workstation being asleep, because it is fetched rather than probed.

```dataview
TABLE WITHOUT ID
  table_name AS "Table",
  schedule AS "Clock",
  last_row AS "Latest row",
  note AS "Note"
FROM "notes/pipeline"
SORT table_name ASC
```

> [!info] Expected staleness is not failure
> `vol_regime_data` runs a business day behind by design — `vol-regime-etl` passes an exclusive
> `end` to yfinance, so each run captures through the *previous* close. It is self-healing.
> `sophie-pipeline-upload` is a weekly Windows task and needs the workstation awake.
