#!/usr/bin/env bash
# Stress (cpu+memory ONLY, no baseline) the FC_FCV folders from more_flaky_check_tests.zip.
#   agent_FC_12 (32 methods) + agent_FCV_9 (26 methods) = 58 methods
# These folders have a full tests.csv (file_here + test_file + mockito_fix), identical schema
# to the flaky_checked_tests variants, so the proven placement logic works unchanged.
# Two-phase: baseline is run LATER, only for methods that fail/flake under stress.
# One run, split CSV per folder: flaky_check_out/stress_<folder>/stress_results.csv
# Resumable: re-run after a reboot; completed methods are skipped.
# RUN ONLY WHEN NO OTHER STRESS OR FLAKERAKE/TD RUN IS ACTIVE (concurrent load corrupts results).
set -uo pipefail

PKG="$HOME/flakecheck/flaky_check_package"
ZIP="/mnt/c/Users/Amita/Downloads/more_flaky_check_tests.zip"
SRC="$HOME/fcfcv_src"

cd "$PKG" || { echo "package not found: $PKG"; exit 1; }

echo ">> extracting FC_FCV test files from zip"
rm -rf "$SRC"; mkdir -p "$SRC"
unzip -o -q "$ZIP" "flaky_checked_tests_FC_FCV/*" -d "$SRC"
BASE="$SRC/flaky_checked_tests_FC_FCV"

for folder in agent_FC_12 agent_FCV_9; do
  echo ">> ===================== $folder ====================="
  csv="$BASE/$folder/tests.csv"
  [ -f "$csv" ] || { echo "   !! no tests.csv in $folder, skipping"; continue; }

  # place each file_here (in the zip) at its test_file path under the package
  python3 - "$csv" "$BASE/$folder" "$PKG" <<'PY'
import csv, sys, os, shutil
csvp, folder, pkg = sys.argv[1], sys.argv[2], sys.argv[3]
n = 0
with open(csvp, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        src = os.path.join(folder, r["file_here"])
        dst = os.path.join(pkg, r["test_file"])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        n += 1
print(f"   placed {n} test files")
PY

  cp "$csv" "$PKG/task_csvs/stress_$folder.csv"

  python3 stress_check.py \
    --tests "task_csvs/stress_$folder.csv" \
    --archive-dir extracted \
    --regimes cpu,memory --runs 10 \
    --out "flaky_check_out/stress_$folder"
done

echo
echo ">> FC_FCV DONE. Per-folder results:"
for folder in agent_FC_12 agent_FCV_9; do
  echo "   flaky_check_out/stress_$folder/stress_results.csv"
done
