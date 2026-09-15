#!/bin/bash
# stress_nd.sh -- run a suite under ONE stress-ng config, N times, log failures.
# Shaker-style: stress-ng <config> & in the background while pytest runs.
# Usage: stress_nd.sh <repo_dir> <label> <out_dir> <N> [stress-ng args...]
#   (no stress args = no-stress baseline / control)
set -uo pipefail
REPO="$(cd "$1" && pwd)"; LABEL="$2"; mkdir -p "$3"; OUT="$(cd "$3" && pwd)"; N="$4"; shift 4
CFG="$*"; cd "$REPO"; SUM="$OUT/stress_summary.csv"
[ -f "$SUM" ] || echo "label,config,run,exit_code,failed,skipped" > "$SUM"
PID=""
if [ -n "$CFG" ]; then stress-ng $CFG & PID=$!; trap '[ -n "$PID" ] && kill "$PID" 2>/dev/null' EXIT; sleep 3; fi
for i in $(seq 1 "$N"); do
  log="$OUT/${LABEL}-run-$i.log"
  NO_DOCKER=true uv run --no-sync pytest -p no:randomly -q -rf --junitxml="$OUT/${LABEL}-run-$i.xml" > "$log" 2>&1
  code=$?; nf=$(grep -c "^FAILED" "$log" 2>/dev/null || echo 0); ns=$(grep -c "skipped" "$log" 2>/dev/null || echo 0)
  grep "^FAILED" "$log" >> "$OUT/${LABEL}-failures.txt" 2>/dev/null || true
  echo "$LABEL,\"$CFG\",$i,$code,$nf,$ns" >> "$SUM"
  echo ">>> [$i/$N] $LABEL exit=$code failed=$nf"
done
[ -n "$PID" ] && kill "$PID" 2>/dev/null
echo ">>> DONE $LABEL -> failures in $OUT/${LABEL}-failures.txt"
