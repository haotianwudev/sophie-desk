---
id:
title:
lane:            # content | research | platform
status: queued   # queued | active | blocked | gate | done
assignee: none   # claude | agy | either | none -- NOT ollama: it can't claim, read, or close
                 # a task on its own (no tool use, no file access). It's a script-callable
                 # utility (scripts/ollama_call.py) that whoever holds the task can use for
                 # cheap bulk work -- note that in the Plan, not in this field.
gate:            # g1 | g2 | g3 | (empty if none)
repo:            # sophie-pipeline | ai-stock-suggestion-server | ai-stock-suggestion-client | sophie-option-research
blocker:
next:
probe: none      # shell command, or none. If it calls bash, use the FULL path to Git
                 # Bash's bash.exe (e.g. "C:\Program Files\Git\bin\bash.exe" probes/x.sh) --
                 # a bare `bash` resolves differently depending on who's running it (Git
                 # Bash's own shell vs. plain PowerShell vs. Task Scheduler), and in at
                 # least one of those it silently resolves to Windows' WSL launcher stub
                 # instead, which fails outright if WSL isn't set up. See sophie-desk skill.
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
