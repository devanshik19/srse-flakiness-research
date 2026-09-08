#!/bin/bash
# 03_generate_batch.sh -- for the first N tests in a non-flaky test list, resolve the
# focal method and generate a ChatUniTest test for it. Adapted from od_full.sh steps
# [1]-[4] (focal resolution -> mockito+jupiter pom patch -> chatunitest generate ->
# pick a candidate that passes alone), with the victim/polluter/probe machinery removed
# (there is no polluter in the non-flaky pipeline). No Docker -- runs on the host mvn.
#
# Usage: 03_generate_batch.sh <repo_dir> <module> <non_flaky_tests.txt> <results_csv> [N] [model]
#   module: "." for a single-module project, otherwise the module's relative path
set -uo pipefail
REPODIR="${1:?usage: 03_generate_batch.sh <repo_dir> <module> <non_flaky_tests.txt> <results_csv> [N] [model]}"
MODULE="${2:?}"
TESTLIST="${3:?}"
RESULTS="${4:?}"
N="${5:-5}"
MODEL="${6:-gpt-4o}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
: "${OPENAI_API_KEY:?set OPENAI_API_KEY first}"

MVNOPTS="-Ddependency-check.skip=true -Dgpg.skip=true -DfailIfNoTests=false -Dcheckstyle.skip -Drat.skip -Denforcer.skip -Danimal.sniffer.skip -Dmaven.javadoc.skip -Dspotless.check.skip=true -Dmaven.compiler.testSource=8 -Dmaven.compiler.testTarget=8"
log(){ echo ">>> $*"; }

# resolve to absolute paths BEFORE cd'ing into REPODIR -- TESTLIST/RESULTS were given
# relative to the original cwd, not to REPODIR, and would silently break otherwise.
REPODIR="$(cd "$REPODIR" && pwd)"
TESTLIST="$(cd "$(dirname "$TESTLIST")" && pwd)/$(basename "$TESTLIST")"
RESULTS="$(cd "$(dirname "$RESULTS")" && pwd)/$(basename "$RESULTS")"

cd "$REPODIR"
POMFILE="pom.xml"; [ "$MODULE" != "." ] && POMFILE="$MODULE/pom.xml"
MODARG=(); [ "$MODULE" != "." ] && MODARG=(-pl "$MODULE")
SRCMAIN="src/main/java"; [ "$MODULE" != "." ] && SRCMAIN="$MODULE/src/main/java"
SRCTEST="src/test/java"; [ "$MODULE" != "." ] && SRCTEST="$MODULE/src/test/java"
CUTESTS="chatunitest-tests"; [ "$MODULE" != "." ] && CUTESTS="$MODULE/chatunitest-tests"

[ -f "$RESULTS" ] || echo "victim_test,focal_status,cut,focal,generated_test,alone_result,notes" > "$RESULTS"

log "[setup] add mockito + junit-jupiter (idempotent) to $POMFILE"
python3 "$HERE/add_mockito.py" "$POMFILE"

log "[setup] clean any stale generated test files left over from a previous run"
find "$SRCTEST" -regextype posix-extended -regex '.*_[0-9]+_[0-9]+_Test\.java' -print -delete 2>/dev/null

log "[setup] one-time module build (skip tests)"
mvn "${MODARG[@]}" clean install -DskipTests $MVNOPTS 2>&1 | tee "$REPODIR/build.log" \
  || { echo "!! build failed, see $REPODIR/build.log"; exit 1; }

