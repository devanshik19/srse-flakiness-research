#!/bin/bash
# 05_check_id_nondex.sh -- ID (implementation-dependent) flakiness check via NonDex.
# NonDex randomizes JDK-unspecified behavior (HashMap/HashSet iteration order, etc.)
# across repeated runs and reports whether the test's outcome depends on it -- distinct
# from ND (repeat-same-order-in-isolation) and OD (order vs the rest of the suite).
#
# Usage: 05_check_id_nondex.sh <repo_dir> <module> <Class#method> <results_csv> [nondexRuns]
set -uo pipefail
REPODIR="${1:?usage: 05_check_id_nondex.sh <repo_dir> <module> <Class#method> <results_csv> [nondexRuns]}"
MODULE="${2:?}"
GEN="${3:?}"
RESULTS="${4:?}"
RUNS="${5:-10}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MVNOPTS="-Ddependency-check.skip=true -Dgpg.skip=true -DfailIfNoTests=false -Dcheckstyle.skip -Drat.skip -Denforcer.skip -Danimal.sniffer.skip -Dmaven.javadoc.skip -Dspotless.check.skip=true -Dmaven.compiler.testSource=8 -Dmaven.compiler.testTarget=8"
log(){ echo ">>> $*"; }

REPODIR="$(cd "$REPODIR" && pwd)"
RESULTS="$(cd "$(dirname "$RESULTS")" && pwd)/$(basename "$RESULTS")"
cd "$REPODIR"
MODARG=(); [ "$MODULE" != "." ] && MODARG=(-pl "$MODULE")
POMFILE="pom.xml"; [ "$MODULE" != "." ] && POMFILE="$MODULE/pom.xml"

[ -f "$RESULTS" ] || echo "generated_test,nondex_runs,result,notes" > "$RESULTS"

SAFE=$(echo "$GEN" | tr '#/.' '___')
LOG="$REPODIR/nondex-$SAFE.log"

# NonDex resolves maven-surefire-plugin's version from the POM itself (via
# mojo-executor) and offers no CLI override -- unlike our own generation/ND
# scripts, we can't just invoke a different plugin coordinate directly. So we
# temporarily bump it in the pom, and ALWAYS revert on exit (even on crash/Ctrl-C)
# via trap, so this never leaks into any other step of the pipeline.
cp "$POMFILE" "$POMFILE.bak-nondex"
trap 'mv -f "$POMFILE.bak-nondex" "$POMFILE" 2>/dev/null' EXIT
log "temporarily bumping maven-surefire-plugin in $POMFILE for this NonDex run only"
python3 "$HERE/bump_surefire.py" "$POMFILE" 3.2.5

log "running NonDex on $GEN ($RUNS randomized configurations, live progress below)"
mvn "${MODARG[@]}" edu.illinois:nondex-maven-plugin:2.2.5:nondex \
  -Dtest="$GEN" -DnondexRuns="$RUNS" $MVNOPTS 2>&1 | tee "$LOG" \
  | grep -E 'nondexSeed=|Tests run:|failed with this configuration|NonDex SUMMARY|BUILD (SUCCESS|FAILURE)'
RC=$?

# guard against the "BUILD SUCCESS but 0 tests actually ran" trap we've now hit
# multiple times in this pipeline (old surefire silently not recognizing JUnit5) --
# sum every "Tests run: N" line in the log; if it's all zeros, NOTHING was verified.
TESTS_RUN_TOTAL=$(grep -oP 'Tests run: \K[0-9]+' "$LOG" | awk '{s+=$1} END{print s+0}')

if [ "$TESTS_RUN_TOTAL" -eq 0 ]; then
  echo "$GEN,$RUNS,NO_TESTS_RUN,NonDex reported 0 tests across all $RUNS configs -- see $LOG" >> "$RESULTS"
  log "NO_TESTS_RUN: $GEN -- NonDex never actually executed the test, do not trust exit code alone"
elif [ "$RC" -eq 0 ]; then
  echo "$GEN,$RUNS,NOT_FLAKY_ID," >> "$RESULTS"
  log "NOT_FLAKY_ID: $GEN ($TESTS_RUN_TOTAL test executions across $RUNS configs, all passed) -- log: $LOG"
else
  echo "$GEN,$RUNS,FLAKY_ID,exit=$RC see $LOG" >> "$RESULTS"
  log "FLAKY_ID: $GEN ($TESTS_RUN_TOTAL test executions across $RUNS configs, some failed, exit=$RC)"
fi
