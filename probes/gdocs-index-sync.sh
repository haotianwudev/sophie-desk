#!/usr/bin/env bash
# Read-only. Measures: does gdocs/index.json exist, is it non-empty, and is it
# roughly in sync with what's actually sitting in D:\GoogleDrive right now.
set -euo pipefail
cd "$(dirname "$0")/.."

IDX="gdocs/index.json"
DRIVE_DIR="/d/GoogleDrive"

if [ ! -f "scripts/sync_gdocs_index.py" ] || [ ! -f "scripts/match_gdoc.py" ]; then
  echo "RUN scripts/sync_gdocs_index.py or scripts/match_gdoc.py missing"
  exit 0
fi

if [ ! -f "$IDX" ]; then
  echo "RUN no gdocs/index.json yet"
  exit 0
fi

indexed=$(python -c "import json; print(len(json.load(open('$IDX'))))" 2>/dev/null || echo 0)

if [ "$indexed" -eq 0 ]; then
  echo "RUN index file present but empty"
  exit 0
fi

# Top-level count is a cheap proxy for "is the index stale" -- the real scan is
# recursive and skip-filtered, so this is a tolerance check, not an exact match.
live=$(find "$DRIVE_DIR" -maxdepth 1 -iname "*.gdoc" 2>/dev/null | wc -l)
diff=$(( live - indexed ))
[ "$diff" -lt 0 ] && diff=$(( -diff ))

if [ "$diff" -le 10 ]; then
  echo "OK ${indexed} docs indexed (live top-level count ${live})"
else
  echo "RUN index stale -- ${indexed} indexed vs ${live} live top-level .gdoc files"
fi
