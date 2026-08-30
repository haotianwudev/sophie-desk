# Working in this repo

If you're an agent (agy, Claude Code, or anything else) starting a session anywhere in
`sophie-desk`: read this first, then **`.agents/skills/sophie-desk/SKILL.md`** for the full
conventions before touching any task, probe, or supervisor file. This file is the short
version; that one is the source of truth.

## The loop, in three steps

1. **Claim** — find your task in `tasks/*.md` (or the one you were just pointed at). Set
   `status: active`, commit, push. That push *is* the claim.
2. **Work** — follow its `## Goal` / `## Plan`. Append to `## Decision log` as you go (dated
   entries, newest last). Never hand-edit `progress`, `probe_status`, or `updated` if the task
   has a `probe` set — those belong to the supervisor.
3. **Close** — fill in `## Result` (a pointer: a study tag, a commit SHA, a file path — never
   a copy of numbers that live elsewhere and would go stale), set `outcome` and `artifacts` in
   frontmatter, set `status: done`, move the file to `tasks/done/`. Commit, push.

## Two hard rules

- **Never touch a task whose `gate:` field is set** without the human explicitly telling you
  to proceed. A gate means a human decision is required before this is "done" — it exists
  specifically because a wrong call here (an overfit backtest, a leaked-data result) is
  expensive and silent, not because of process for its own sake.
- **Frontmatter stays flat YAML** — plain scalars, no nested structures. A value that needs
  quoting (a path with spaces, say) must be valid on its own; don't assume a lenient parser
  will forgive it. This has broken things for real once already.

## Where things are

- `sophie/work-model.md` — the whole design, in plain English, if you want the *why*.
- `Runbook.md` — exact commands for recurring operations.
- `supervisor/README.md` — what the automated supervisor does (and doesn't).
- `papers/` — the research paper library. `Papers.md` is the live board (by relevance, by
  area, what's missing a deep summary); `FOLLOWUP-CANDIDATES.md` is the todo list of papers
  not yet gathered — check it before searching from scratch. `option-writing/` holds one
  `.pdf` + classified `.md` note per paper already in the library — every note needs the
  frontmatter schema in the skill's "Every paper note needs frontmatter" section, not just
  prose. See the skill's "deep-summarize one paper" pattern if that's the kind of task you've
  been given.

Full detail on all of the above lives in `.agents/skills/sophie-desk/SKILL.md` — this file is
deliberately short; when in doubt, that one wins.
