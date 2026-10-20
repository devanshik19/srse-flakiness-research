#!/bin/bash
# docker_validate.sh <gen_out_dir> [N] [MAXI] [START] [quick]
# Run generated tests inside each instance's Epoch image (correct Python/deps), logging EACH
# test's verdict per run, in six regimes that isolate one variable at a time:
#   baseline : fixed order, FIXED seed (PYTHONHASHSEED=0), no stress   -> intrinsic ND control
#   cpu/io/memory : fixed order, fixed seed, under stress-ng load      -> timing / race flakiness
#   hashseed : fixed order, RANDOM PYTHONHASHSEED                      -> hash-ordering (NOD)
#   order    : RANDOM order (-p randomly), fixed seed                  -> order-dependence (OD)
# A test whose verdict is not identical across all runs of a regime is flaky. Writes docker_results.csv.
#
# Resume: process only folders [START..MAXI] (1-based, sorted order). MAXI=0 = to end.
# Output: a new CSV gets a header; an existing CSV is appended to. Override the path with OUT_CSV=...
# Examples:
#   bash docker_validate.sh gen_django 10                                   # all, 10 runs each
#   bash docker_validate.sh gen_django 10 40 21                             # 21..40, append to docker_results.csv
#   OUT_CSV=gen_django/docker_results2.csv bash docker_validate.sh gen_django 10 40 21   # 21..40 into its own CSV
set -uo pipefail
GEN="$(realpath "$1")"; N="${2:-5}"; MAXI="${3:-0}"; START="${4:-1}"
# output CSV: defaults to gen dir; override with env OUT_CSV=... (e.g. a separate docker_results2.csv)
OUT="${OUT_CSV:-$GEN/docker_results.csv}"
ACT="source /opt/miniconda3/bin/activate && conda activate testbed"
PYT="python -m pytest _gen_tests -v --tb=no -p no:cacheprovider --continue-on-collection-errors"

# stress regimes: "phase_name|stress-ng args"  (memory bounded so it can't OOM the box)
# (interrupt/filesystem/vm classes segfault or overload on WSL — left out on purpose)
STRESS=( "cpu|--class cpu --all 1"
         "io|--class io --all 1"
         "memory|--vm 2 --vm-bytes 256M" )
[ "${5:-}" = "quick" ] && STRESS=()   # 5th arg "quick" = baseline + hashseed + order only

[ ! -f "$OUT" ] && echo "instance,phase,run,test,verdict" > "$OUT"   # new file gets a header; existing file is appended to

log_runs() {   # $1=container  $2=instance  $3=phase  $4=env-prefix  $5=pytest-extra-args
  for i in $(seq 1 "$N"); do
    echo "  $3 run $i/$N" >&2
    docker exec "$1" bash -lc "$ACT && cd /testbed && $4 $PYT $5" 2>&1 \
      | grep -oE '_gen_tests/\S+::\S+ (PASSED|FAILED|ERROR)' \
      | while read -r line; do
          v="${line##* }"; t="${line% *}"
          echo "$2,$3,$i,\"$t\",$v" >> "$OUT"
        done
  done
}

count=0
for d in "$GEN"/*/; do
  count=$((count + 1))
  [ "$count" -lt "$START" ] && continue
  [ "$MAXI" -gt 0 ] && [ "$count" -gt "$MAXI" ] && break
  INST="$(basename "$d")"
  IMG="ghcr.io/epoch-research/swe-bench.eval.x86_64.$INST"
  echo "===== $INST ($count) ====="
  docker pull -q "$IMG" >/dev/null 2>&1 || docker pull -q "$IMG" >/dev/null 2>&1 \
    || { echo "  PULL FAILED"; continue; }
  CID="$(docker run -d -e PYTHONDONTWRITEBYTECODE=1 -v "$d":/testbed/_gen_tests:ro "$IMG" sleep infinity)"
  docker exec "$CID" bash -lc "$ACT && pip install -q pytest pytest-randomly pytest-django" >/dev/null 2>&1

  # baseline: fixed order + fixed seed
  echo "-- baseline --"; log_runs "$CID" "$INST" baseline "PYTHONHASHSEED=0" "-p no:randomly"

  # stress: fixed order + fixed seed, under load
  for s in "${STRESS[@]}"; do
    name="${s%%|*}"; args="${s#*|}"
    echo "-- $name stress --"
    stress-ng $args >/dev/null 2>&1 & SP=$!; sleep 2
    if kill -0 "$SP" 2>/dev/null; then                 # only log if the stressor is alive
      log_runs "$CID" "$INST" "$name" "PYTHONHASHSEED=0" "-p no:randomly"
      kill "$SP" 2>/dev/null; pkill -x stress-ng 2>/dev/null
    else
      echo "  $name stressor died, skipping phase" >&2
    fi
  done

  # hashseed: random seed, fixed order  (isolates hash-ordering / NOD)
  echo "-- hashseed --"; log_runs "$CID" "$INST" hashseed "PYTHONHASHSEED=\$RANDOM" "-p no:randomly"

  # order: random order, fixed seed  (isolates order-dependence / OD)
  echo "-- order --"; log_runs "$CID" "$INST" order "PYTHONHASHSEED=0" "-p randomly"

  docker rm -f "$CID" >/dev/null
  docker rmi -f "$IMG" >/dev/null 2>&1          # reclaim disk; tests are saved, re-pull if needed
done
echo ">>> results -> $OUT"
