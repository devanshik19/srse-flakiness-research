#!/bin/bash
# od_full.sh v4 -- AgentFlake end-to-end OD worker for ONE row.
# THE RECIPE (proven on dubbo apiba89f44): restore PRISTINE module pom from the subject zip,
# add Mockito with JUnit EXCLUDED (dubbo's own junit5 stays authoritative -> platform provider,
# no NOOP clash), generate via chatunitest (mvn 3.9.x, explicit plugin goal), pick candidate,
# 100-order sweep + control probes on 3.8.6 custom-surefire. NEVER rewrite junit/surefire in the
# pom -- the ReproFlake extension expects the pristine pom and mutating it forces JUnit4Provider.
set -uo pipefail
CONTAINER="${1:?container}"; SUBJDIR="${2:?subjectDir}"; MODULE="${3:?module}"
POLLUTER="${4:?polluter}"; VICTIM="${5:?victim}"; MODEL="${6:-gpt-4o}"
N_SWEEP="${N_SWEEP:-100}"; N_PROBE="${N_PROBE:-30}"
REPO="$HOME/srse-research"; OUTDIR="$REPO/agentflake-od"; RAW="$OUTDIR/raw/$CONTAINER"
RESULTS="$OUTDIR/results.csv"; mkdir -p "$RAW"
VCLASS="${VICTIM%%#*}"; VMETHOD="${VICTIM##*#}"
CONTAINER_TESTROOT="$SUBJDIR/Flaky/$MODULE/src/test/java"; SUBJECT="${SUBJECT_OVERRIDE:-$(basename "$SUBJDIR")}"
ZIP="$SUBJDIR.zip"
log(){ echo ">>> $*"; }; die(){ echo "!! $*" >&2; exit 1; }
# record a finding row (so no canonical OD row is ever silently dropped) and exit loop-friendly
record_fail(){ # $1=verdict  $2=note   (uses SUBJECT/MODULE/CUT_SIMPLE/FOCAL if set)
  [ -f "$RESULTS" ] || echo "subject,module,focal_method,generated_test,alone,sweep_orders,sweep_pass,ctrl_polluterFirst,ctrl_victimFirst,gen_polluterFirst,od_verdict,notes" > "$RESULTS"
  echo "$SUBJECT,$MODULE,${CUT_SIMPLE:-NA}#${FOCAL:-NA},NONE,na,0,0,na,na,na,$1,$2" >> "$RESULTS"
  echo "!! recorded $1 for $SUBJECT ($2); continuing"; exit 0; }
[ -d "$SUBJDIR/Flaky" ] || die "no Flaky/ under $SUBJDIR"
[ -f "$ZIP" ] || die "subject zip not found: $ZIP (needed to restore pristine pom)"
docker inspect "$CONTAINER" >/dev/null 2>&1 || die "container $CONTAINER not running (docker start $CONTAINER)"
if [ -f "$RESULTS" ] && cut -d, -f1 "$RESULTS" | grep -qx "$SUBJECT"; then
  log "already in results.csv: $SUBJECT -- skipping"; exit 0; fi

log "[0] clean stale staged generated tests"
find "$CONTAINER_TESTROOT" -regextype posix-extended -regex ".*_[0-9]+_[0-9]+_Test\.java" -print -delete 2>/dev/null || true

log "[1] resolve focal for $VICTIM"
DECLFILE="$CONTAINER_TESTROOT/${VCLASS//.//}.java"
if ! grep -Eq "\b$VMETHOD\b" "$DECLFILE" 2>/dev/null; then
  CAND=$(grep -rEl "void[[:space:]]+$VMETHOD[[:space:]]*\(" "$CONTAINER_TESTROOT" 2>/dev/null | head -1)
  [ -n "$CAND" ] && DECLFILE="$CAND"; fi
[ -f "$DECLFILE" ] || die "cannot locate a test file declaring $VMETHOD"
log "    declaring file: $DECLFILE"
FOCLINE=$("$REPO/resolve_focal.sh" "$DECLFILE" "$VMETHOD" "$MODEL" 2>"$RAW/focal.err" | tee "$RAW/focal.log" | grep '^FOCAL=' | tail -1)
FOCAL=$(echo "$FOCLINE" | sed -n 's/^FOCAL=\([^ ]*\).*/\1/p')
FSTATUS=$(echo "$FOCLINE" | sed -n 's/.*STATUS=\([^ ]*\).*/\1/p')
log "    $FOCLINE"
if [ "$FSTATUS" != "agreed" ] || [ -z "$FOCAL" ]; then
  echo "$SUBJECT,$MODULE,$VCLASS#$VMETHOD,FOCAL_UNCONFIRMED,na,0,0,na,na,na,SKIPPED_FOCAL,status=$FSTATUS" >> "$RESULTS"
  echo "!! recorded SKIPPED_FOCAL for $SUBJECT (status=$FSTATUS; see $RAW/focal.log); continuing"; exit 0; fi
