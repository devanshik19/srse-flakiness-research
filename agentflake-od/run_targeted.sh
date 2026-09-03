#!/bin/bash
# Targeted OD probe: run (preceding, target) in exact order N times, like od_statistics_generator.sh
set -uo pipefail
MODULE="dubbo-rpc/dubbo-rpc-api"; N="${1:-30}"
MVNOPTIONS="-Ddependency-check.skip=true -Dgpg.skip=true -DfailIfNoTests=false -Dskip.installnodenpm -Dskip.npm -Dskip.yarn -Dlicense.skip -Dcheckstyle.skip -Drat.skip -Denforcer.skip -Danimal.sniffer.skip -Dmaven.javadoc.skip -Dfindbugs.skip -Dwarbucks.skip -Dmodernizer.skip -Dimpsort.skip -Dmdep.analyze.skip -Dpgpverify.skip -Dxml.skip -Dcobertura.skip=true -Dspotless.check.skip=true"
POLLUTER="org.apache.dubbo.rpc.RpcContextTest#testAsync"
VICTIM="org.apache.dubbo.rpc.proxy.javassist.JavassistProxyFactoryTest#testGetInvoker"
GEN="org.apache.dubbo.rpc.proxy.javassist.JavassistProxyFactory_getInvoker_1_1_Test#testGetInvoker"
OUT=/app/source/flaky-result-od/targeted; mkdir -p "$OUT/testlog"

probe() {  # $1=label $2=order-string(comma) $3=target(class#method)
  local label="$1" order="$2" target="$3" tc tm p=0 f=0 e=0 m=0
  tc="${target%%#*}"; tm="${target##*#}"
  echo "---- $label : order = $order ----"
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
    echo "   $label iter $i -> $r"
    case "$r" in pass) ((p++));; failure) ((f++));; error) ((e++));; *) ((m++));; esac
  done
  echo ">> $label SUMMARY: pass=$p failure=$f error=$e missing=$m (N=$N)"
  echo "$label,$p,$f,$e,$m,$N" >> "$OUT/targeted-summary.csv"
}

echo "experiment,pass,failure,error,missing,N" > "$OUT/targeted-summary.csv"
probe "control_polluterFirst" "$POLLUTER,$VICTIM" "$VICTIM"
probe "control_victimFirst"   "$VICTIM,$POLLUTER" "$VICTIM"
probe "generated_polluterFirst" "$POLLUTER,$GEN"  "$GEN"
echo "==================== TARGETED SUMMARY ===================="
cat "$OUT/targeted-summary.csv"
