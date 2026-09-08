#!/bin/bash
# 01_collect_tests.sh -- clone a subject at a pinned commit and enumerate every test
# that actually ran, via surefire reports (Shinae's mentor's approach: checkout the
# commit, get the full test list, THEN exclude the known-flaky ones).
#
# Usage: 01_collect_tests.sh <repo_url> <commit> <work_dir> [module]
#   module: relative path to the Maven module to test (default: repo root ".")
#
# Output: <work_dir>/all_tests.txt  -- one "fully.qualified.Class#method" per line
set -uo pipefail
REPO_URL="${1:?usage: 01_collect_tests.sh <repo_url> <commit> <work_dir> [module]}"
COMMIT="${2:?need commit sha}"
WORKDIR="${3:?need a work dir to clone into}"
MODULE="${4:-.}"
MVNOPTS="-Ddependency-check.skip=true -Dgpg.skip=true -DfailIfNoTests=false -Dcheckstyle.skip -Drat.skip -Denforcer.skip -Danimal.sniffer.skip -Dmaven.javadoc.skip -Dspotless.check.skip=true"

log(){ echo ">>> $*"; }

if [ -d "$WORKDIR/.git" ]; then
  log "reusing existing clone at $WORKDIR"
else
  log "cloning $REPO_URL -> $WORKDIR"
  git clone "$REPO_URL" "$WORKDIR"
fi
WORKDIR="$(cd "$WORKDIR" && pwd)"
cd "$WORKDIR"
log "checkout $COMMIT"
git checkout --quiet "$COMMIT" || { echo "!! checkout failed"; exit 1; }

MODARG=()
[ "$MODULE" != "." ] && MODARG=(-pl "$MODULE")

log "mvn test (this is expected to take a while and some tests may fail -- that's fine, we just want surefire reports written for whatever DID run)"
mvn "${MODARG[@]}" test $MVNOPTS > "$WORKDIR/mvn-test.log" 2>&1
echo "   mvn exit=$? (see $WORKDIR/mvn-test.log if you want to check what failed/skipped)"

log "enumerating tests from surefire-reports"
python3 - <<'PY' > "$WORKDIR/all_tests.txt"
import glob
import xml.etree.ElementTree as ET

for report in glob.glob("**/target/surefire-reports/TEST-*.xml", recursive=True):
    try:
        root = ET.parse(report).getroot()
    except Exception:
        continue
    for test in root.iter("testcase"):
        cn, nm = test.get("classname"), test.get("name")
        if cn and nm and "[" not in nm:
            print(f"{cn}#{nm}")
PY
sort -u -o "$WORKDIR/all_tests.txt" "$WORKDIR/all_tests.txt"
N=$(wc -l < "$WORKDIR/all_tests.txt")
log "wrote $N unique tests -> $WORKDIR/all_tests.txt"
