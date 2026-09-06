# tasks

One row per `tasks/*.md` and `tasks/done/*.md` file — the task board `Desk.md` renders. This
is the table that let `Desk.md` drop Dataview (2026-09-05): every section on that page is now
a `sqlite-query` block against this table instead of a live `FROM "tasks"` query.

**Not live** — unlike the old Dataview board, this only reflects reality after a rebuild. The
supervisor rebuilds it automatically on every tick that changes something (see
[Runbook.md](../../Runbook.md)'s supervisor section), so it's normally at most ~30 minutes
stale while the loop is running. A manual edit outside the supervisor (claiming a task by
hand, editing prose) needs an explicit `python build_index.py` before `Desk.md` reflects it.

## Columns

Mirrors `templates/task.md`'s frontmatter exactly, plus two computed fields.

| Column | Type | Notes |
|---|---|---|
| `id` | TEXT (primary key) | |
| `title` | TEXT | |
| `lane` | TEXT | `content` / `research` / `platform` |
| `status` | TEXT | `queued` / `active` / `blocked` / `gate` / `done` |
| `assignee` | TEXT | `claude` / `agy` / `either` / `none` |
| `gate` | TEXT | `g1` / `g2` / `g3` / empty |
| `repo` | TEXT | |
| `blocker` | TEXT | |
| `next` | TEXT | |
| `probe` | TEXT | the exact probe command |
| `progress` | TEXT | supervisor-written, never hand-edited |
| `probe_status` | TEXT | `OK` / `RUN` / `STALL` / `ERROR` |
| `stall_flag` | TEXT | non-empty when `status: active` with no real commit in 12+ minutes |
| `outcome` | TEXT | one line, filled on close |
| `artifacts` | TEXT | commits, URLs, study tags |
| `created` | TEXT | |
| `updated` | TEXT | |
| `in_done` | INTEGER | 1 if the file lives in `tasks/done/`, else 0 — this is what "Recently finished" filters on |
| `file_path` | TEXT | path relative to the workspace root |

**Parsed with a lenient line-based reader, not real YAML** — a task's `progress`/`blocker`/
`outcome` routinely holds raw probe-error text with unquoted colons
(`ERROR: CreateProcessCommon:640: ...`), which breaks a real YAML parser. Confirmed live: 8 of
24 task files failed `yaml.safe_load` before this was fixed. Mirrors
`sophie-desk/supervisor/run.py`'s own parser for exactly the same reason.

## Example queries

```sql
-- Desk.md's "Needs you"
SELECT id, lane,
       CASE WHEN COALESCE(stall_flag,'') <> '' THEN 'stalled: ' || stall_flag
            WHEN COALESCE(gate,'') <> '' THEN 'gate ' || gate
            ELSE 'blocked' END AS why
FROM tasks
WHERE in_done = 0 AND (status = 'blocked' OR status = 'gate' OR COALESCE(stall_flag,'') <> '');

-- WIP by lane (limits: content 2 / research 1 / platform 1)
SELECT lane, count(*) FROM tasks WHERE in_done = 0 AND status IN ('active','blocked') GROUP BY lane;

-- everything closed this week, most recent first
SELECT id, outcome, updated FROM tasks WHERE in_done = 1 ORDER BY updated DESC LIMIT 20;
```
