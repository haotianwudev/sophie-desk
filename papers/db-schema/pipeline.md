# pipeline

One row per `notes/pipeline/*.md` — supervisor-written pipeline health (fetched from Neon +
Cloud Scheduler, meant to survive the workstation being asleep since it's fetched rather than
probed like a task).

**Not implemented yet as of 2026-09-05** — `notes/pipeline/` doesn't exist on disk, so this
table is always empty. Not used by `Desk.md` (that section stays on a live Dataview
`FROM "notes/pipeline"` query, same as the rest of that board), but wired up here for anything
that wants to query pipeline health without opening Obsidian — needs zero further work once
the supervisor actually starts writing that folder, just start writing `notes/pipeline/*.md`
files with this frontmatter and rebuild.

## Columns

| Column | Type | Notes |
|---|---|---|
| `table_name` | TEXT (primary key) | the Postgres/Neon table this row reports on |
| `schedule` | TEXT | the Cloud Scheduler cron/cadence |
| `last_row` | TEXT | latest row's timestamp or identifying value |
| `note` | TEXT | free text — e.g. explaining expected staleness |

Parsed with the same lenient line-based reader as [tasks](tasks.md), for the same reason
(`note` is free text and may contain colons).

## Example query

```sql
SELECT table_name, schedule, last_row, note FROM pipeline ORDER BY table_name ASC;
```
