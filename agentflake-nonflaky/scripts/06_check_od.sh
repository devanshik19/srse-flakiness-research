#!/bin/bash
# 06_check_od.sh -- OD (order-dependent) flakiness check for ONE generated test.
# Runs the FULL suite (this generated test + all developer tests) under N randomly
# shuffled orders (stock surefire -Dsurefire.runOrder=random -- no custom-patched
# extension needed) and checks whether the target test's outcome changes across
# orders. Uses the same test-compile + explicit-modern-surefire pattern as
# generation/ND, for the same reason: this project's pom pins surefire 2.17, which
# silently runs 0 tests for JUnit5.
#
# This is a coarser first pass than the OD-detection pipeline's replay-confirm
# gate (see od_full.sh/run_od_generic.sh) -- any order that fails just gets flagged
# OD_SUSPECT here rather than auto-replayed to rule out plain non-determinism.
# Treat OD_SUSPECT as "investigate", not "confirmed order-dependent".
#
# Usage: 06_check_od.sh <repo_dir> <module> <Class#method> <results_csv> [N]
set -uo pipefail
REPODIR="${1:?usage: 06_check_od.sh <repo_dir> <module> <Class#method> <results_csv> [N]}"
MODULE="${2:?}"
GEN="${3:?}"
RESULTS="${4:?}"
N="${5:-10}"

MVNOPTS="-Ddependency-check.skip=true -Dgpg.skip=true -DfailIfNoTests=false -Dcheckstyle.skip -Drat.skip -Denforcer.skip -Danimal.sniffer.skip -Dmaven.javadoc.skip -Dspotless.check.skip=true -Dmaven.compiler.testSource=8 -Dmaven.compiler.testTarget=8"
log(){ echo ">>> $*"; }

REPODIR="$(cd "$REPODIR" && pwd)"
RESULTS="$(cd "$(dirname "$RESULTS")" && pwd)/$(basename "$RESULTS")"
cd "$REPODIR"
MODARG=(); [ "$MODULE" != "." ] && MODARG=(-pl "$MODULE")

GCLASS="${GEN%%#*}"; GSIMPLE="${GCLASS##*.}"

[ -f "$RESULTS" ] || echo "generated_test,seed,result" > "$RESULTS"

log "[1/2] test-compile once (live output below)"
mvn "${MODARG[@]}" test-compile $MVNOPTS 2>&1 | tee "$REPODIR/od-compile.log" \
  || { echo "!! test-compile failed, see $REPODIR/od-compile.log"; exit 1; }

log "[2/2] running FULL SUITE under $N random orders, checking $GEN each time"
pass=0; fail=0; miss=0
for k in $(seq 1 "$N"); do
  SEED="$RANDOM$RANDOM"
  find "$MODULE" -name 'TEST-*.xml' -delete 2>/dev/null
  mvn "${MODARG[@]}" org.apache.maven.plugins:maven-surefire-plugin:3.2.5:test \
    -Dsurefire.runOrder=random -Dsurefire.runOrder.random.seed="$SEED" \
    $MVNOPTS > "$REPODIR/od-run-$k.log" 2>&1
  xml=$(find "$MODULE" -name "TEST-*$GSIMPLE.xml" | head -1)
  if [ -n "$xml" ] && grep -q '<testcase' "$xml" && ! grep -q '<failure\|<error' "$xml"; then
    res=pass; pass=$((pass+1))
  elif [ -n "$xml" ]; then
    res=fail; fail=$((fail+1))
  else
    res=missing; miss=$((miss+1))
  fi
  echo "$GEN,$SEED,$res" >> "$RESULTS"
  [ "$res" = "pass" ] && rm -f "$REPODIR/od-run-$k.log"
  log "  [$k/$N] seed=$SEED -> $res"
done

verdict=NOT_OD
[ "$fail" -gt 0 ] && verdict=OD_SUSPECT
{ [ "$pass" -eq 0 ] && [ "$fail" -eq 0 ] && [ "$miss" -gt 0 ]; } && verdict=NO_TESTS_RUN
log "DONE: $GEN pass=$pass fail=$fail missing=$miss total=$N verdict=$verdict"
echo "OD_RESULT=$GEN pass=$pass fail=$fail missing=$miss total=$N verdict=$verdict"
