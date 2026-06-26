#!/bin/bash
INSTANCE_ID="$1"
TEST_FILE="$2"
TEST_NAME="$3"
REPO_NAME="$4"

# Activate the testbed conda env (docker exec doesn't inherit it)
source /opt/miniconda3/etc/profile.d/conda.sh
conda activate testbed

cd /testbed || { echo "$INSTANCE_ID,NO_TESTBED"; exit 0; }

git apply golden.patch 2>/dev/null || { echo "$INSTANCE_ID,GOLDEN_FAIL"; exit 0; }
git apply agent.patch 2>/dev/null || { echo "$INSTANCE_ID,AGENT_FAIL"; exit 0; }

pip install ipflakies pytest-random-order pytest-csv >/dev/null 2>&1

IPF_UTILS=$(find /opt/miniconda3/envs/testbed -name "utils.py" -path "*ipflakies*" 2>/dev/null | head -1)
python3 -c "
import io
f='$IPF_UTILS'
s=io.open(f,encoding='utf-8').read()
s=s.replace('WIDTH = os.get_terminal_size().columns','try:\n    WIDTH = os.get_terminal_size().columns\nexcept OSError:\n    WIDTH = 80')
s=s.replace('HEIGHT = os,get_terminal_size().lines','try:\n    HEIGHT = os.get_terminal_size().lines\nexcept OSError:\n    HEIGHT = 24')
io.open(f,'w',encoding='utf-8').write(s)
" 2>/dev/null

if [ -f setup.cfg ] && grep -q "^testpaths" setup.cfg; then
    cp setup.cfg setup.cfg.bak
    sed -i "s|^testpaths.*|testpaths = $TEST_FILE|" setup.cfg
    if [ "$REPO_NAME" == "astropy" ]; then
        if grep -q "^addopts" setup.cfg; then
            sed -i "s|^addopts.*|addopts = -p no:warnings -p no:doctestplus -p no:openfiles -p no:arraydiff -p no:astropy_header -p no:filter_subpackage -p no:remotedata|" setup.cfg
        else
            echo "addopts = -p no:doctestplus -p no:openfiles -p no:arraydiff -p no:astropy_header -p no:filter_subpackage -p no:remotedata" >> setup.cfg
        fi
    fi
else
    cat > pytest.ini << EOF
[pytest]
testpaths = $TEST_FILE
EOF
fi

PASS=0; FAIL=0
for i in $(seq 1 100); do
    if PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 timeout 60 python -m pytest "${TEST_FILE}::${TEST_NAME}" -p random_order -p csv --assert=plain -q >/dev/null 2>&1; then
        PASS=$((PASS+1)); else FAIL=$((FAIL+1)); fi
done
if [ "$PASS" -gt 0 ] && [ "$FAIL" -gt 0 ]; then LOOP="FLAKY"
elif [ "$PASS" -eq 100 ]; then LOOP="ALWAYS_PASS"
else LOOP="ALWAYS_FAIL"; fi

COLUMNS=80 PYTHONUNBUFFERED=1 timeout 900 python -m ipflakies -i 10 >/dev/null 2>&1
if [ -f "ipflakies_result/flakies.json" ]; then
    IPF=$(python3 -c "import json; d=json.load(open('ipflakies_result/flakies.json')); print(len([k for k in d if k!='time']))" 2>/dev/null)
    [ -z "$IPF" ] && IPF="ERROR"
else
    IPF="NO_RESULT_FILE"
fi

echo "$INSTANCE_ID,$REPO_NAME,$TEST_FILE,$TEST_NAME,${PASS}/100,$LOOP,IPF:$IPF"
