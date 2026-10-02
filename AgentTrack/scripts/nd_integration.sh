#!/bin/bash
# ND check for the sdk-py INTEGRATION suite: each test ALONE, fresh process, N reruns.
# Unlike run_nd_batch.sh it (a) opts back IN to the integration marker -- addopts carries
# -m 'not integration', which would deselect every test (exit 5 = "missing"), and (b) treats a
# conftest skip as API-down, not a pass -- the autouse guard skips (exit 0) when /ok is unreachable.
# Resumable: skips tests already in nd_summary.csv.
set -uo pipefail
REPODIR="$(cd "$1" && pwd)"; QUEUE="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
OUTDIR="$3"; N="${4:-50}"; PROMOTE="${5:-200}"
URL="${LANGGRAPH_INTEGRATION_URL:-http://localhost:2024}"
mkdir -p "$OUTDIR"; OUTDIR="$(cd "$OUTDIR" && pwd)"
SUMMARY="$OUTDIR/nd_summary.csv"; PERRUN="$OUTDIR/nd_perrun.csv"; PROM="$OUTDIR/nd_perrun_promote.csv"
[ -f "$SUMMARY" ] || echo "test_id,pass,fail,missing,total,verdict" > "$SUMMARY"
for f in "$PERRUN" "$PROM"; do [ -f "$f" ] || echo "test_id,run,result" > "$f"; done
cd "$REPODIR"
curl -sf -m 5 "$URL/ok" >/dev/null || { echo "!! API not up at $URL -- start the stack first"; exit 1; }

one(){ # $1=testid $2=N $3=perrun; sets P F M S; returns 1 if the API went away mid-run
  local id="$1" n="$2" out="$3" k code res
  P=0; F=0; M=0; S=0
  for k in $(seq 1 "$n"); do
    NO_DOCKER=true PYTHONHASHSEED=0 uv run --no-sync pytest "$id" \
      -o addopts= -m integration -p no:randomly -q > "/tmp/ndi-$k.log" 2>&1
    code=$?
    if   [ "$code" -eq 5 ]; then res=missing; M=$((M+1))
    elif [ "$code" -ne 0 ]; then res=fail;    F=$((F+1))
    elif grep -qE '[0-9]+ skipped' "/tmp/ndi-$k.log"; then res=skip; S=$((S+1))
    else                         res=pass;    P=$((P+1)); fi
    echo "$id,$k,$res" >> "$out"
    echo ">>>   [$k/$n] $res  (pass=$P fail=$F missing=$M skip=$S)"
    [ "$res" = skip ] && return 1
  done
  return 0
}
verdict(){ v=NOT_FLAKY; { [ "$F" -gt 0 ] || [ "$M" -gt 0 ]; } && v=FLAKY_ND; }

total=$(grep -c '::' "$QUEUE"); i=0
while IFS= read -r T; do
  [ -z "$T" ] && continue; i=$((i+1))
  if cut -d, -f1 "$SUMMARY" | grep -qxF "$T"; then echo ">>> [$i/$total] SKIP done: $T"; continue; fi
  echo ">>> [$i/$total] ND (N=$N): $T"
  one "$T" "$N" "$PERRUN" || { echo "!! skipped -> API down at $URL. Stopping; nothing logged for $T."; exit 1; }
  verdict; used=$N
  if [ "$v" = FLAKY_ND ]; then
    echo ">>> !! FLINCH: $T -> promoting to N=$PROMOTE"
    one "$T" "$PROMOTE" "$PROM" || { echo "!! API down mid-promote. Stopping; nothing logged for $T."; exit 1; }
    verdict; used=$PROMOTE
  fi
  echo "$T,$P,$F,$M,$used,$v" >> "$SUMMARY"
  echo ">>> [$i/$total] $T -> $v"
done < "$QUEUE"
echo ">>> DONE. FLAKY_ND tests:"; grep ',FLAKY_ND$' "$SUMMARY" || echo "  (none)"
