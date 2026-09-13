#!/bin/bash
# ND check for ONE pytest test id: run ALONE, fresh process, same order, N times.
set -uo pipefail
REPODIR="$(cd "$1" && pwd)"; TESTID="$2"
RESULTS="$(cd "$(dirname "$3")" && pwd)/$(basename "$3")"; N="${4:-50}"
cd "$REPODIR"; log(){ echo ">>> $*"; }
[ -f "$RESULTS" ] || echo "test_id,run,result" > "$RESULTS"
pass=0; fail=0; miss=0
for k in $(seq 1 "$N"); do
  NO_DOCKER=true PYTHONHASHSEED=0 uv run --no-sync pytest "$TESTID" -p no:randomly -q > "/tmp/nd-$k.log" 2>&1
  code=$?
  if   [ "$code" -eq 0 ]; then res=pass;    pass=$((pass+1))
  elif [ "$code" -eq 5 ]; then res=missing; miss=$((miss+1))
  else                         res=fail;    fail=$((fail+1)); fi
  echo "$TESTID,$k,$res" >> "$RESULTS"
  log "  [$k/$N] -> $res  (pass=$pass fail=$fail missing=$miss)"
done
verdict=NOT_FLAKY; { [ "$fail" -gt 0 ] || [ "$miss" -gt 0 ]; } && verdict=FLAKY_ND
echo "ND_RESULT=$TESTID pass=$pass fail=$fail missing=$miss total=$N verdict=$verdict"
