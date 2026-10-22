#!/usr/bin/env python3
"""
03_resolve_focal.py -- fill the focal_method column in nonflaky_all.csv.

For each non-flaky test it resolves the focal method with the existing AgentFlake
helpers (the same ones resolve_focal.sh uses): focal_extract.py -> focal_method_finder_batch.py
-> llm_focal.py -> intersect_focal.py. It runs them once per test CLASS file (one LLM call
per file, not per method), then writes each method's focal back into the CSV.

Needs:
  - the clones stage 1 left under <workroot>/<slug>  (slug = <repo-name>__<sha[:7]>)
  - the helper scripts (pass their folder with --helpers; default ~/agentflake-work/nonflaky)
  - OPENAI_API_KEY set in the shell (same requirement as resolve_focal.sh), unless --jaccard-only

Usage:
  OPENAI_API_KEY=sk-... python3 03_resolve_focal.py \
      --in nonflaky_all.csv --out nonflaky_all_focal.csv \
      --workroot work --helpers ~/agentflake-work/nonflaky
  # free/offline, less accurate:
  python3 03_resolve_focal.py --in nonflaky_all.csv --out nonflaky_all_focal.csv --jaccard-only
"""
import argparse, csv, json, os, subprocess, sys, tempfile, collections


def norm(name):
    if not name:
        return ""
    return str(name).split("(")[0].strip().split(".")[-1]


def slug_of(url, sha):
    return url.rstrip("/").split("/")[-1] + "__" + sha[:7]


def testfile(workroot, slug, module, cls):
    sub = "" if module in (".", "", None) else module
    return os.path.join(workroot, slug, sub, "src", "test", "java",
                        cls.replace(".", "/") + ".java")


ap = argparse.ArgumentParser()
ap.add_argument("--in", dest="inp", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--workroot", default="work")
ap.add_argument("--helpers", default=os.path.expanduser("~/agentflake-work/nonflaky"))
ap.add_argument("--model", default="gpt-4o")
ap.add_argument("--jaccard-only", action="store_true")
a = ap.parse_args()

rows = list(csv.DictReader(open(a.inp, newline="", encoding="utf-8")))

# group non-flaky tests by (slug, module, test class)
groups = collections.OrderedDict()
for r in rows:
    slug = slug_of(r["url"], r["sha"])
    cls = r["non_flaky_test"].split("#", 1)[0]
    groups.setdefault((slug, r["module"], cls), []).append(r)

H = a.helpers
focal = {}   # (slug, module, "Class#method") -> (focal_method, status)

for (slug, module, cls), grp in groups.items():
    tf = testfile(a.workroot, slug, module, cls)
    if not os.path.isfile(tf):
        print(f"!! missing test file, skipping: {tf}", file=sys.stderr)
        continue
    with tempfile.TemporaryDirectory() as w:
        ji, jo = os.path.join(w, "ji.json"), os.path.join(w, "jo.json")
        lo, io_ = os.path.join(w, "lo.json"), os.path.join(w, "io.json")
        ca = os.path.join(w, "cache.json")
        try:
            with open(ji, "w") as f:
                subprocess.run(["python3", os.path.join(H, "focal_extract.py"), tf],
                               check=True, stdout=f)
            subprocess.run(["python3", os.path.join(H, "focal_method_finder_batch.py"), ji, jo],
                           check=True, stdout=subprocess.DEVNULL)
            if a.jaccard_only:
                for e in json.load(open(jo)):
                    focal[(slug, module, f"{cls}#{e.get('test_name')}")] = (
                        norm(e.get("focal_method")), "jaccard")
            else:
                subprocess.run(["python3", os.path.join(H, "llm_focal.py"), tf,
                                "-o", lo, "--model", a.model, "--cache", ca], check=True)
                subprocess.run(["python3", os.path.join(H, "intersect_focal.py"), jo, lo, io_],
                               check=True, stdout=subprocess.DEVNULL)
                for e in json.load(open(io_)):
                    fm = e.get("focal_method") or e.get("jaccard_focal") or e.get("llm_focal")
                    focal[(slug, module, f"{cls}#{e.get('test_name')}")] = (
                        norm(fm), e.get("status", ""))
        except subprocess.CalledProcessError as err:
            print(f"!! focal resolution failed for {cls} in {slug}: {err}", file=sys.stderr)
            continue
    print(f"[{slug}] {cls}: resolved", file=sys.stderr)

with open(a.out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["proj_name", "url", "sha", "module", "non_flaky_test", "focal_method", "focal_status"])
    filled = 0
    for r in rows:
        slug = slug_of(r["url"], r["sha"])
        fm, st = focal.get((slug, r["module"], r["non_flaky_test"]), ("", ""))
        if fm:
            filled += 1
        w.writerow([r["proj_name"], r["url"], r["sha"], r["module"],
                    r["non_flaky_test"], fm, st])

print(f"\nfilled focal_method for {filled}/{len(rows)} rows -> {a.out}", file=sys.stderr)