# derive the PRODUCTION class-under-test that actually DECLARES the focal method.
# naive "${VCLASS%Test}" breaks on the TestCase/Tests/IT conventions (wildfly etc) -> it
# would hand chatunitest a method inside the TEST class and the plugin NPEs. Instead: strip
# every common test-class suffix to get candidate simple names, then pick the class under
# src/main whose file declares $FOCAL, preferring a name-matched candidate then same package.
SRCMAIN="$SUBJDIR/Flaky/$MODULE/src/main/java"
VPKG="${VCLASS%.*}"; VSIMPLE="${VCLASS##*.}"
CANDS_SIMPLE=$(printf '%s\n' "${VSIMPLE%TestCase}" "${VSIMPLE%Tests}" "${VSIMPLE%Test}" \
  "${VSIMPLE%ITCase}" "${VSIMPLE%IT}" "${VSIMPLE%ITest}" "$VSIMPLE" | awk 'NF && !seen[$0]++')
CUT=""
if [ -d "$SRCMAIN" ]; then
  # 1) a src/main class whose simple name is a stripped candidate AND that declares $FOCAL
  while IFS= read -r cs; do
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      grep -Eq "(^|[^A-Za-z0-9_])$FOCAL[[:space:]]*\(" "$f" || continue
      rel="${f#$SRCMAIN/}"; CUT="${rel%.java}"; CUT="${CUT//\//.}"; break 2
    done < <(find "$SRCMAIN" -name "$cs.java" 2>/dev/null)
  done <<< "$CANDS_SIMPLE"
  # 2) fallback: ANY src/main class declaring $FOCAL, preferring the victim's own package
  if [ -z "$CUT" ]; then
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      rel="${f#$SRCMAIN/}"; c="${rel%.java}"; c="${c//\//.}"
      if [ "${c%.*}" = "$VPKG" ]; then CUT="$c"; break; fi
      [ -z "$CUT" ] && CUT="$c"
    done < <(grep -rlE "(^|[^A-Za-z0-9_])$FOCAL[[:space:]]*\(" "$SRCMAIN" --include='*.java' 2>/dev/null)
  fi
fi
# 3) last resort: suffix-strip the test-class name (old behaviour, TestCase-aware)
if [ -z "$CUT" ]; then
  cs="${VSIMPLE%TestCase}"; cs="${cs%Tests}"; cs="${cs%Test}"; cs="${cs%IT}"
  CUT="$VPKG.$cs"
  log "    (!) no src/main class declares $FOCAL; falling back to name-strip CUT=$CUT"
fi
FOCAL_FQ="$CUT#$FOCAL"; CUT_SIMPLE="${CUT##*.}"
log "    CUT=$CUT focal=$FOCAL -> $FOCAL_FQ"

inC(){ docker exec -w /app/source "$CONTAINER" bash -lc "$1"; }
log "[guard] verify ordering Maven 3.8.6 + custom surefire"
inC 'mvn -v | head -1; ls /usr/share/maven/lib/ext/ | grep -i surefire || echo NO_EXT' | tee "$RAW/mvn-guard.log"
grep -q "Apache Maven 3.8" "$RAW/mvn-guard.log" || die "default mvn not 3.8.x"
grep -qi "surefire.*extension" "$RAW/mvn-guard.log" || die "custom surefire ext missing"
M39=$(inC 'ls -d /opt/*maven*3.9*/bin/mvn 2>/dev/null | head -1' | grep -m1 . || true)
[ -n "$M39" ] || die "Maven 3.9.x for generation not found in container"
log "    generation Maven: $M39"
MVNOPTS="-Ddependency-check.skip=true -Dgpg.skip=true -DfailIfNoTests=false -Dcheckstyle.skip -Drat.skip -Denforcer.skip -Danimal.sniffer.skip -Dmaven.javadoc.skip -Dspotless.check.skip=true"

