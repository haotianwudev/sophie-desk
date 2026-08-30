#!/usr/bin/env bash
# Read-only. Generic probe reused across all classify+extract batch tasks.
# Measures: how many matched docs are classified so far, and how many
# citation candidate rows exist in FOLLOWUP-CANDIDATES.md.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f "gdocs/classified_state.json" ]; then
  echo "RUN no gdocs/classified_state.json yet"
  exit 0
fi

classified=$(python -c "import json; print(len(json.load(open('gdocs/classified_state.json', encoding='utf-8'))))" 2>/dev/null || echo 0)

set +e
citation_rows=$(grep -E '^\|' papers/FOLLOWUP-CANDIDATES.md 2>/dev/null | grep -cE '\(https://www\.sophie-ai-finance\.com/articles/')
set -e
citation_rows=${citation_rows:-0}

if [ "$classified" -eq 0 ]; then
  echo "RUN 0 docs classified yet"
  exit 0
fi

echo "OK ${classified}/215 docs classified, ${citation_rows} citation candidate rows"
