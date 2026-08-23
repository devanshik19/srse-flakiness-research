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
if [ -z "$TEST_NAME" ]; then
    echo "$INSTANCE_ID,$REPO,$TEST_FILE,,,,NO_TEST_NAME" >> "$RESULTS"
    exit 0
fi
REPO_NAME=$(echo "$REPO" | cut -d'/' -f2)
REPO_DIR="$BASE_DIR/$REPO_NAME"

# django can't run under plain pytest (needs its own settings-configured
# runner). Record explicitly as incompatible rather than fake ALWAYS_FAIL.
case "$REPO_NAME" in
    django)
        echo "$INSTANCE_ID,$REPO,$TEST_FILE,$TEST_NAME,,NOT_COMPATIBLE,IPF:NOT_COMPATIBLE" >> "$RESULTS"
        echo "$INSTANCE_ID -> NOT_COMPATIBLE (plain pytest unsupported for django)"
        exit 0
        ;;
esac

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
    if PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 timeout 60 ~/xarray/ipflakies-env/bin/python3 -m pytest "${TEST_FILE}::${TEST_NAME}" --assert=plain -q > "$LOG_DIR/${INSTANCE_ID}_run${i}.log" 2>&1; then
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
CONFIG_SCOPED=0

# matplotlib's per-commit "pip install -e ." recompiles C extensions — too
# slow/fragile for iPFlakies. The 100x loop runs fine, but skip order-dependence.
if [ "$REPO_NAME" == "matplotlib" ]; then
    IPFLAKIES_RESULT="NOT_COMPATIBLE"
    CONFIG_SCOPED=1
fi

# Try pyproject.toml first (TOML syntax, handled separately from sed-based INI)
if [ "$CONFIG_SCOPED" -eq 0 ] && [ -f "pyproject.toml" ] && grep -q "testpaths" "pyproject.toml"; then
    cp "pyproject.toml" "pyproject.toml.bak"
    python3 -c "
import re
with open('pyproject.toml') as f:
    content = f.read()
content = re.sub(r'testpaths\s*=.*', 'testpaths = [\"$TEST_FILE\"]', content)
with open('pyproject.toml', 'w') as f:
    f.write(content)
"
    source ~/xarray/ipflakies-env/bin/activate
    pip install -e . --break-system-packages > /dev/null 2>&1
    pip install Cython "numpy<2.0" --break-system-packages > /dev/null 2>&1
    IPF_LOG="$LOG_DIR/${INSTANCE_ID}_ipflakies.log"
    COLUMNS=80 PYTHONUNBUFFERED=1 timeout 900 python3 -m ipflakies -i 10 > "$IPF_LOG" 2>&1
    if [ -f "ipflakies_result/flakies.json" ]; then
        IPFLAKIES_RESULT=$(python3 -c "import json; data=json.load(open('ipflakies_result/flakies.json')); print(len([k for k in data if k != 'time']))")
        [ -z "$IPFLAKIES_RESULT" ] && IPFLAKIES_RESULT="ERROR"
    else
        IPFLAKIES_RESULT="NO_RESULT_FILE"
    fi
    deactivate
    mv "pyproject.toml.bak" "pyproject.toml"
    CONFIG_SCOPED=1
fi

# Fall back to INI-style config files
if [ "$CONFIG_SCOPED" -eq 0 ]; then
    for CFG in pytest.ini setup.cfg tox.ini; do
        if [ -f "$CFG" ] && grep -q "testpaths" "$CFG"; then
            cp "$CFG" "$CFG.bak"
            sed -i "s|^testpaths.*|testpaths = $TEST_FILE|" "$CFG"
            source ~/xarray/ipflakies-env/bin/activate
            pip install -e . --break-system-packages > /dev/null 2>&1
            pip install Cython "numpy<2.0" --break-system-packages > /dev/null 2>&1
            IPF_LOG="$LOG_DIR/${INSTANCE_ID}_ipflakies.log"
            COLUMNS=80 PYTHONUNBUFFERED=1 timeout 900 python3 -m ipflakies -i 10 > "$IPF_LOG" 2>&1
            if [ -f "ipflakies_result/flakies.json" ]; then
                IPFLAKIES_RESULT=$(python3 -c "import json; data=json.load(open('ipflakies_result/flakies.json')); print(len([k for k in data if k != 'time']))")
                [ -z "$IPFLAKIES_RESULT" ] && IPFLAKIES_RESULT="ERROR"
            else
                IPFLAKIES_RESULT="NO_RESULT_FILE"
            fi
            deactivate
            mv "$CFG.bak" "$CFG"
            CONFIG_SCOPED=1
            break
        fi
    done
fi

echo "$INSTANCE_ID,$REPO,$TEST_FILE,$TEST_NAME,${PASS_COUNT}/100,$LOOP_STATUS,IPF:$IPFLAKIES_RESULT" >> "$RESULTS"
echo "$INSTANCE_ID -> 100x:$LOOP_STATUS ($PASS_COUNT/100), iPFlakies:$IPFLAKIES_RESULT"
