#!/bin/bash
# AgentFlake OD detector v2 -- runs INSIDE container, cwd=/app/source
# NOTE: this ReproFlake surefire fork REQUIRES -Dtest on every invocation (getTest() does new File(test);
# null -> NPE). So we enumerate test classes from target/test-classes and always pass -Dtest.
set -uo pipefail
MODULE="dubbo-rpc/dubbo-rpc-api"
GEN="org.apache.dubbo.rpc.proxy.javassist.JavassistProxyFactory_getInvoker_1_1_Test#testGetInvoker"
N=100; REPLAYS=5
MVNOPTIONS="-Ddependency-check.skip=true -Dgpg.skip=true -DfailIfNoTests=false -Dskip.installnodenpm -Dskip.npm -Dskip.yarn -Dlicense.skip -Dcheckstyle.skip -Drat.skip -Denforcer.skip -Danimal.sniffer.skip -Dmaven.javadoc.skip -Dfindbugs.skip -Dwarbucks.skip -Dmodernizer.skip -Dimpsort.skip -Dmdep.analyze.skip -Dpgpverify.skip -Dxml.skip -Dcobertura.skip=true -Dspotless.check.skip=true"
OUT=/app/source/flaky-result-od; ORDERDIR=/app/source/.od-orders
GEN_CLASS="${GEN%%#*}"; GEN_METHOD="${GEN##*#}"
mkdir -p "$OUT/testlog" "$ORDERDIR"

echo ">> [1/4] enumerate test classes from target/test-classes, then baseline run in testorder mode"
CLASSES=$(cd "$MODULE/target/test-classes" && find . -name "*Test.class" ! -name '*$*' | sed 's|^\./||; s|/|.|g; s|\.class$||' | paste -sd,)
[ -z "$CLASSES" ] && { echo "!! no *Test.class in $MODULE/target/test-classes -- did the module compile tests?"; exit 1; }
echo "   found $(echo "$CLASSES" | tr ',' '\n' | wc -l) test classes"
find "$MODULE" -name "TEST-*.xml" -delete 2>/dev/null
mvn -pl "$MODULE" test -Dsurefire.runOrder=testorder -Dtest="$CLASSES" $MVNOPTIONS > "$OUT/testlog/baseline.log" 2>&1 || true
ls "$MODULE/target/surefire-reports"/TEST-*.xml >/dev/null 2>&1 || { echo "!! baseline produced no reports; see $OUT/testlog/baseline.log"; exit 1; }

echo ">> [2/4] build testlist from baseline reports"
python3 - "$MODULE/target/surefire-reports" "$GEN" > "$OUT/testlist.txt" 2> "$OUT/testlog/testlist-skipped.txt" <<'PY'
import sys, glob, os
from xml.etree import ElementTree as ET
d, gen = sys.argv[1], sys.argv[2]; tests=[]; skipped=[]
for fp in glob.glob(os.path.join(d,"TEST-*.xml")):
    try: root=ET.parse(fp).getroot()
    except Exception: continue
    for tc in root.findall("testcase"):
        c=tc.get("classname"); n=tc.get("name")
        if not c or not n: continue
        if "[" in n or "[" in c: skipped.append(f"{c}#{n}"); continue
        tests.append(f"{c}#{n}")
tests=sorted(set(tests))
if gen not in tests: tests.append(gen)
print("\n".join(tests))
sys.stderr.write(f"{len(skipped)} parameterized/dynamic skipped\n"+"\n".join(sorted(set(skipped))))
PY
NT=$(wc -l < "$OUT/testlist.txt")
echo "   testlist has $NT tests ($(head -1 "$OUT/testlog/testlist-skipped.txt"))"
[ "$NT" -lt 2 ] && { echo "!! testlist has $NT tests (<2) -- enumeration failed, refusing to run a meaningless sweep. See $OUT/testlog/baseline.log"; exit 1; }