log "[2] restore PRISTINE module pom from zip + add mockito (junit excluded)"
PDIR="/tmp/pris_$SUBJECT"; rm -rf "$PDIR"; mkdir -p "$PDIR"
if [ "$MODULE" = "." ]; then
  unzip -o "$ZIP" "*Flaky/pom.xml" -d "$PDIR" >/dev/null 2>&1 || unzip -o "$ZIP" "*pom.xml" -d "$PDIR" >/dev/null 2>&1
  PP=$(find "$PDIR" -path "*Flaky/pom.xml" | head -1)
  [ -z "$PP" ] && PP=$(find "$PDIR" -name pom.xml | awk '{print length,$0}' | sort -n | head -1 | cut -d' ' -f2-)
else
  unzip -o "$ZIP" "*/$MODULE/pom.xml" -d "$PDIR" >/dev/null 2>&1 || unzip -o "$ZIP" "*$MODULE/pom.xml" -d "$PDIR" >/dev/null 2>&1
  PP=$(find "$PDIR" -path "*/$MODULE/pom.xml" | head -1)
fi
[ -f "$PP" ] || die "could not extract pristine module pom (module=$MODULE) from $ZIP"
cp "$PP" "$SUBJDIR/Flaky/$MODULE/pom.xml"
[ -f "$REPO/add_mockito.py" ] || die "missing $REPO/add_mockito.py (copy it into srse-research)"
docker cp "$REPO/add_mockito.py" "$CONTAINER:/app/source/add_mockito.py" >/dev/null
inC "python3 add_mockito.py '$MODULE/pom.xml'" | tee "$RAW/pom.log"

log "[3] clean staged/generated + build + generate for $FOCAL_FQ (mvn 3.9.x, explicit plugin goal)"
inC "rm -rf '$MODULE/chatunitest-tests' 2>/dev/null; find '$MODULE/src/test/java' -regextype posix-extended -regex '.*_[0-9]+_[0-9]+_Test\.java' -delete 2>/dev/null; true" >/dev/null
inC "$M39 clean install -DskipTests -pl '$MODULE' -am $MVNOPTS" > "$RAW/build.log" 2>&1 || { tail -30 "$RAW/build.log"; record_fail BUILD_ERROR "mvn 3.9 clean install failed for $FOCAL_FQ (see raw/$CONTAINER/build.log)"; }
inC "ulimit -c 0 2>/dev/null; rm -f $MODULE/core* $MODULE/hs_err_pid*.log 2>/dev/null; $M39 -pl '$MODULE' io.github.zju-aces-ise:chatunitest-maven-plugin:2.1.1:method -DselectMethod='$FOCAL_FQ' -DapiKeys='${OPENAI_API_KEY:-}' -Durl=https://api.openai.com/v1/chat/completions -Dmodel=$MODEL -DtestNumber=1 -DstopWhenSuccess=true -Dcheckstyle.skip=true $MVNOPTS" > "$RAW/generate.log" 2>&1 || true
  if ! inC "find '$MODULE/chatunitest-tests' -name '*_Test.java' 2>/dev/null | grep -q ." ; then tail -30 "$RAW/generate.log"; record_fail GEN_ERROR "chatunitest produced no usable test for $FOCAL_FQ (native crash/no output; see raw/$CONTAINER/generate.log)"; fi

