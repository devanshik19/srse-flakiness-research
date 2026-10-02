#!/bin/bash
# run_stress_cfg.sh <repo_root> <out_root> <configs.csv> [N]
# Reads configs.csv (label,stress-ng-args); lines starting with # are skipped.
# Whole repo by default. Override packages with PKGS="langgraph ...".
# Limit test CPU cores with CORES="0-5" (6 cores), "0-3" (4), "0-1" (2).
set -uo pipefail
LG="$(cd "$1" && pwd)"; OUT="$2"; CFG="$(cd "$(dirname "$3")" && pwd)/$(basename "$3")"; N="${4:-10}"
H="$(cd "$(dirname "$0")" && pwd)"; mkdir -p "$OUT"
[ -n "${CORES:-}" ] && export TASKSET="taskset -c $CORES"
PKGS="${PKGS:-langgraph checkpoint checkpoint-sqlite checkpoint-conformance prebuilt cli sdk-py}"
for pkg in $PKGS; do
  d="$LG/libs/$pkg"; [ -d "$d" ] || continue
  o="$OUT/$pkg"; mkdir -p "$o"; echo "===== $pkg ====="
  while IFS=, read -r label args; do
    [ -z "$label" ] && continue
    case "$label" in \#*) continue;; esac
    "$H/stress_nd.sh" "$d" "$label" "$o" "$N" $args </dev/null
  done < "$CFG"
done
echo ">>> DONE -> $OUT/<pkg>/stress_summary.csv"
