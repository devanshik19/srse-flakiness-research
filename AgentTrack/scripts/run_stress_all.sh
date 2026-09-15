#!/bin/bash
# run_stress_all.sh -- baseline + cpu/memory/io/device stress (start small).
# Usage: run_stress_all.sh <repo_dir> <out_dir> [N] [level]
#   level = stress-ng --all value; start 1, then 2/4/8.
set -uo pipefail
REPO="$1"; OUT="$2"; N="${3:-10}"; L="${4:-1}"
H="$(cd "$(dirname "$0")" && pwd)"
"$H/stress_nd.sh" "$REPO" baseline  "$OUT" "$N"
"$H/stress_nd.sh" "$REPO" cpu-$L    "$OUT" "$N" --class cpu    --all "$L"
"$H/stress_nd.sh" "$REPO" memory-$L "$OUT" "$N" --class vm     --all "$L"
"$H/stress_nd.sh" "$REPO" io-$L     "$OUT" "$N" --class io     --all "$L"
"$H/stress_nd.sh" "$REPO" device-$L "$OUT" "$N" --class device --all "$L"
echo ">>> ALL DONE -> $OUT/stress_summary.csv"
