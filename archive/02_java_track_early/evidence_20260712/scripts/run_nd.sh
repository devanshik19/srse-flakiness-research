#!/usr/bin/env bash
# run_nd.sh — ND flakiness loop ONLY, reusing Phase-1 compiled tests.
# Usage:  ./run_nd.sh <fully.qualified.ClassName> [NDN] [projectFlakyDir]
set -u
CLASS="${1:?need fully-qualified class}"
NDN="${2:-100}"
PROJ="${3:-$PWD}"
SHORT="${CLASS##*.}"
SRCFIX="-Dmaven.compiler.source=8 -Dmaven.compiler.target=8 -Dmaven.compiler.release=8 -Dversion.jdk=1.8"
cd "$PROJ" || { echo "no such dir: $PROJ"; exit 1; }

TEST_CLASSES=$(find src/test -name "${SHORT}_*_Test.java" -exec basename {} .java \; 2>/dev/null)
if [ -z "$TEST_CLASSES" ]; then
    echo "| ND | $SHORT | no clean tests on disk — was this a real result in Phase 1? |"; exit 0
fi

mvn -q test-compile $SRCFIX >/dev/null 2>&1

echo "== ND loop for $SHORT ($NDN iterations each) =="
ND_FLAKY=0; ND_REPORT=""
for t in $TEST_CLASSES; do
    pass=0; fail=0
    mvn surefire:test -Dtest="$t" -DfailIfNoTests=false >/dev/null 2>&1
    for i in $(seq 1 "$NDN"); do
        if mvn -o surefire:test -Dtest="$t" -Dsurefire.includes="**/$t.java" $SRCFIX -DfailIfNoTests=false \
             >"/tmp/${SHORT}_nd.log" 2>&1 && grep -q "BUILD SUCCESS" "/tmp/${SHORT}_nd.log"; then
            pass=$((pass+1))
        else
            fail=$((fail+1))
        fi
    done
    echo "  $t: $pass pass / $fail fail (of $NDN)"
    if [ "$pass" -gt 0 ] && [ "$fail" -gt 0 ]; then
        ND_FLAKY=$((ND_FLAKY+1)); ND_REPORT="$ND_REPORT $t($fail/$NDN)"
    fi
done
echo "ND-flaky classes: $ND_FLAKY  [$ND_REPORT]"
echo "ND-ROW: $SHORT  ND:$ND_FLAKY  detail:[$ND_REPORT]"
