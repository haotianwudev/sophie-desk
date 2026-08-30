#!/usr/bin/env bash
# Read-only. Measures: does the classifier script exist, and has it added
# at least one new candidate row with a Doc ID Source filled in (the
# marker that distinguishes a gdocs-sourced row from the original 71
# citation-following rows, which all have an empty Doc ID Source).
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f "scripts/classify_gdocs_candidates.py" ]; then
  echo "RUN scripts/classify_gdocs_candidates.py missing"
  exit 0
fi

# Count Candidates-table rows with a non-empty last-but-one cell (Doc ID Source).
new_rows=$(awk -F'|' '
  /^\| Title \(best guess\)/ {intable=1; next}
  /^\|---/ {next}
  /^## Passed on/ {intable=0}
  intable && /^\|/ {
    gsub(/^[ \t]+|[ \t]+$/, "", $7)
    if ($7 != "") c++
  }
  END { print c+0 }
' papers/FOLLOWUP-CANDIDATES.md)

if [ "$new_rows" -eq 0 ]; then
  echo "RUN script exists but no candidate rows with a Doc ID Source yet"
  exit 0
fi

echo "OK ${new_rows} candidate rows sourced from gdocs (Doc ID Source filled)"
