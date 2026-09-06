# The Desk

New here? Read [sophie/work-model.md](sophie/work-model.md) first — the whole design, in plain
English, one page. Need to relaunch or restart something? [Runbook.md](Runbook.md). Looking
for the research paper library specifically, not tasks? [papers/Papers.md](papers/Papers.md).
Got an idea but no budget to formalize it right now? [Todo.md](Todo.md).

Live board over `tasks/`, rendered via [papers/paper-index/papers.db](papers/paper-index/README.md)
(the `sqlite-query` blocks below need the **SQLite Explorer** Obsidian plugin — see
[papers/db-schema/README.md](papers/db-schema/README.md)). **Rebuild the index before trusting
this page** — unlike the old Dataview boards, these blocks aren't live against the markdown;
run `python build_index.py` in `sophie-pipeline/paper-index/` any time a task file changes
(the supervisor's own tick does this for you if it's running — see Runbook.md).
`progress` and `probe_status` are written by the supervisor after it runs each task's probe;
treat any other field as declared state, not measured state.

---

## Needs you

```sqlite-query
source: /papers/paper-index/papers.db
sql: |
  SELECT id AS "Task", lane AS "Lane",
         CASE WHEN COALESCE(stall_flag, '') <> '' THEN 'stalled: ' || stall_flag
              WHEN COALESCE(gate, '') <> '' THEN 'gate ' || gate
              ELSE 'blocked' END AS "Why",
         progress AS "Progress", next AS "Next step"
  FROM tasks
  WHERE in_done = 0
    AND (status = 'blocked' OR status = 'gate' OR COALESCE(stall_flag, '') <> '')
  ORDER BY lane ASC
```

## Running

```sqlite-query
source: /papers/paper-index/papers.db
sql: |
  SELECT id AS "Task", lane AS "Lane", assignee AS "Who",
         progress AS "Progress", updated AS "Updated"
  FROM tasks
  WHERE in_done = 0 AND status = 'active'
  ORDER BY updated DESC
```

## Queued

```sqlite-query
source: /papers/paper-index/papers.db
sql: |
  SELECT id AS "Task", lane AS "Lane", assignee AS "Who", next AS "Next step"
  FROM tasks
  WHERE in_done = 0 AND status = 'queued'
  ORDER BY lane ASC
```

---

## WIP check

Lane limits: **content 2 · research 1 · platform 1**. Over the limit means you have become the queue.

```sqlite-query
source: /papers/paper-index/papers.db
sql: |
  SELECT lane AS "Lane", count(*) AS "In flight"
  FROM tasks
  WHERE in_done = 0 AND (status = 'active' OR status = 'blocked')
  GROUP BY lane
```

---

## Recently finished

```sqlite-query
source: /papers/paper-index/papers.db
sql: |
  SELECT id AS "Task", lane AS "Lane", outcome AS "Result", updated AS "Done"
  FROM tasks
  WHERE in_done = 1
  ORDER BY updated DESC
  LIMIT 12
```

---

## Pipeline

Written by the supervisor from Neon + Cloud Scheduler — the one section here that survives
the workstation being asleep, because it is fetched rather than probed.

**Not implemented yet** — `notes/pipeline/` doesn't exist on disk as of 2026-09-05, so this
renders empty. The `pipeline` table is already wired into the index (see
[papers/db-schema/README.md](papers/db-schema/README.md)); it'll populate as soon as the
supervisor starts writing that folder.

```sqlite-query
source: /papers/paper-index/papers.db
sql: |
  SELECT table_name AS "Table", schedule AS "Clock", last_row AS "Latest row", note AS "Note"
  FROM pipeline
  ORDER BY table_name ASC
```

> [!info] Expected staleness is not failure
> `vol_regime_data` runs a business day behind by design — `vol-regime-etl` passes an exclusive
> `end` to yfinance, so each run captures through the *previous* close. It is self-healing.
> `sophie-pipeline-upload` is a weekly Windows task and needs the workstation awake.
