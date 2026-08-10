#!/usr/bin/env bash
# ./run_one.sh <zenodo_url> <FQ.Class|auto:FQ.TestClass>
set -u
URL="${1:?url}"; T="${2:?class}"; : "${OPENAI_API_KEY:?export OPENAI_API_KEY}"
CU=2.1.1; ND=2.1.1; IDF=2.0.1-SNAPSHOT; TMO=600
FIX="-Dmaven.compiler.source=8 -Dmaven.compiler.target=8 -Denforcer.skip=true -Dmaven.enforcer.skip=true -Dsurefire.failIfNoSpecifiedTests=false"
SKIP="-DskipTests -Dmaven.test.skip=true -Dmaven.javadoc.skip=true -Dgpg.skip=true"
S="?"; PROJ="?"
cd "$HOME/srse-java" || exit 1
row(){ printf '| ? | %s | %s | files:%s | clean:%s | excl:%s | ID:%s | OD:%s | ND:pending | %s |\n' \
        "$S" "${CLASS:-?}" "${1:-0}" "${2:-0}" "${3:-0}" "${4:-n/a}" "${5:-n/a}" "$6"; }
die(){ row "${1:-0}" 0 0 n/a n/a "NULL: $2"; exit 0; }

Z=$(basename "$URL"); rm -f "$Z"; wget -q -O "$Z" "$URL" || die 0 "download failed"
D="$PWD/${Z%.zip}.dir"; rm -rf "$D"; mkdir -p "$D"; unzip -q "$Z" -d "$D" || die 0 "bad zip"
P=$(find "$D" -maxdepth 4 -name pom.xml | grep -v '/result/' | grep -m1 Flaky) || P=""
[ -z "$P" ] && P=$(find "$D" -maxdepth 4 -name pom.xml | head -1)
[ -z "$P" ] && die 0 "no pom"
M=$(find "$D" -maxdepth 5 -type d -name repository | head -1)
[ -n "$M" ] && cp -rn "$M/." ~/.m2/repository/ 2>/dev/null
PROJ=$(dirname "$P"); cd "$PROJ" || exit 1

