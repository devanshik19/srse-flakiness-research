#!/bin/bash
# 04_check_nd.sh -- ND (non-deterministic) flakiness check for ONE generated test.
# Runs the test ALONE, in the SAME order, N times (default 100) and tallies pass/fail.
# This is purely "is this test flaky on repeat, in isolation" -- it says nothing about
# order-dependence (that's the separate OD sweep, against the full suite, later).
#
# Uses the same test-compile-once + explicit-modern-surefire pattern as
# 03_generate_batch.sh's "pass alone" check, for the same reason: this project's pom
# pins an ancient surefire (2.17) that silently runs 0 tests for JUnit5.
#
# Usage: 04_check_nd.sh <repo_dir> <module> <Class#method> <results_csv> [N]
set -uo pipefail
REPODIR="${1:?usage: 04_check_nd.sh <repo_dir> <module> <Class#method> <results_csv> [N]}"
MODULE="${2:?}"
GEN="${3:?}"
RESULTS="${4:?}"
N="${5:-100}"

MVNOPTS="-Ddependency-check.skip=true -Dgpg.skip=true -DfailIfNoTests=false -Dcheckstyle.skip -Drat.skip -Denforcer.skip -Danimal.sniffer.skip -Dmaven.javadoc.skip -Dspotless.check.skip=true -Dmaven.compiler.testSource=8 -Dmaven.compiler.testTarget=8"
log(){ echo ">>> $*"; }

REPODIR="$(cd "$REPODIR" && pwd)"
RESULTS="$(cd "$(dirname "$RESULTS")" && pwd)/$(basename "$RESULTS")"
cd "$REPODIR"
MODARG=(); [ "$MODULE" != "." ] && MODARG=(-pl "$MODULE")

GCLASS="${GEN%%#*}"; GMETHOD="${GEN##*#}"
GSIMPLE="${GCLASS##*.}"

[ -f "$RESULTS" ] || echo "generated_test,run,result" > "$RESULTS"

log "[1/2] test-compile once (nothing changes between the $N repeats)"
mvn "${MODARG[@]}" test-compile $MVNOPTS > "$REPODIR/nd-compile.log" 2>&1 \
  || { echo "!! test-compile failed, see $REPODIR/nd-compile.log"; exit 1; }

log "[2/2] running $GEN alone x$N"
pass=0; fail=0; miss=0
for k in $(seq 1 "$N"); do
  find "$MODULE" -name 'TEST-*.xml' -delete 2>/dev/null
  mvn "${MODARG[@]}" org.apache.maven.plugins:maven-surefire-plugin:3.2.5:test \
    -Dtest="$GCLASS#$GMETHOD" $MVNOPTS > "$REPODIR/nd-run-$k.log" 2>&1
  xml=$(find "$MODULE" -name "TEST-*$GSIMPLE.xml" | head -1)
  if [ -n "$xml" ] && grep -q '<testcase' "$xml" && ! grep -q '<failure\|<error' "$xml"; then
    res=pass; pass=$((pass+1))
  elif [ -n "$xml" ]; then
    res=fail; fail=$((fail+1))
  else
    res=missing; miss=$((miss+1))
  fi
  echo "$GEN,$k,$res" >> "$RESULTS"
  [ "$res" = "pass" ] && rm -f "$REPODIR/nd-run-$k.log"
  log "  [$k/$N] -> $res  (running: pass=$pass fail=$fail missing=$miss)"
done

verdict=NOT_FLAKY
{ [ "$fail" -gt 0 ] || [ "$miss" -gt 0 ]; } && verdict=FLAKY_ND
log "DONE: $GEN pass=$pass fail=$fail missing=$miss total=$N verdict=$verdict"
echo "ND_RESULT=$GEN pass=$pass fail=$fail missing=$miss total=$N verdict=$verdict"