i=0
while IFS= read -r VICTIM; do
  [ -z "$VICTIM" ] && continue
  i=$((i+1)); [ "$i" -gt "$N" ] && break
  VCLASS="${VICTIM%%#*}"; VMETHOD="${VICTIM##*#}"
  log "[$i/$N] $VICTIM"

  DECLFILE="$SRCTEST/${VCLASS//.//}.java"
  if [ ! -f "$DECLFILE" ]; then
    echo "$VICTIM,DECL_NOT_FOUND,,,,,could not locate declaring file $DECLFILE" >> "$RESULTS"
    continue
  fi

  FOCLINE=$("$HERE/resolve_focal.sh" "$DECLFILE" "$VMETHOD" "$MODEL" 2>"$REPODIR/focal-$i.err" \
    | tee "$REPODIR/focal-$i.log" | grep '^FOCAL=' | tail -1)
  FOCAL=$(echo "$FOCLINE" | sed -n 's/^FOCAL=\([^ ]*\).*/\1/p')
  FSTATUS=$(echo "$FOCLINE" | sed -n 's/.*STATUS=\([^ ]*\).*/\1/p')
  log "    $FOCLINE"
  if [ "$FSTATUS" != "agreed" ] || [ -z "$FOCAL" ]; then
    echo "$VICTIM,${FSTATUS:-error},,,,,see focal-$i.log" >> "$RESULTS"
    continue
  fi

  # derive the production class-under-test that actually declares $FOCAL (same
  # algorithm as od_full.sh: try stripped test-class-name candidates first, then
  # any src/main class declaring the method, then fall back to name-stripping).
  VPKG="${VCLASS%.*}"; VSIMPLE="${VCLASS##*.}"
  CANDS_SIMPLE=$(printf '%s\n' "${VSIMPLE%TestCase}" "${VSIMPLE%Tests}" "${VSIMPLE%Test}" \
    "${VSIMPLE%ITCase}" "${VSIMPLE%IT}" "${VSIMPLE%ITest}" "$VSIMPLE" | awk 'NF && !seen[$0]++')
  CUT=""
  if [ -d "$SRCMAIN" ]; then
    while IFS= read -r cs; do
      while IFS= read -r f; do
        [ -z "$f" ] && continue
        grep -Eq "(^|[^A-Za-z0-9_])$FOCAL[[:space:]]*\(" "$f" || continue
        rel="${f#$SRCMAIN/}"; CUT="${rel%.java}"; CUT="${CUT//\//.}"; break 2
      done < <(find "$SRCMAIN" -name "$cs.java" 2>/dev/null)
    done <<< "$CANDS_SIMPLE"
    if [ -z "$CUT" ]; then
      while IFS= read -r f; do
        [ -z "$f" ] && continue
        rel="${f#$SRCMAIN/}"; c="${rel%.java}"; c="${c//\//.}"
        if [ "${c%.*}" = "$VPKG" ]; then CUT="$c"; break; fi
        [ -z "$CUT" ] && CUT="$c"
      done < <(grep -rlE "(^|[^A-Za-z0-9_])$FOCAL[[:space:]]*\(" "$SRCMAIN" --include='*.java' 2>/dev/null)
    fi
  fi
  if [ -z "$CUT" ]; then
    cs="${VSIMPLE%TestCase}"; cs="${cs%Tests}"; cs="${cs%Test}"; cs="${cs%IT}"
    CUT="$VPKG.$cs"
    log "    (!) no src/main class declares $FOCAL; falling back to name-strip CUT=$CUT"
  fi
  FOCAL_FQ="$CUT#$FOCAL"; CUT_SIMPLE="${CUT##*.}"
  log "    CUT=$CUT focal=$FOCAL -> $FOCAL_FQ"

  rm -rf "$CUTESTS" 2>/dev/null
  ulimit -c 0 2>/dev/null; rm -f "$MODULE"/core* "$MODULE"/hs_err_pid*.log 2>/dev/null

  log "    generating (ChatUniTest, live output below)..."
  mvn "${MODARG[@]}" io.github.zju-aces-ise:chatunitest-maven-plugin:2.1.1:method \
    -DselectMethod="$FOCAL_FQ" -DapiKeys="$OPENAI_API_KEY" \
    -Durl=https://api.openai.com/v1/chat/completions -Dmodel="$MODEL" \
    -DtestNumber=1 -DstopWhenSuccess=true -Dcheckstyle.skip=true $MVNOPTS \
    2>&1 | tee "$REPODIR/generate-$i.log" | grep -E '^\[CHATUNITEST\]|Generating test for method|round [0-9]|ERROR' || true

  if ! find "$CUTESTS" -name '*_Test.java' 2>/dev/null | grep -q .; then
    echo "$VICTIM,agreed,$CUT,$FOCAL,NONE,na,GEN_FAILED see generate-$i.log" >> "$RESULTS"
    continue
  fi

  # pick a candidate that passes alone (same logic as od_full.sh step [4], no docker)
  GEN=""
  shopt -s globstar nullglob
  CANDS=$(ls "$CUTESTS"/**/"${CUT_SIMPLE}_${FOCAL}"_*_Test.java 2>/dev/null)
  [ -z "$CANDS" ] && CANDS=$(ls "$CUTESTS"/**/*_Test.java 2>/dev/null)
  for f in $CANDS; do
    [ -f "$f" ] || continue
    rel="${f#$CUTESTS/}"; dest="$SRCTEST/$(dirname "$rel")"
    mkdir -p "$dest"; cp "$f" "$dest/"
    copied="$dest/$(basename "$f")"
    cls=$(basename "$f" .java); pkg=$(dirname "$rel" | sed 's|/|.|g'); fqc="$pkg.$cls"
    find "$MODULE" -name 'TEST-*.xml' -delete 2>/dev/null
    # test-compile via the project's own compiler, then run via an explicit MODERN
    # surefire (bypassing whatever old version the pom pins -- e.g. Java-WebSocket
    # pins surefire 2.17, which predates JUnit5 and silently runs 0 tests instead
    # of erroring). Chaining phase+goal in one invocation so it shares the reactor.
    log "    checking candidate $fqc passes alone (live output below)..."
    if ! mvn "${MODARG[@]}" test-compile org.apache.maven.plugins:maven-surefire-plugin:3.2.5:test \
      -Dtest="$fqc" $MVNOPTS 2>&1 | tee "$REPODIR/alone-$i.log" | grep -E '^\[ERROR\]|Tests run:|BUILD (SUCCESS|FAILURE)'; then
      mkdir -p "$REPODIR/generated-failed/round-$i"; mv "$copied" "$REPODIR/generated-failed/round-$i/"
      continue   # this candidate failed (compile or test) -- archive it out of src/test/java, don't leave it there
    fi
    xml=$(find "$MODULE" -name "TEST-*$cls.xml" | head -1)
    if [ -n "$xml" ] && grep -q '<testcase' "$xml" && ! grep -q '<failure\|<error' "$xml"; then
      cn=$(grep -oP '<testcase[^>]*\bclassname="\K[^"]+' "$xml" | head -1)
      nm=$(grep -oP '<testcase[^>]*[[:space:]]name="\K[^"]+' "$xml" | head -1)
      GEN="$cn#$nm"; break   # winner -- keep $copied in place permanently
    fi
    mkdir -p "$REPODIR/generated-failed/round-$i"; mv "$copied" "$REPODIR/generated-failed/round-$i/"
  done
  shopt -u globstar nullglob

  if [ -z "$GEN" ]; then
    ngen=$(find "$CUTESTS" -name '*_Test.java' 2>/dev/null | wc -l)
    if [ "$ngen" = "0" ]; then
      echo "$VICTIM,agreed,$CUT,$FOCAL,NONE,na,GEN_FAILED (no compiling test)" >> "$RESULTS"
    else
      echo "$VICTIM,agreed,$CUT,$FOCAL,GENERATED,fail,CANDIDATE_FAILED (did not pass alone)" >> "$RESULTS"
    fi
    continue
  fi

  log "    generated: $GEN"
  echo "$VICTIM,agreed,$CUT,$FOCAL,$GEN,pass," >> "$RESULTS"
done < "$TESTLIST"

log "DONE. results -> $RESULTS"
