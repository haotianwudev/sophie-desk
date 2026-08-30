---
id:
title:
lane:            # content | research | platform
status: queued   # queued | active | blocked | gate | done
assignee: none   # claude | agy | ollama | either | none
gate:            # g1 | g2 | g3 | (empty if none)
repo:            # sophie-pipeline | ai-stock-suggestion-server | ai-stock-suggestion-client | sophie-option-research
blocker:
next:
probe: none      # shell command, or none
progress:        # written by the supervisor — do not hand-edit
probe_status:    # OK | RUN | STALL — written by the supervisor
outcome:         # one line, filled on done
artifacts:       # commits, URLs, study tags, row counts
created:
updated:
---

## Goal

What done looks like, in one paragraph. Acceptance criteria if they aren't obvious.

## Plan

Ordered steps. Mark hard stops explicitly.

## Decision log

Append-only. Newest last. Date every entry.

## Result

Filled by `/desk-log` on completion — pointers, not copies. A study tag and a row count,
not the Sharpe numbers, which live in `option_research_evaluation` and go stale on re-run.
