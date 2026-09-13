#!/bin/bash
# ND-check every test in the queue (suspects first). N=50; any flinch -> re-run at 200.
# Resumable: skips tests already in nd_summary.csv, so you can Ctrl-C and rerun.
set -uo pipefail
REPODIR="$(cd "$1" && pwd)"; QUEUE="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
OUTDIR="$3"; N="${4:-50}"; PROMOTE="${5:-200}"
HERE="$(cd "$(dirname "$0")" && pwd)"; mkdir -p "$OUTDIR"; OUTDIR="$(cd "$OUTDIR" && pwd)"
SUMMARY="$OUTDIR/nd_summary.csv"; PERRUN="$OUTDIR/nd_perrun.csv"
[ -f "$SUMMARY" ] || echo "test_id,pass,fail,missing,total,verdict" > "$SUMMARY"
total=$(grep -c '::' "$QUEUE"); i=0
grab(){ sed -n "s/.*$1=\([A-Za-z0-9_]*\).*/\1/p" <<<"$2"; }
while IFS= read -r T; do
  [ -z "$T" ] && continue; i=$((i+1))
  if cut -d, -f1 "$SUMMARY" | grep -qxF "$T"; then echo ">>> [$i/$total] SKIP done: $T"; continue; fi
  echo ">>> [$i/$total] ND (N=$N): $T"
  out=$("$HERE/nd_check.sh" "$REPODIR" "$T" "$PERRUN" "$N" | tail -1)
  v=$(grab verdict "$out"); used=$N
  if [ "$v" = "FLAKY_ND" ]; then
    echo ">>> !! FLINCH: $T -> promoting to N=$PROMOTE"
    out=$("$HERE/nd_check.sh" "$REPODIR" "$T" "$OUTDIR/nd_perrun_promote.csv" "$PROMOTE" | tail -1)
    v=$(grab verdict "$out"); used=$PROMOTE
  fi
  echo "$T,$(grab pass "$out"),$(grab fail "$out"),$(grab missing "$out"),$used,$v" >> "$SUMMARY"
  echo ">>> [$i/$total] $T -> $v"
done < "$QUEUE"
echo ">>> DONE. FLAKY_ND tests:"; grep ',FLAKY_ND$' "$SUMMARY" || echo "  (none)"
