#!/bin/bash
# run_stress_sweep_repo.sh <repo_root> <out_root> [N] [levels]
# Whole-repo stress sweep: every package under libs/, every stress class, each level.
# Integration tests auto-skip (NO_DOCKER + addopts -m "not integration").
# memory/vm is bounded so it can't OOM the box.
set -uo pipefail
LG="$(cd "$1" && pwd)"; OUT="$2"; N="${3:-10}"; LEVELS="${4:-2}"
H="$(cd "$(dirname "$0")" && pwd)"; mkdir -p "$OUT"
LEVELS="${LEVELS//,/ }"
CLASSES="cpu cpu-cache io device interrupt filesystem pipe security os scheduler"
for pkg in langgraph checkpoint checkpoint-sqlite checkpoint-conformance prebuilt cli sdk-py; do
  d="$LG/libs/$pkg"; [ -d "$d" ] || continue
  o="$OUT/$pkg"; mkdir -p "$o"
  echo "===== STRESS $pkg ====="
  "$H/stress_nd.sh" "$d" baseline "$o" "$N"
  "$H/stress_nd.sh" "$d" memory   "$o" "$N" --vm 2 --vm-bytes 256M
  for L in $LEVELS; do
    for C in $CLASSES; do
      "$H/stress_nd.sh" "$d" "${C}-${L}" "$o" "$N" --class "$C" --all "$L"
    done
  done
done
echo ">>> SWEEP DONE -> $OUT/<pkg>/stress_summary.csv"
