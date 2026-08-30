#!/usr/bin/env bash
# Read-only. Measures: does the extractor script exist, and has it added at
# least one new candidate row whose Surfaced-by is an article link (not a
# paper-note reference like [some-paper-slug]) -- the marker that
# distinguishes a citation-extraction row from the original 71.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f "scripts/extract_gdoc_citations.py" ]; then
  echo "RUN scripts/extract_gdoc_citations.py missing"
  exit 0
fi

# Only count actual table rows (start with '|'), not the schema doc's own
# example text near the top of the file, which contains this same URL
# pattern and was a false-positive match here once already.
set +e
new_rows=$(grep -E '^\|' papers/FOLLOWUP-CANDIDATES.md 2>/dev/null | grep -cE '\(https://www\.sophie-ai-finance\.com/articles/')
set -e

if [ "$new_rows" -eq 0 ]; then
  echo "RUN script exists but no citation candidate rows added yet"
  exit 0
fi

echo "OK ${new_rows} citation candidate rows added"
