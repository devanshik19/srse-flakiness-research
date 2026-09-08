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

Both --known-csv and --idoft-csv are optional (skip a source if you don't have
it handy), but at least one should be given or this does nothing useful.

Output: one "fully.qualified.Class#method" per line, everything from --all-tests
that did NOT match a known-flaky entry. Also prints a short report to stderr
listing exactly which known-flaky tests were found/excluded, and which known-flaky
entries did NOT match anything in --all-tests (worth a manual look -- could mean a
rename, or the flaky test isn't run by plain `mvn test`).
"""
import argparse
import csv
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-url", required=True)
    ap.add_argument("--all-tests", required=True)
    ap.add_argument("--known-csv")
    ap.add_argument("--idoft-csv")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    with open(args.all_tests, encoding="utf-8") as f:
        all_tests = [l.strip() for l in f if l.strip()]

    known = load_known_csv(args.known_csv, args.repo_url)
    idoft = load_idoft_csv(args.idoft_csv, args.repo_url)
    flaky = known | idoft

    all_set = set(all_tests)
    excluded = sorted(t for t in all_tests if t in flaky)
    non_flaky = sorted(t for t in all_tests if t not in flaky)
    unmatched_flaky = sorted(t for t in flaky if t not in all_set)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(non_flaky) + ("\n" if non_flaky else ""))

    print(f"repo: {args.repo_url}", file=sys.stderr)
    print(f"all tests collected:      {len(all_tests)}", file=sys.stderr)
    print(f"known-flaky (164 CSV):    {len(known)}", file=sys.stderr)
    print(f"known-flaky (IDoFT):      {len(idoft)}", file=sys.stderr)
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
