#!/bin/bash
# docker_validate.sh <gen_out_dir> [N]
# Run generated tests inside each instance's Epoch image, logging each test's verdict per run, in:
#   baseline : fixed order, no stress
#   <stress> : fixed order, under each stress regime in STRESS below (timing / race flakiness)
#   shuffle  : random test order + random hash seed (order / nondeterminism flakiness)
# A test whose verdict is not identical across all runs is flaky. Writes docker_results.csv.
set -uo pipefail
GEN="$(realpath "$1")"; N="${2:-5}"; MAXI="${3:-0}"; START="${4:-1}"   # process instances [START..MAXI]; MAXI=0 = to end
OUT="$GEN/docker_results.csv"
ACT="source /opt/miniconda3/bin/activate && conda activate testbed"
PYT="python -m pytest _gen_tests -v --tb=no -p no:cacheprovider --continue-on-collection-errors"

# stress regimes: "phase_name|stress-ng args"  (memory is bounded so it can't OOM the box)
# (interrupt/filesystem/vm classes segfault or overload on WSL — left out on purpose)
STRESS=( "cpu|--class cpu --all 1"
         "io|--class io --all 1"
         "memory|--vm 2 --vm-bytes 256M" )
[ "${5:-}" = "quick" ] && STRESS=()   # 5th arg "quick" = baseline + shuffle only (stress already proven ~0)

[ "$START" -le 1 ] && echo "instance,phase,run,test,verdict" > "$OUT"   # fresh start writes header; resume appends

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

  echo "-- baseline --"; log_runs "$CID" "$INST" baseline "" "-p no:randomly"

  for s in "${STRESS[@]}"; do
    name="${s%%|*}"; args="${s#*|}"
    echo "-- $name stress --"
    stress-ng $args >/dev/null 2>&1 & SP=$!; sleep 2
    if kill -0 "$SP" 2>/dev/null; then                 # only log if the stressor is alive
      log_runs "$CID" "$INST" "$name" "" "-p no:randomly"
      kill "$SP" 2>/dev/null; pkill -x stress-ng 2>/dev/null
    else
      echo "  $name stressor died, skipping phase" >&2
    fi
  done

  echo "-- shuffle --"; log_runs "$CID" "$INST" shuffle "PYTHONHASHSEED=\$RANDOM" ""

  docker rm -f "$CID" >/dev/null
  docker rmi -f "$IMG" >/dev/null 2>&1          # reclaim disk; tests are saved, re-pull if needed
done
echo ">>> results -> $OUT"
