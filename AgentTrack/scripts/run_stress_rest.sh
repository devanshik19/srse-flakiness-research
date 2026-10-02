#!/bin/bash
set -uo pipefail
LG="$(cd "$1" && pwd)"; OUT="$2"; N="${3:-15}"
H="$(cd "$(dirname "$0")" && pwd)"
for pkg in checkpoint checkpoint-sqlite checkpoint-conformance prebuilt cli sdk-py; do
  d="$LG/libs/$pkg"; [ -d "$d" ] || continue; o="$OUT/$pkg"; mkdir -p "$o"
  echo "===== STRESS $pkg ====="
  "$H/stress_nd.sh" "$d" io-1     "$o" "$N" --class io     --all 1
  "$H/stress_nd.sh" "$d" device-1 "$o" "$N" --class device --all 1
  "$H/stress_nd.sh" "$d" cpu-1    "$o" "$N" --class cpu    --all 1
  "$H/stress_nd.sh" "$d" memory-1 "$o" "$N" --vm 2 --vm-bytes 256M
done
echo ">>> DONE -> $OUT/<pkg>/stress_summary.csv"
