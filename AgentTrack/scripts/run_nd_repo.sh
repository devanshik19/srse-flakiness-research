#!/bin/bash
# ND-sweep the remaining libs/ packages: collect -> prioritize -> run_nd_batch, per package.
# Usage: run_nd_repo.sh <repo_root> <out_root> [N] [promote_N]
set -uo pipefail
LG="$(cd "$1" && pwd)"; OUT="$2"; N="${3:-50}"; PR="${4:-200}"
H="$(cd "$(dirname "$0")" && pwd)"; mkdir -p "$OUT"
for pkg in checkpoint checkpoint-sqlite checkpoint-conformance prebuilt cli sdk-py; do
  d="$LG/libs/$pkg"; o="$OUT/$pkg"; [ -d "$d" ] || { echo "skip $pkg"; continue; }
  mkdir -p "$o"
  echo "=== $pkg: collect ==="
  ( cd "$d" && NO_DOCKER=true uv run --no-sync pytest --co -q -p no:randomly -o addopts= 2>/dev/null | grep '::' ) > "$o/tests_all.txt" || true
  python3 "$H/prioritize.py" "$o/tests_all.txt" "$o/tests_queue.txt"
  echo "=== $pkg: ND N=$N ($(wc -l < "$o/tests_queue.txt") tests) ==="
  "$H/run_nd_batch.sh" "$d" "$o/tests_queue.txt" "$o" "$N" "$PR"
done
echo ">>> DONE -> $OUT/<pkg>/nd_summary.csv"
