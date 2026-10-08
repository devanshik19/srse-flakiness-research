#!/bin/bash
# docker_validate.sh <gen_out_dir> [N]
# Run generated tests inside each instance's Epoch image (correct Python/deps), N times at
# baseline and N times under host CPU stress, logging EACH test's verdict per run.
# A test that is not the same verdict every time -> flaky. Writes docker_results.csv.
set -uo pipefail
GEN="$(realpath "$1")"; N="${2:-5}"
OUT="$GEN/docker_results.csv"
ACT="source /opt/miniconda3/bin/activate && conda activate testbed"
echo "instance,phase,run,test,verdict" > "$OUT"

log_runs() {   # $1=container  $2=instance  $3=phase
  for i in $(seq 1 "$N"); do
    echo "  $3 run $i/$N" >&2
    docker exec "$1" bash -lc "$ACT && cd /testbed && python -m pytest _gen_tests -v --tb=no -p no:cacheprovider --continue-on-collection-errors" 2>&1 \
      | grep -oE '_gen_tests/\S+::\S+ (PASSED|FAILED|ERROR)' \
      | while read -r line; do
          v="${line##* }"; t="${line% *}"
          echo "$2,$3,$i,\"$t\",$v" >> "$OUT"
        done
  done
}

for d in "$GEN"/*/; do
  INST="$(basename "$d")"
  IMG="ghcr.io/epoch-research/swe-bench.eval.x86_64.$INST"
  echo "===== $INST ====="
  docker pull -q "$IMG" >/dev/null 2>&1 || { echo "  PULL FAILED"; continue; }
  CID="$(docker run -d -e PYTHONDONTWRITEBYTECODE=1 -v "$d":/testbed/_gen_tests:ro "$IMG" sleep infinity)"
  docker exec "$CID" bash -lc "$ACT && pip install -q pytest" >/dev/null 2>&1

  echo "-- baseline --"
  log_runs "$CID" "$INST" baseline

  echo "-- cpu stress --"
  stress-ng --class cpu --all 1 >/dev/null 2>&1 & SP=$!; sleep 2
  log_runs "$CID" "$INST" cpu
  kill "$SP" 2>/dev/null; pkill -x stress-ng 2>/dev/null

  docker rm -f "$CID" >/dev/null
  docker rmi -f "$IMG" >/dev/null 2>&1          # reclaim disk; tests are saved, re-pull if needed
done
echo ">>> results -> $OUT"
