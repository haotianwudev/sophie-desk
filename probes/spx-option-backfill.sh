#!/usr/bin/env bash
# Probe: SPX option chain backfill.
# Prints one line: "<OK|RUN|STALL> <measurement>". Exits 0 always — a probe reports, never fails.
#
# Ground truth is file counts on disk, NOT the log and NOT task notifications. Both have lied
# in both directions on this job: a wrapper printed DOWNLOAD FULLY COMPLETE having downloaded
# nothing, and a "killed" notification arrived while the work was still running.

set -u
PIPE="/f/workspace/sophie-pipeline"
RAW="$PIPE/data/raw_theta"
LOG="$PIPE/data/download_full.log"
TOTAL_SPXW=1360
STALL_HOURS=6

spx=$(ls "$RAW/SPX"/*.csv 2>/dev/null | wc -l)
spxw=$(ls "$RAW/SPXW"/*.csv 2>/dev/null | wc -l)

if [ -f "$PIPE/data/DOWNLOAD_COMPLETE" ]; then
  echo "OK complete · SPX $spx · SPXW $spxw"
  exit 0
fi

# Is a downloader actually alive? A quiet log alone proves nothing.
alive=$(ps -W 2>/dev/null | grep -ci "python" || echo 0)

if [ -f "$LOG" ]; then
  age=$(( ( $(date +%s) - $(stat -c %Y "$LOG") ) / 3600 ))
else
  age=999
fi

if [ "$age" -ge "$STALL_HOURS" ]; then
  echo "STALL SPXW $spxw/$TOTAL_SPXW · log idle ${age}h · ${alive} python procs"
else
  echo "RUN SPXW $spxw/$TOTAL_SPXW · log ${age}h ago"
fi
exit 0
