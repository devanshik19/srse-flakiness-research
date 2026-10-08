#!/usr/bin/env python3
# flaky.py <docker_results.csv>
# FLAKY = same test does not get the same verdict on every run.
# Reports at two granularities:
#   - function: one `def test_...` (precise unit)
#   - file:     one generated GPT sample (one test_*.py); flaky if any function in it is flaky
import csv, sys
from collections import defaultdict

funcs = defaultdict(list)                       # (instance, func) -> [(phase, verdict), ...]
with open(sys.argv[1], newline="") as f:
    for r in csv.DictReader(f):
        funcs[(r["instance"], r["test"].strip('"'))].append((r["phase"], r["verdict"]))

flaky_funcs = []
flaky_files = set()
for (inst, func), runs in sorted(funcs.items()):
    if len({v for _, v in runs}) > 1:           # more than one distinct verdict -> flaky
        flaky_funcs.append((inst, func, runs))
        flaky_files.add((inst, func.split("::")[0]))

all_files = {(inst, func.split("::")[0]) for (inst, func) in funcs}

for inst, func, runs in flaky_funcs:
    base = sorted({v for p, v in runs if p == "baseline"})
    cpu  = sorted({v for p, v in runs if p == "cpu"})
    print(f"FLAKY  {inst}  {func}")
    print(f"       baseline={base}  cpu={cpu}")

print(f"\nfunctions: {len(flaky_funcs)} flaky / {len(funcs)} total")
print(f"files:     {len(flaky_files)} flaky / {len(all_files)} total")
