#!/usr/bin/env python3
"""
02_exclude_flaky.py -- given a subject's full test list (from 01_collect_tests.sh),
drop every test that is already known-flaky: either in Shinae's 164-test CSV, or
listed anywhere in IDoFT's pr-data.csv for the same project (any commit -- IDoFT
flags a test as flaky for the project, not just at one SHA, per the mentor's
instruction to exclude "any tests listed as flaky for that project in IDoFT").

Usage:
  python3 02_exclude_flaky.py \
      --repo-url https://github.com/TooTallNate/Java-WebSocket \
      --all-tests all_tests.txt \
      --known-csv 164_AgentFlake_Flaky_Tests.csv \
      --idoft-csv idoft_pr_data.csv \
      --out non_flaky_tests.txt

You can also pass --matched-csv result_matched.csv (the AgentFlake flaky-dataset
sheet: columns 'project' = repo URL, 'flaky_test' = Class#method). Same URL-level
matching as the other two sources.

All of --known-csv, --idoft-csv and --matched-csv are optional (skip a source if
you don't have it handy), but at least one should be given or this does nothing useful.

Output: one "fully.qualified.Class#method" per line, everything from --all-tests
that did NOT match a known-flaky entry. Also prints a short report to stderr
listing exactly which known-flaky tests were found/excluded, and which known-flaky
entries did NOT match anything in --all-tests (worth a manual look -- could mean a
rename, or the flaky test isn't run by plain `mvn test`).

With --csv-out (plus --sha / --module) it ALSO appends formatted rows
"proj_name,url,sha,module,non_flaky_test,focal_method" to that file. Append-mode, so a
loop over many subjects accumulates one combined CSV. focal_method is left blank here --
it's filled by stage 2 (resolve_focal.sh). The --out bare list is still always written.
"""
import argparse
import csv
import os
import sys


def norm_repo(url: str) -> str:
    return url.strip().rstrip("/").lower()


def load_known_csv(path, repo_url):
    """164_AgentFlake_Flaky_Tests.csv: Slug,Commit,Flaky Test Name,container,test_type
    'Flaky Test Name' is already Class#method."""
    out = set()
    if not path:
        return out
    target = norm_repo(repo_url)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            slug = row.get("Slug") or ""
            if norm_repo(slug) != target:
                continue
            name = (row.get("Flaky Test Name") or "").strip()
            if name:
                out.add(name)
    return out


def load_idoft_csv(path, repo_url):
    """IDoFT pr-data.csv: Project URL,SHA Detected,Module Path,
    Fully-Qualified Test Name (packageName.ClassName.methodName),Category,Status,PR Link,Notes
    Test name uses dots throughout -- convert to Class#method by splitting on the last dot."""
    out = set()
    if not path:
        return out
    target = norm_repo(repo_url)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            url = row.get("Project URL") or ""
            if norm_repo(url) != target:
                continue
            fq = (row.get("Fully-Qualified Test Name (packageName.ClassName.methodName)") or "").strip()
            if "." not in fq:
                continue
            cls, method = fq.rsplit(".", 1)
            out.add(f"{cls}#{method}")
    return out


def load_matched_csv(path, repo_url):
    """result_matched.csv (AgentFlake flaky-dataset sheet):
    sheet_test_type,project,flaky_commit,test_type,result_container,zip,module,
    polluter/state setter,flaky_test,...
    'project' is the repo URL; 'flaky_test' is already Class#method. Matched by repo
    URL only (any commit/module), same convention as load_idoft_csv."""
    out = set()
    if not path:
        return out
    target = norm_repo(repo_url)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if norm_repo(row.get("project") or "") != target:
                continue
            name = (row.get("flaky_test") or "").strip()
            if name:
                out.add(name)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-url", required=True)
    ap.add_argument("--all-tests", required=True)
    ap.add_argument("--known-csv")
    ap.add_argument("--idoft-csv")
    ap.add_argument("--matched-csv")
    ap.add_argument("--out", required=True)
    ap.add_argument("--csv-out",
                    help="ALSO append formatted rows "
                         "(proj_name,url,sha,module,non_flaky_test,focal_method) to this file; "
                         "append-mode so a loop over many subjects builds one combined CSV")
    ap.add_argument("--sha", default="", help="commit sha to tag --csv-out rows with")
    ap.add_argument("--module", default=".", help="module to tag --csv-out rows with")
    args = ap.parse_args()

    with open(args.all_tests, encoding="utf-8") as f:
        all_tests = [l.strip() for l in f if l.strip()]

    known = load_known_csv(args.known_csv, args.repo_url)
    idoft = load_idoft_csv(args.idoft_csv, args.repo_url)
    matched = load_matched_csv(args.matched_csv, args.repo_url)
    flaky = known | idoft | matched

    all_set = set(all_tests)
    excluded = sorted(t for t in all_tests if t in flaky)
    non_flaky = sorted(t for t in all_tests if t not in flaky)
    unmatched_flaky = sorted(t for t in flaky if t not in all_set)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(non_flaky) + ("\n" if non_flaky else ""))

    if args.csv_out:
        proj = args.repo_url.strip().rstrip("/").split("/")[-1]
        header_needed = not os.path.exists(args.csv_out) or os.path.getsize(args.csv_out) == 0
        with open(args.csv_out, "a", newline="", encoding="utf-8") as cf:
            w = csv.writer(cf)
            if header_needed:
                w.writerow(["proj_name", "url", "sha", "module", "non_flaky_test", "focal_method"])
            for t in non_flaky:
                w.writerow([proj, args.repo_url, args.sha, args.module, t, ""])  # focal filled in stage 2

    print(f"repo: {args.repo_url}", file=sys.stderr)
    print(f"all tests collected:      {len(all_tests)}", file=sys.stderr)
    print(f"known-flaky (164 CSV):    {len(known)}", file=sys.stderr)
    print(f"known-flaky (IDoFT):      {len(idoft)}", file=sys.stderr)
    print(f"known-flaky (matched):    {len(matched)}", file=sys.stderr)
    print(f"excluded (matched+ran):   {len(excluded)}", file=sys.stderr)
    print(f"non-flaky remaining:      {len(non_flaky)} -> {args.out}", file=sys.stderr)
    if excluded:
        print("\n-- excluded tests --", file=sys.stderr)
        for t in excluded:
            print(f"  {t}", file=sys.stderr)
    if unmatched_flaky:
        print(
            f"\n-- {len(unmatched_flaky)} known-flaky entries did NOT appear in --all-tests "
            "(renamed/moved/not exercised by `mvn test`?) --",
            file=sys.stderr,
        )
        for t in unmatched_flaky:
            print(f"  {t}", file=sys.stderr)


if __name__ == "__main__":
    main()
