---
id: gdocs-content-link
title: Link papers to matching Drive research docs and cache their content
lane: research
status: done
assignee: claude
gate:
repo: sophie-desk
blocker:
next:
probe: none
progress:
probe_status:
stall_flag:
outcome: Ran match_gdoc.py against all 24 papers; inspected the 3 highest-scoring candidates (0.60-0.65) in full. None are genuinely about a specific library paper -- all are the user's own broader independent Gemini research syntheses, each with its own citation list. No gdoc_id links added -- correctly no match, not a stall.
artifacts: papers/option-writing/*.md (unmodified), gdocs/index.json (335 entries)
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
- **2026-08-30** — Ran `scripts/match_gdoc.py` against all 24 paper titles in
  `papers/option-writing/`. Best scores clustered 0.38-0.65 — no exact or near-exact matches.
  Fetched full content for the 3 highest scorers (0.65 "Decomposing Volatility Risk Premium" vs.
  Feunou-Jahan-Parvar-Okou's "Downside Variance Risk Premium"; 0.63 "Options Strategies for
  Market Crises" vs. Santa-Clara/Saretto's "Option Strategies: Good Deals and Margin Calls"; 0.60
  "Volatility Risk Premium Research and Application" vs. two FX/VRP papers). All three are the
  user's own independently-commissioned Gemini Deep Research reports on broad adjacent topics —
  each carries its own 20-30+ item Works Cited list of external sources, not a summary of any one
  paper in this library.
- **2026-08-30** — One genuine overlap found: the "Decomposing VRP" doc's citation #6 is
  literally titled "Downside Variance Risk Premium" (hosted at econ.au.dk), almost certainly the
  same working paper as `feunou-jahan-parvar-okou-2018-downside-variance-risk-premium.md` (whose
  own `link` field points to a different mirror, bank-banque-canada.ca — same title, same genre,
  different host, very likely the same paper). Did **not** add `gdoc_id` for this: the Drive doc
  is about VRP decomposition broadly and cites this paper once among 34 sources — a `gdoc_id`
  field implies "this doc is about that paper," which would misrepresent the relationship. A
  citation-overlap relationship (many-to-many, doc cites paper) doesn't fit that field; if this
  becomes worth tracking later it needs a different mechanism, not `gdoc_id`.
- **2026-08-30** — Conclusion: the `gdoc_id` design assumed the user's Drive research is often
  paper-specific (a deep-research write-up *of* a given academic paper). The actual corpus is
  the opposite — broad independent topic sessions that happen to cite some overlapping sources.
  No links added this round; that is the correct outcome per the task's own "don't force a
  link" rule, not a failure to find something. Left a pointer in the sophie-desk skill so a
  future run doesn't re-attempt the same search expecting a different result.

## Result

Ran the full matching pass across all 24 `papers/option-writing/*.md` entries against the
335-doc Drive index (`scripts/match_gdoc.py`). No paper cleared the "genuinely about this
paper" bar for a `gdoc_id` link — the Drive corpus turned out to be broad independent research,
not paper-specific summaries. No frontmatter was modified. See Decision log above for the one
interesting citation-overlap finding (Feunou-Jahan-Parvar-Okou 2018, cited once inside an
unrelated Drive doc's bibliography) that didn't warrant a link but might be worth knowing about.
