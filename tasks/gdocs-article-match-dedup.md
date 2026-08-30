---
id: gdocs-article-match-dedup
title: Match Drive research docs to Sophie article slugs, and report duplicate docs
lane: content
status: active
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-article-match-dedup.sh
progress: missing: scripts/match_articles_gdocs.py scripts/find_gdoc_duplicates.py
probe_status: RUN
stall_flag: 
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

Follow-up to `tasks/done/gdocs-index-sync.md` (built `gdocs/index.json`, 335 Drive docs, and
`scripts/match_gdoc.py`). That effort targeted `papers/option-writing/` and found no confident
links there. This task targets a different, better-fitting config: Sophie's own published
articles, which are far more likely to be 1:1 with the user's Gemini Deep Research sessions
(many articles are themselves written *from* a deep-research doc).

**Read-only investigation only — do not rename, delete, or edit anything in `D:\GoogleDrive`,
and do not edit any file under `ai-stock-suggestion-client/`.** Output goes to two new
gitignored report files under `gdocs/`. The user will review both reports before anyone touches
real files; that's a separate follow-up task, not this one.

Two independent pieces:

### Part A — match articles to Drive docs

Article configs live in `F:/workspace/ai-stock-suggestion-client/src/data/articles/*.ts`
(files named `{year}-q{quarter}.ts`, e.g. `2026-q3.ts` — skip `index.ts` and `types.ts`, those
aren't article data). Each article object has at least `title`, `slug`, and sometimes an
existing `googleDoc: "https://docs.google.com/document/d/e/..."` field (a published-doc URL —
**already a confirmed link, not something to re-derive**).

1. Parse every article's `title`, `slug`, and whether `googleDoc` is already present (true/false)
   from all `src/data/articles/{year}-q{n}.ts` files. A simple regex per object is fine
   (`title:\s*"((?:[^"\\]|\\.)*)"`, `slug:\s*"([^"]*)"`, and a check for a `googleDoc:` key in
   the same object) — this doesn't need a real TS/AST parser, the file is a plain array literal.
2. For every article, score it against every entry in `gdocs/index.json` the same way
   `scripts/match_gdoc.py` does (reuse `difflib.SequenceMatcher` — either import the function
   from that script or duplicate the ~3 lines, whichever is cleaner).
3. Write `gdocs/article-matches.md`: a markdown table, one row per article, columns `Score |
   Article Slug | Article Title | Has googleDoc? | Best Gdoc Candidate | Candidate Doc ID`,
   **sorted by score descending** so the strongest candidates are at the top. Include every
   article (even ones that already have `googleDoc` — mark those clearly, e.g. `Has googleDoc?`
   = `yes`, so the reviewer can see at a glance which rows are "already linked" vs "gap to
   review"). Don't filter out low scores — the user is reviewing this by eye, sorted order does
   the filtering for them.

### Part B — duplicate Drive docs

Several `.gdoc` titles in `gdocs/index.json` carry a trailing ` (1)`, ` (2)` etc. — the same
research topic saved more than once, possibly with different content each time (re-run at a
later date), possibly a true accidental duplicate. **Do not assume which — just report the
groups for the user to judge.**

1. Group `gdocs/index.json` entries by a normalized key: strip a trailing `\s*\(\d+\)$` suffix
   (case-insensitive), collapse whitespace, lowercase.
2. Keep only groups with 2+ members.
3. Write `gdocs/duplicates.md`: for each group, the normalized title as a heading, then a table
   of its members — `Title (as saved) | Doc ID | Modified` (mtime formatted as a readable date,
   not a raw epoch float) — **sorted newest-first within the group**. Sort the groups themselves
   by member count descending, then alphabetically.

## Plan

1. Write a script, `scripts/match_articles_gdocs.py`, that does Part A end to end (parse
   articles → score against the index → write `gdocs/article-matches.md`).
2. Write a script, `scripts/find_gdoc_duplicates.py`, that does Part B end to end (group →
   write `gdocs/duplicates.md`).
3. Run both for real, sanity-check the outputs make sense (spot check: a few articles you
   recognize as "obviously deep-research-based" should show up with a plausible high-scoring
   candidate; a few duplicate groups should look like genuine repeated research, not noise).
4. Commit the two new scripts (not the gitignored `gdocs/*.md` reports they produce — same rule
   as the sibling task: check `.gitignore` covers `gdocs/` before committing, don't force it in
   if `git status` shows it untracked-but-not-ignored).

## Decision log

- **2026-08-30** — Scoped to matching + dedup-reporting only, explicitly excluding any rename/
  delete on `D:\GoogleDrive` — that syncs to the user's real Google account and needs their
  review of the actual report before anyone touches it, not a judgment call for an unattended
  dispatch to make.

## Result

<!-- filled by /desk-log on completion -->
