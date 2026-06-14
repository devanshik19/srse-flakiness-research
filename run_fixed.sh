#!/bin/bash
INSTANCE_ID="$1"
BASE_DIR=~/swt_runs
PATCH_DIR=~/patches
LOG_DIR=~/loop_logs
RESULTS=~/srse-research/results.csv

mkdir -p "$BASE_DIR" "$PATCH_DIR" "$LOG_DIR"
echo "=== $INSTANCE_ID ==="

INFO=$(python3 ~/srse-research/helpers/get_instance_info4.py "$INSTANCE_ID")
if [ "$INFO" == "NOTFOUND" ]; then
    echo "$INSTANCE_ID,,,,,,NOT_FOUND" >> "$RESULTS"
    exit 0
fi

REPO=$(echo "$INFO" | cut -d'|' -f1)
COMMIT=$(echo "$INFO" | cut -d'|' -f2)
TEST_FILE=$(echo "$INFO" | cut -d'|' -f3)
TEST_NAME=$(echo "$INFO" | cut -d'|' -f4)
REPO_NAME=$(echo "$REPO" | cut -d'/' -f2)
REPO_DIR="$BASE_DIR/$REPO_NAME"

if [ ! -d "$REPO_DIR" ]; then
    git clone "https://github.com/$REPO.git" "$REPO_DIR" || { echo "$INSTANCE_ID,$REPO,,,,,CLONE_FAIL" >> "$RESULTS"; exit 0; }
fi

cd "$REPO_DIR" || exit 0
git checkout . 2>/dev/null
git clean -fd 2>/dev/null
git checkout "$COMMIT" 2>/dev/null || { echo "$INSTANCE_ID,$REPO,,,,,CHECKOUT_FAIL" >> "$RESULTS"; exit 0; }

git apply "$PATCH_DIR/${INSTANCE_ID}_golden.patch" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "$INSTANCE_ID,$REPO,$TEST_FILE,$TEST_NAME,,,GOLDEN_PATCH_FAIL" >> "$RESULTS"
    exit 0
fi

git apply "$PATCH_DIR/${INSTANCE_ID}_agent.patch" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "$INSTANCE_ID,$REPO,$TEST_FILE,$TEST_NAME,,,AGENT_PATCH_FAIL" >> "$RESULTS"
    exit 0
fi

RUN_LOG="$LOG_DIR/${INSTANCE_ID}_runs.csv"
> "$RUN_LOG"
PASS_COUNT=0
FAIL_COUNT=0

for i in $(seq 1 100); do
    if PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 timeout 60 python3 -m pytest "${TEST_FILE}::${TEST_NAME}" --assert=plain -q > "$LOG_DIR/${INSTANCE_ID}_run${i}.log" 2>&1; then
        echo "$i,PASSED" >> "$RUN_LOG"
        PASS_COUNT=$((PASS_COUNT+1))
    else
        echo "$i,FAILED" >> "$RUN_LOG"
        FAIL_COUNT=$((FAIL_COUNT+1))
    fi
done

if [ "$PASS_COUNT" -gt 0 ] && [ "$FAIL_COUNT" -gt 0 ]; then
    LOOP_STATUS="FLAKY"
elif [ "$PASS_COUNT" -eq 100 ]; then
    LOOP_STATUS="ALWAYS_PASS"
else
    LOOP_STATUS="ALWAYS_FAIL"
fi

IPFLAKIES_RESULT="SKIPPED"
for CFG in pytest.ini setup.cfg tox.ini; do
    if [ -f "$CFG" ] && grep -q "testpaths" "$CFG"; then
        cp "$CFG" "$CFG.bak"
        sed -i "s|^testpaths.*|testpaths = $TEST_FILE|" "$CFG"
        source ~/xarray/ipflakies-env/bin/activate
        pip install -e . > /dev/null 2>&1
        pip install Cython "numpy<2.0" > /dev/null 2>&1
        IPF_OUT=$(timeout 300 env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m ipflakies -i 10 2>&1)
        FLAKY_LINE=$(echo "$IPF_OUT" | grep -oE '^[0-9]+ flaky')
        IPFLAKIES_RESULT=$(echo "$FLAKY_LINE" | grep -oE '^[0-9]+')
        [ -z "$IPFLAKIES_RESULT" ] && IPFLAKIES_RESULT="ERROR"
        deactivate
        mv "$CFG.bak" "$CFG"
        break
    fi
done

echo "$INSTANCE_ID,$REPO,$TEST_FILE,$TEST_NAME,${PASS_COUNT}/100,$LOOP_STATUS,IPF:$IPFLAKIES_RESULT" >> "$RESULTS"
echo "$INSTANCE_ID -> 100x:$LOOP_STATUS ($PASS_COUNT/100), iPFlakies:$IPFLAKIES_RESULT"
