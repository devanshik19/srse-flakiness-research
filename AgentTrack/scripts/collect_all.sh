#!/bin/bash
# Whole-repo test manifest: project,sha,module,test for every pytest package under libs/.
# Usage: collect_all.sh <langgraph_repo_root> <out_csv>
set -uo pipefail
LG="$(cd "$1" && pwd)"; CSV="$2"
SHA=$(git -C "$LG" rev-parse HEAD)
LOGDIR="$(dirname "$CSV")/collect_logs"; mkdir -p "$LOGDIR"
echo "project name,sha,module,test" > "$CSV"
# checkpoint-postgres (needs Postgres) and sdk-js (JavaScript) are skipped.
for pkg in langgraph checkpoint checkpoint-sqlite checkpoint-conformance prebuilt cli sdk-py; do
  d="$LG/libs/$pkg"
  [ -d "$d" ] || { echo "skip $pkg (no dir)"; continue; }
  echo "=== $pkg: syncing (test group) ==="
  ( cd "$d" && { uv sync --group test --python 3.13 \
                 || uv sync --all-groups --python 3.13 \
                 || uv sync --python 3.13; } ) > "$LOGDIR/sync-$pkg.log" 2>&1 \
    || { echo "  !! sync FAILED for $pkg -> $LOGDIR/sync-$pkg.log"; continue; }
  # -o addopts= clears the package's config addopts (they set -vv, which hides node ids)
  ( cd "$d" && NO_DOCKER=true uv run --no-sync pytest --co -q -p no:randomly \
       --continue-on-collection-errors -o addopts= ) > "$LOGDIR/collect-$pkg.log" 2>&1 || true
  grep '::' "$LOGDIR/collect-$pkg.log" \
    | awk -v p=langgraph -v s="$SHA" -v m="libs/$pkg" '{print p","s","m","$0}' >> "$CSV"
  n=$(grep -c '::' "$LOGDIR/collect-$pkg.log" || true)
  echo "  $pkg: $n tests   (log: $LOGDIR/collect-$pkg.log)"
done
echo "TOTAL: $(( $(wc -l < "$CSV") - 1 )) tests -> $CSV"
