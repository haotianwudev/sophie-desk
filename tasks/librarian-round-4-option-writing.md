---
id: librarian-round-4-option-writing
title: Find NEW option-writing papers (round 4) — record anything you can't download
lane: research
status: active
assignee: agy
gate:
repo: sophie-option-research
blocker:
next: Claim, check all 18 existing papers first, then search broadly again.
probe: bash probes/librarian-round-4-option-writing.sh
progress: <3>WSL (72965 - Relay) ERROR: CreateProcessCommon:640: execvpe(/bin/bash) failed: No such file or directory
probe_status: ERROR
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

A fourth round, back to the general scope (option writing / premium selling broadly, not
narrowed to VRP like round 3). Find **3-5 new** open-access papers and file them into
`papers/option-writing/`, same convention as every prior round.

**Before searching, read every existing `.md` note in `papers/option-writing/`** — there are
18 already, across four angles: general covered-call/put-writing decomposition, tail risk,
cross-asset/FX premium, VIX-futures roll premium, and now VRP predictors/term-structure from
round 3. Don't re-cover ground any of these already own.

## New this round: if you find a paper worth including but can't get the PDF

Some relevant papers will be paywalled, behind a dead link, or otherwise not actually
downloadable even though they're clearly real and relevant. **Don't just skip these silently.**
Instead, still write the `.md` note (title, authors, year, link, one-sentence hypothesis) but
put this line right after the title, before anything else:

```
**STATUS: PDF NOT DOWNLOADED — <short reason, e.g. "paywalled, SSRN preview only">**
```

No matching `.pdf` file for that one — that absence plus the STATUS line is what marks it
as "found but not fetched," so the user can go look at it themselves later and decide whether
it's worth getting some other way. Every other note keeps the existing convention (no STATUS
line, has a matching PDF).

Same file-pair convention otherwise: `<short-slug>.pdf` (only when genuinely open-access) +
`<short-slug>.md`.

## Why this folder, why gitignored PDFs

Same as every prior round: PDFs are gitignored (`papers/**/*.pdf`, this repo is public);
`.md` notes are committed.

## Not in scope

- Don't touch or re-summarize any existing paper's note.
- Don't touch `sophie-option-research` itself.
- Don't judge whether these papers validate anything — that's a later, gated step.

## Decision log

## Result

<!-- pointer only: how many new (downloaded + recorded-but-unavailable), folder is the real answer -->
