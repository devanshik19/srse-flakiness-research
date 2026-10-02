#!/bin/bash
# Stress every pytest package under libs/ (integration tests auto-skip via NO_DOCKER).
# Per package: io, device, cpu, memory at --all <level>, N reruns each.
# Usage: run_stress_repo.sh <repo_root> <out_root> [N] [level]
set -uo pipefail
LG="$(cd "$1" && pwd)"; OUT="$2"; N="${3:-10}"; L="${4:-1}"
H="$(cd "$(dirname "$0")" && pwd)"; mkdir -p "$OUT"
for pkg in langgraph checkpoint checkpoint-sqlite checkpoint-conformance prebuilt cli sdk-py; do
  d="$LG/libs/$pkg"; [ -d "$d" ] || continue
  o="$OUT/$pkg"; mkdir -p "$o"
  echo "===== STRESS $pkg ====="
  "$H/stress_nd.sh" "$d" "io-$L"     "$o" "$N" --class io     --all "$L"
  "$H/stress_nd.sh" "$d" "device-$L" "$o" "$N" --class device --all "$L"
  "$H/stress_nd.sh" "$d" "cpu-$L"    "$o" "$N" --class cpu    --all "$L"
  "$H/stress_nd.sh" "$d" "memory-$L" "$o" "$N" --class vm     --all "$L"
done
echo ">>> ALL DONE -> $OUT/<pkg>/stress_summary.csv"
