#!/bin/bash
set -uo pipefail
MODULE="${MODULE:?}"; POLLUTER="${POLLUTER:?}"; VICTIM="${VICTIM:?}"; GEN="${GEN:?}"; N="${N:-30}"
MVNOPTIONS="-Ddependency-check.skip=true -Dgpg.skip=true -DfailIfNoTests=false -Dcheckstyle.skip -Drat.skip -Denforcer.skip -Danimal.sniffer.skip -Dmaven.javadoc.skip -Dspotless.check.skip=true"
OUT=/app/source/flaky-result-od/targeted; mkdir -p "$OUT/testlog"
probe(){
  local label="$1" order="$2" target="$3" tc tm p=0 f=0
  tc="${target%%#*}"; tm="${target##*#}"
  for i in $(seq 1 "$N"); do
    find "$MODULE" -name "TEST-*.xml" -delete 2>/dev/null
    mvn -pl "$MODULE" test -Dsurefire.runOrder=testorder -Dtest="$order" $MVNOPTIONS > "$OUT/testlog/$label-$i.log" 2>&1
    local xf=""
    while IFS= read -r file; do
      if grep -Pq "<testcase[^>]*\bclassname=\"$tc\"[^>]*\bname=\"$tm\"" "$file" || \
         grep -Pq "<testcase[^>]*\bname=\"$tm\"[^>]*\bclassname=\"$tc\"" "$file"; then xf="$file"; break; fi
    done < <(find "$MODULE" -name "TEST-*.xml")
    local r=missing
    [[ -n "$xf" ]] && r=$(python python-scripts/parse_surefire_report.py "$xf" 0 "$target" 2>/dev/null | head -n1 | cut -d, -f2 | tr -d '[:space:]')
    case "$r" in pass) p=$((p+1));; failure|error) f=$((f+1));; esac
  done
  echo "$p $f"
}
read cpf_p cpf_f < <(probe control_polluterFirst "$POLLUTER,$VICTIM" "$VICTIM")
read cvf_p cvf_f < <(probe control_victimFirst "$VICTIM,$POLLUTER" "$VICTIM")
read gpf_p gpf_f < <(probe generated_polluterFirst "$POLLUTER,$GEN" "$GEN")
echo "PROBE_RESULT=ctrlPF=$cpf_p/$cpf_f ctrlVF=$cvf_p/$cvf_f genPF=$gpf_p/$gpf_f"
