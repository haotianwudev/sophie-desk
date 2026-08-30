---
id: gdocs-content-link
title: Link papers to matching Drive research docs and cache their content
lane: research
status: queued
assignee: claude
gate:
repo: sophie-desk
blocker: Depends on gdocs-index-sync landing first (needs gdocs/index.json + scripts/match_gdoc.py)
next: Once gdocs-index-sync is done, run match_gdoc.py against each paper title in papers/option-writing/*.md
probe: none
progress:
probe_status:
stall_flag:
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

`gdocs-index-sync` builds a title→doc_id index of the user's ~335 Gemini Deep Research docs in
`D:\GoogleDrive`, plus a matcher script. This task is the half that actually reads content: for
papers in `papers/option-writing/*.md` that have a confident matching Drive doc, fetch that
doc's real content (via the `mcp__claude_ai_Google_Drive__*` connector tools already attached
to this Claude Code session — `read_file_content` or `download_file_content`, keyed by
`doc_id`) and cache it locally so future reads are a plain `Read` call, not a fresh API round
trip.

**Why this can't be agy's job**: agy has no proven access to this session's Google Drive
connector. Confirmed only Claude Code sessions with that connector attached can fetch content
today — see the sibling task's Decision log.

**Judgment call, not mechanical**: `match_gdoc.py`'s ranking is approximate (title-string
similarity between a formal academic paper title and an ad-hoc Gemini session title). Do not
auto-link every top match — read the actual candidate content before linking; a plausible
string match can still be the wrong document. Only link when the fetched content is genuinely
about that paper.

## Plan

1. For each `papers/option-writing/*.md`, read its `title` frontmatter field and run
   `python scripts/match_gdoc.py "<title>"`.
2. For any match above roughly 0.5 similarity, fetch that doc's content via the Google Drive
   connector tools and skim it — confirm it's actually about the paper (not just a title
   coincidence) before linking.
3. On a confirmed match:
   - Add `gdoc_id: "<doc_id>"` to that paper's frontmatter (keep it a flat scalar — same
     Dataview-parsing rule as everything else in this repo).
   - Cache the fetched content under `gdocs/cache/<doc_id>.md` (this directory is gitignored —
     personal content, public repo). Include a small header: source title, doc_id, fetch date.
   - **Do not overwrite the paper's own `## Summary` or `## Detailed Summary` sections** — the
     linked Drive doc is a reference pointer for pulling detail/citations/URLs on demand, not a
     replacement for the paper's existing summary content.
4. Papers with no confident match: leave `gdoc_id` unset. Don't force a link.
5. Update the "Every paper note needs frontmatter" section of the sophie-desk skill
   (`.agents/skills/sophie-desk/SKILL.md`, canonical copy) to document the new optional
   `gdoc_id` field, then run `python scripts/gen_skills.py` to resync the `.claude/` mirror.
6. Commit. This is prose/frontmatter edits to existing files plus new gitignored cache files —
   no destructive action, but it's touching the paper library, so review the diff yourself
   before committing (this is why it's `assignee: claude`, not `agy`, even though it carries no
   `gate` — the "no gate" here reflects that nothing needs a *human* sign-off, not that it
   should run unattended).

## Decision log

- **2026-08-30** — Split off from `gdocs-index-sync` specifically because content-fetch needs
  a capability (Google Drive MCP connector) that only this Claude Code session is confirmed to
  have; bundling it into the agy-dispatched task would have silently failed on the fetch step.

## Result

<!-- filled by /desk-log on completion -->
