#!/usr/bin/env bash
# Read-only. Measures: does the script exist, and has it produced a report
# with a real number of rows (not just a header).
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f "scripts/exact_match_gdocs.py" ]; then
  echo "RUN scripts/exact_match_gdocs.py missing"
  exit 0
fi

if [ ! -f "gdocs/article-exact-matches.md" ]; then
  echo "RUN script exists but gdocs/article-exact-matches.md not generated yet"
  exit 0
fi

rows=$(grep -c '^|' gdocs/article-exact-matches.md 2>/dev/null || echo 0)
matched=$(grep -c '| matched |' gdocs/article-exact-matches.md 2>/dev/null || echo 0)

if [ "$rows" -lt 5 ]; then
  echo "RUN too few rows (${rows}) to be a real run"
  exit 0
fi

echo "OK ${rows} rows, ${matched} matched"
