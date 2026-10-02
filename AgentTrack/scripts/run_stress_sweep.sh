#!/bin/bash
# run_stress_sweep.sh <repo_dir> <out_dir> [N] [levels]
# Runs the whole suite N times under each stress class, at each --all level.
# memory/vm is bounded (never --all) so it can't OOM the box.
set -uo pipefail
REPO="$1"; OUT="$2"; N="${3:-10}"; LEVELS="${4:-2}"
H="$(cd "$(dirname "$0")" && pwd)"
LEVELS="${LEVELS//,/ }"
CLASSES="cpu cpu-cache io device interrupt filesystem pipe security os scheduler"

"$H/stress_nd.sh" "$REPO" baseline "$OUT" "$N"
"$H/stress_nd.sh" "$REPO" memory  "$OUT" "$N" --vm 2 --vm-bytes 256M
for L in $LEVELS; do
  for C in $CLASSES; do
    "$H/stress_nd.sh" "$REPO" "${C}-${L}" "$OUT" "$N" --class "$C" --all "$L"
  done
done
echo ">>> SWEEP DONE -> $OUT/stress_summary.csv"
