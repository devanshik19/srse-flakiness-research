#!/bin/bash
# run_batch3_checks.sh -- run ND(100)/ID(30)/OD(20) on every unique successfully-
# generated test from batch3_results.csv. Meant to be nohup'd, this can take hours.
set -uo pipefail
cd ~/agentflake-work/nonflaky

awk -F, 'NR>1 && $6=="pass" {print $5}' java-websocket/batch3_results.csv | sort -u > java-websocket/batch3_unique_gen.txt
N=$(wc -l < java-websocket/batch3_unique_gen.txt)
echo ">>> $N unique generated tests to check"

: > java-websocket/nd_results_batch3.csv
: > java-websocket/id_results_batch3.csv
: > java-websocket/od_results_batch3.csv

i=0
while IFS= read -r GEN; do
  i=$((i+1))
  echo "########## [$i/$N] $GEN ##########"
  ./04_check_nd.sh java-websocket . "$GEN" java-websocket/nd_results_batch3.csv 100
  ./05_check_id_nondex.sh java-websocket . "$GEN" java-websocket/id_results_batch3.csv 30
  ./06_check_od.sh java-websocket . "$GEN" java-websocket/od_results_batch3.csv 20
done < java-websocket/batch3_unique_gen.txt

echo ">>> ALL CHECKS DONE"