echo ">> [3/4] generate $N class-shuffled orders"
python3 - "$OUT/testlist.txt" "$ORDERDIR" "$N" <<'PY'
import sys, os, random
from collections import OrderedDict
tl, outdir, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
tests=[l.strip() for l in open(tl) if l.strip() and "#" in l]
g=OrderedDict()
for t in tests: g.setdefault(t.split("#",1)[0],[]).append(t)
rng=random.Random(42); w=len(str(n))
for i in range(1,n+1):
    cs=list(g.keys()); rng.shuffle(cs)
    order=[x for c in cs for x in g[c]]
    open(os.path.join(outdir,f"order-{i:0{w}d}.txt"),"w").write("\n".join(order)+"\n")
print(f"   wrote {n} orders over {len(g)} classes")
PY

run_order() {  # $1=orderfile $2=tag -> pass|failure|error|missing
  local of="$1" tag="$2" abs; abs="$(readlink -f "$of")"
  find "$MODULE" -name "TEST-*.xml" -delete 2>/dev/null
  mvn -pl "$MODULE" test -Dsurefire.runOrder=testorder -Dtest="$abs" $MVNOPTIONS > "$OUT/testlog/mvn-$tag.log" 2>&1
  local f=""
  while IFS= read -r file; do
    if grep -Pq "<testcase[^>]*\bclassname=\"$GEN_CLASS\"[^>]*\bname=\"$GEN_METHOD\"" "$file" || \
       grep -Pq "<testcase[^>]*\bname=\"$GEN_METHOD\"[^>]*\bclassname=\"$GEN_CLASS\"" "$file"; then f="$file"; break; fi
  done < <(find "$MODULE" -name "TEST-*.xml")
  [[ -z "$f" ]] && { echo "missing"; return; }
  python python-scripts/parse_surefire_report.py "$f" 0 "$GEN" 2>/dev/null | head -n1 | cut -d, -f2 | tr -d '[:space:]'
}

echo ">> [4/4] sanity check on order-001"
first=$(ls "$ORDERDIR"/order-*.txt | head -1); exp=$(wc -l < "$first")
r1=$(run_order "$first" "sanity")
got=$(grep -oP 'Tests run: \K[0-9]+' "$OUT/testlog/mvn-sanity.log" | tail -1)
echo "   order lists $exp tests, maven ran ${got:-0}, generated-test result=$r1"
if [[ -z "$got" || "$got" -lt $((exp/2)) ]]; then
  echo "!! SANITY FAILED: maven ran ${got:-0} of $exp requested tests. -Dtest file form not selecting all. Inspect $OUT/testlog/mvn-sanity.log. Stopping."
  exit 2
fi

echo ">> sweeping $N orders"
RES="$OUT/od-detection-results.csv"; echo "order,result" > "$RES"; sp=""; sf=""
for of in "$ORDERDIR"/order-*.txt; do
  name=$(basename "$of" .txt); res=$(run_order "$of" "$name"); [[ -z "$res" ]] && res=missing
  echo "$name,$res" >> "$RES"; echo "   $name -> $res"
  [[ "$res" == "pass" ]] && sp="$of"
  { [[ "$res" == "failure" || "$res" == "error" ]]; } && sf="$of"
done

echo "==================== RESULT ===================="
if [[ -n "$sp" && -n "$sf" ]]; then
  echo ">> OD CANDIDATE: generated test FLIPS. pass=$(basename "$sp") fail=$(basename "$sf")"
  C="$OUT/od-candidate"; mkdir -p "$C"; cp "$sp" "$C/passing-order.txt"; cp "$sf" "$C/failing-order.txt"
  echo "kind,replay,result" > "$C/replay.csv"
  for k in pass fail; do of="$sp"; [[ "$k" == fail ]] && of="$sf"
    for r in $(seq 1 $REPLAYS); do echo "$k,$r,$(run_order "$of" "replay-$k-$r")" >> "$C/replay.csv"; done
  done
  echo ">> replay confirmation:"; cat "$C/replay.csv"
else
  echo ">> NOT OD across $N orders: generated test result constant."
  echo ">> distribution:"; tail -n +2 "$RES" | cut -d, -f2 | sort | uniq -c
fi
echo ">> artifacts under $OUT"
