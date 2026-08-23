#!/usr/bin/env bash
set -u
Q="${1:?queue.tsv}"; OUT="$HOME/srse-research/results.md"; LOG="$HOME/srse-research/batch.log"
mkdir -p "$HOME/srse-research"; cd "$HOME/srse-java" || exit 1
n=0
while IFS=$'\t' read -r url cls <&9; do
  [ -z "${url:-}" ] && continue
  n=$((n+1)); echo "=== [$n] $cls $(date +%H:%M) ===" | tee -a "$LOG"
  r=$(timeout 1500 ./run_one.sh "$url" "$cls" </dev/null 2>&1 | tee -a "$LOG" | grep -E '^\| \? \|' | tail -1)
  echo "${r:-| ? | $cls | - | - | - | - | - | - | TIMEOUT/CRASH |}" | tee -a "$OUT"
done 9< "$Q"
echo "DONE -> $OUT"