if [[ "$T" == auto:* ]]; then
  F=${T#auto:}; F=${F%%#*}; C=${F%Test}
  SRC="src/main/java/$(echo "$C" | tr . /).java"
  [ -f "$SRC" ] || SRC=$(find src/main -name "$(basename "$C").java" 2>/dev/null | head -1)
  [ -n "${SRC:-}" ] && [ -f "$SRC" ] || die 0 "class not found for $F"
  CLASS=$(echo "${SRC#src/main/java/}" | sed 's|/|.|g;s|\.java$||')
else
  CLASS="$T"; SRC="src/main/java/$(echo "$CLASS" | tr . /).java"
  [ -f "$SRC" ] || die 0 "class not found"
fi
S=${CLASS##*.}
G=/tmp/${S}_gen.log; CC=/tmp/${S}_cc.log; BA=/tmp/${S}_base.log; NX=/tmp/${S}_nondex.log; IF=/tmp/${S}_idf.log
echo "CLASS=$CLASS  JDK=$(java -version 2>&1 | head -1)"

PUB=$(grep -cE '^[[:space:]]+(public|protected)[[:space:]]+[A-Za-z<>_.,[:space:]]+\w+[[:space:]]*\(' "$SRC"); PUB=${PUB:-0}
[ "$PUB" -eq 0 ] && die 0 "no public methods"
[ "$PUB" -gt 150 ] && die 0 "monolithic class ($PUB methods)"

sed -i -E 's#<(source|target)>1\.[567]</#<\1>1.8</#g; s#(<maven\.compiler\.(source|target|release)>)[567]<#\18<#g' pom.xml
mvn install $SKIP $FIX >/dev/null 2>&1
ls target/*.jar >/dev/null 2>&1 || die 0 "jar not built (pristine pom)"
python3 "$HOME/srse-java/patch_pom.py" pom.xml || die 0 "pom patch failed"

gen(){ rm -rf /tmp/chatunitest-info/* 2>/dev/null; timeout $TMO mvn io.github.zju-aces-ise:chatunitest-maven-plugin:$CU:class \
        -DselectClass="$CLASS" -DapiKeys="$OPENAI_API_KEY" \
        -Durl=https://api.openai.com/v1/chat/completions $FIX >"$G" 2>&1; }
gen; N=$(find chatunitest-tests -name '*.java' 2>/dev/null | wc -l)
if [ "$N" -eq 0 ] && grep -qE 'class.json|InterruptedIO' "$G"; then
  rm -rf /tmp/chatunitest-info/*; gen; N=$(find chatunitest-tests -name '*.java' 2>/dev/null | wc -l); fi
if [ "$N" -eq 0 ]; then
  grep -q 401 "$G" && die 0 "API 401"
  grep -q "class.json" "$G" && die 0 "class never parsed"
  grep -qE "failed round|Fixing test" "$G" && die 0 "repair rounds exhausted (uncompilable)"
  grep -q "Skip method" "$G" && die 0 "all methods skipped (complex params)"
  die 0 "no tests generated"
fi

mvn -q io.github.zju-aces-ise:chatunitest-maven-plugin:$CU:copy $FIX || die "$N" "copy failed"
mkdir -p ../_dropped ../_excluded
find src/test chatunitest-tests -name '*_Suite.java' -delete 2>/dev/null
for _ in 1 2 3; do
  mvn test-compile $FIX >"$CC" 2>&1
  grep -q "BUILD SUCCESS" "$CC" && break
  BAD=$(grep -oE "src/test/java/[^ :]+\.java" "$CC" | sort -u)
  [ -z "$BAD" ] && break
  for f in $BAD; do echo "drop(no-compile): $f"; mv "$f" ../_dropped/ 2>/dev/null; done
done
grep -q "BUILD SUCCESS" "$CC" || die "$N" "generated tests won't compile"

FI=$(find src/test -name "${S}_*_Test.java" | wc -l)
mvn test -Dtest="${S}_*" $FIX -DfailIfNoTests=false >"$BA" 2>&1
grep -E 'Tests run:' "$BA" | tail -1
R=$(grep -oE 'Tests run: [0-9]+' "$BA" | tail -1 | grep -oE '[0-9]+'); R=${R:-0}
if [ "$R" -eq 0 ]; then
  grep -q "JUnit4Provider" "$BA" && die "$FI" "surefire used JUnit4 provider (jupiter not on classpath)"
  die "$FI" "harness ran 0 tests"
fi
E=0
BROKEN=$(python3 -c "
import glob,xml.etree.ElementTree as X
b=set()
for f in glob.glob('target/surefire-reports/TEST-*.xml'):
    try:
        r=X.parse(f).getroot()
        if int(r.get('failures',0))+int(r.get('errors',0))>0: b.add(r.get('name').split('.')[-1])
    except Exception: pass
print(' '.join(sorted(b)))")
for b in $BROKEN; do
  echo "exclude(broken): $b"
  find src/test -name "$b.java" -exec mv {} ../_excluded/ \; 2>/dev/null
  E=$((E+1))
done
[ "$E" -gt 0 ] && { rm -rf target/test-classes; mvn -q test-compile $FIX; }
CL=$(grep -rh "@Test" src/test --include="${S}_*_Test.java" 2>/dev/null | wc -l); CL=${CL:-0}
[ "$CL" -eq 0 ] && die "$FI" "all $E generated test classes broken"
echo "clean=$CL excluded=$E (originals kept in ../_excluded ../_dropped)"

mvn edu.illinois:nondex-maven-plugin:$ND:nondex -Dtest="${S}_*" $FIX -DfailIfNoTests=false >"$NX" 2>&1
ID=$(grep -ci 'failed on .* configuration' "$NX"); ID=${ID:-0}

rm -rf .dtfixingtools target/test-classes; mvn -q test-compile $FIX
mvn edu.illinois.cs:idflakies-maven-plugin:$IDF:detect -Ddetector.detector_type=random-class-method \
    -Ddt.randomize.rounds=30 $FIX >"$IF" 2>&1
O=$(grep -c "" .dtfixingtools/original-order 2>/dev/null); O=${O:-0}
if [ "$O" -eq 0 ]; then OD="n/a"; else
  OD=0
  find .dtfixingtools -name '*.json' -exec grep -ho '"dts": *\[[^]]*\]' {} \; 2>/dev/null | grep -qE '"dts": *\[[^] ]' && OD=1
fi

V=none
[ "$ID" != "0" ] && V="FLAKY - verify"
[ "$OD" = "1" ] && V="FLAKY - verify"
row "$FI" "$CL" "$E" "$ID" "$OD" "$V"
echo "idflakies tested $O methods | dir: $PROJ"
[ "$V" = "none" ] && printf '%s\t%s\n' "$CLASS" "$PROJ" >> "$HOME/srse-research/nd_queue.tsv"
