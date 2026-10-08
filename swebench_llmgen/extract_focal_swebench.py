#!/usr/bin/env python3
# Extract the focal method(s) per SWE-bench Verified instance from the gold patch.
# The gold patch is the bug fix; git hunk headers "@@ ... @@ def foo(...)" name the
# enclosing function, so we read the focal method straight from the diff (no checkout).
#
# Output: swebench_focal.csv  ->  instance_id, repo, base_commit, file, focal_function
# Usage:  pip install datasets ; python3 extract_focal_swebench.py
import csv, re
from datasets import load_dataset

ds = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")

FILE_RE = re.compile(r'^\+\+\+ b/(.+?)\s*$', re.M)
# enclosing def/class named in a hunk header
HUNK_RE = re.compile(r'^@@ .*? @@\s*(?:async\s+)?(?:def|class)\s+([A-Za-z_]\w*)', re.M)

rows = []
for ex in ds:
    # a patch can touch several files; split into per-file sections
    for section in ("diff --git" + ex["patch"]).split("diff --git")[1:]:
        fm = FILE_RE.search(section)
        if not fm:
            continue
        fpath = fm.group(1).strip()
        if not fpath.endswith(".py"):
            continue
        funcs = HUNK_RE.findall(section)
        for fn in (funcs or [""]):               # keep file even if no func name found
            rows.append([ex["instance_id"], ex["repo"], ex["base_commit"], fpath, fn])

# de-dup identical (instance, file, function) rows
seen, uniq = set(), []
for r in rows:
    k = tuple(r)
    if k not in seen:
        seen.add(k); uniq.append(r)

with open("swebench_focal.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["instance_id", "repo", "base_commit", "file", "focal_function"])
    w.writerows(uniq)

named = sum(1 for r in uniq if r[4])
print(f"{len(ds)} instances -> {len(uniq)} focal rows ({named} with a function name) -> swebench_focal.csv")
