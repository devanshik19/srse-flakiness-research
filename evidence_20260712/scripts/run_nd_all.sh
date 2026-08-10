#!/usr/bin/env bash
# run_nd_all.sh — ND loop over real-result projects, IN QUEUE ORDER (sequential).
# Usage: ./run_nd_all.sh ~/srse-research/nd_queue.tsv [NDN]
set -u
Q="${1:?need queue tsv}"; NDN="${2:-100}"
OUT="$HOME/srse-research/nd_results.md"; : > "$OUT"
cd "$HOME/srse-java" || exit 1
while IFS=$'\t' read -r class dir; do
    [ -z "$class" ] && continue
    echo "### ND: $class"
    "$HOME/srse-java/run_nd.sh" "$class" "$NDN" "$HOME/srse-java/$dir" 2>&1 | tee -a "$OUT" | grep -E "pass /|ND-ROW"
done < "$Q"
echo "ND DONE — $OUT"
