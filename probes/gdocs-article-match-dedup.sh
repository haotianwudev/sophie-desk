#!/usr/bin/env bash
# Read-only. Measures: do the two report scripts exist and have they produced
# non-trivial output files.
set -euo pipefail
cd "$(dirname "$0")/.."

missing=""
[ -f "scripts/match_articles_gdocs.py" ] || missing="$missing scripts/match_articles_gdocs.py"
[ -f "scripts/find_gdoc_duplicates.py" ] || missing="$missing scripts/find_gdoc_duplicates.py"

if [ -n "$missing" ]; then
  echo "RUN missing:$missing"
  exit 0
fi

if [ ! -f "gdocs/article-matches.md" ] || [ ! -f "gdocs/duplicates.md" ]; then
  echo "RUN scripts exist but reports not generated yet"
  exit 0
fi

rows=$(grep -c '^|' gdocs/article-matches.md 2>/dev/null || echo 0)
dupgroups=$(grep -c '^## ' gdocs/duplicates.md 2>/dev/null || echo 0)

if [ "$rows" -lt 5 ]; then
  echo "RUN article-matches.md has too few rows (${rows}) to be a real run"
  exit 0
fi

echo "OK ${rows} article-match rows, ${dupgroups} duplicate groups"