log "[4] pick a generated candidate that passes ALONE (platform provider, plain mvn test)"
GEN=$(inC "set -e; cd '$MODULE'; shopt -s globstar nullglob
  CANDS=\$(ls chatunitest-tests/**/${CUT_SIMPLE}_${FOCAL}_*_Test.java 2>/dev/null)
  [ -z \"\$CANDS\" ] && CANDS=\$(ls chatunitest-tests/**/*_Test.java 2>/dev/null)
  for f in \$CANDS; do
    [ -f \"\$f\" ] || continue
    rel=\${f#chatunitest-tests/}; dest=src/test/java/\$(dirname \"\$rel\")
    mkdir -p \"\$dest\"; cp \"\$f\" \"\$dest/\"
    cls=\$(basename \"\$f\" .java)
    pkg=\$(dirname \"\$rel\" | sed 's|/|.|g'); fqc=\"\$pkg.\$cls\"
    cd /app/source
    find '$MODULE' -name 'TEST-*.xml' -delete 2>/dev/null
    mvn -pl '$MODULE' test -Dtest=\"\$fqc\" $MVNOPTS >/tmp/alone.log 2>&1 || { cd '$MODULE'; continue; }
    xml=\$(find '$MODULE' -name \"TEST-*\$cls.xml\" | head -1)
    if [ -n \"\$xml\" ] && grep -q '<testcase' \"\$xml\" && ! grep -q '<failure\\|<error' \"\$xml\"; then
      cn=\$(grep -oP '<testcase[^>]*\\bclassname=\"\\K[^\"]+' \"\$xml\" | head -1)
      nm=\$(grep -oP '<testcase[^>]*[[:space:]]name=\"\\K[^\"]+' \"\$xml\" | head -1)
      echo \"\$cn#\$nm\"; exit 0; fi
    cd '$MODULE'; done; exit 1" 2>"$RAW/pick.err") || {
  cat "$RAW/pick.err"
  ngen=$(inC "find '$MODULE/chatunitest-tests' -name '*_Test.java' 2>/dev/null | wc -l" | tr -d '[:space:]')
  [ -f "$RESULTS" ] || echo "subject,module,focal_method,generated_test,alone,sweep_orders,sweep_pass,ctrl_polluterFirst,ctrl_victimFirst,gen_polluterFirst,od_verdict,notes" > "$RESULTS"
  if [ "${ngen:-0}" = "0" ]; then
    echo "$SUBJECT,$MODULE,$CUT_SIMPLE#$FOCAL,NONE,na,0,0,na,na,na,GEN_FAILED,chatunitest produced no compiling test for $FOCAL_FQ across all rounds" >> "$RESULTS"
    echo "!! recorded GEN_FAILED for $SUBJECT (generation produced no compiling test); continuing"
  else
    echo "$SUBJECT,$MODULE,$CUT_SIMPLE#$FOCAL,GENERATED,fail,0,0,na,na,na,CANDIDATE_FAILED,generated candidate(s) did not pass alone" >> "$RESULTS"
    echo "!! recorded CANDIDATE_FAILED for $SUBJECT (candidate did not pass alone); continuing"
  fi
  exit 0
}
log "    picked: $GEN"

log "[5] $N_SWEEP-order sweep"
docker cp "$OUTDIR/run_od_generic.sh" "$CONTAINER:/app/source/run_od_generic.sh" >/dev/null
SWEEP=$(inC "MODULE='$MODULE' GEN='$GEN' N='$N_SWEEP' bash run_od_generic.sh" | tee "$RAW/sweep.log" | grep -E '^SWEEP_RESULT=' | tail -1)
SW_VERDICT=$(echo "$SWEEP" | sed -n 's/.*verdict=\([^ ]*\).*/\1/p')
SW_PASS=$(echo "$SWEEP" | sed -n 's/.*pass=\([0-9]*\).*/\1/p')
SW_TOTAL=$(echo "$SWEEP" | sed -n 's/.*total=\([0-9]*\).*/\1/p')
[ -n "$SW_VERDICT" ] || { tail -20 "$RAW/sweep.log"; die "no SWEEP_RESULT"; }
log "    sweep: $SW_PASS/$SW_TOTAL verdict=$SW_VERDICT"

log "[6] control probes N=$N_PROBE"
docker cp "$OUTDIR/run_probe_generic.sh" "$CONTAINER:/app/source/run_probe_generic.sh" >/dev/null
PROBE=$(inC "MODULE='$MODULE' POLLUTER='$POLLUTER' VICTIM='$VICTIM' GEN='$GEN' N='$N_PROBE' bash run_probe_generic.sh" | tee "$RAW/probe.log" | grep -E '^PROBE_RESULT=' | tail -1)
CTRL_PF=$(echo "$PROBE" | sed -n 's/.*ctrlPF=\([^ ]*\).*/\1/p')
CTRL_VF=$(echo "$PROBE" | sed -n 's/.*ctrlVF=\([^ ]*\).*/\1/p')
GEN_PF=$(echo "$PROBE" | sed -n 's/.*genPF=\([^ ]*\).*/\1/p')
log "    probes: ctrlPF=$CTRL_PF ctrlVF=$CTRL_VF genPF=$GEN_PF"

[ -f "$RESULTS" ] || echo "subject,module,focal_method,generated_test,alone,sweep_orders,sweep_pass,ctrl_polluterFirst,ctrl_victimFirst,gen_polluterFirst,od_verdict,notes" > "$RESULTS"
NOTE="focal jaccard+llm agreed; pristine pom + mockito(junit excl); ordering 3.8.6 custom-surefire; coverage/mutation pending"
echo "$SUBJECT,$MODULE,$CUT_SIMPLE#$FOCAL,$(basename "${GEN%%#*}"),pass,$SW_TOTAL,$SW_PASS,$CTRL_PF,$CTRL_VF,$GEN_PF,$SW_VERDICT,$NOTE" >> "$RESULTS"
log "DONE:"; tail -1 "$RESULTS"
