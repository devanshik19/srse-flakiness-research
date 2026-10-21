# Extracting non-flaky tests from a Java project

A two-step pipeline:

1. **`01_collect_tests.sh`** — list every test that actually runs in a project module at a
   given commit.
2. **`02_exclude_flaky.py`** — subtract the known-flaky tests from that list, leaving the
   non-flaky set (optionally as a formatted CSV).

Run them in order; step 2 consumes step 1's output.

## Requirements

- `bash`, `git`, Maven, a JDK, `python3`
- At least one flaky-test source CSV to exclude against (any combination):
  - `result_matched.csv` — AgentFlake dataset sheet (cols: `project`, `flaky_commit`,
    `module`, `flaky_test`, …)
  - `164_AgentFlake_Flaky_Tests.csv` (cols: `Slug`, `Flaky Test Name`, …)
  - IDoFT `pr-data.csv` (cols: `Project URL`, `Fully-Qualified Test Name …`)

## Step 1 — collect all tests that run

```bash
./01_collect_tests.sh <repo_url> <commit> <work_dir> [module]
```

- Clones `<repo_url>` into `<work_dir>` (reuses an existing clone), checks out `<commit>`,
  runs `mvn test`, and writes every test that ran to `<work_dir>/all_tests.txt`
  (one `fully.qualified.Class#method` per line).
- `[module]` is the Maven module to test (default `.` = repo root). For a multi-module repo
  pass the module path, e.g. `dubbo-common`.
- Some tests failing during `mvn test` is expected and fine — we only need the surefire
  reports for whatever ran.

## Step 2 — subtract the flaky ones

```bash
python3 02_exclude_flaky.py \
  --repo-url <repo_url> \
  --all-tests <work_dir>/all_tests.txt \
  --matched-csv result_matched.csv \     # and/or --known-csv / --idoft-csv
  --out non_flaky_<subject>.txt \        # bare list: one Class#method per line
  --csv-out nonflaky_all.csv \           # OPTIONAL: formatted CSV (append mode)
  --sha <commit> --module <module>       # only used to tag --csv-out rows
```

- Drops every test in `all_tests.txt` that is listed as flaky for that repo (matched by
  repo URL) in any CSV you pass.
- `--out` always writes the plain non-flaky list.
- `--csv-out` additionally **appends** rows
  `proj_name,url,sha,module,non_flaky_test,focal_method`. Append mode means looping over many
  subjects builds a single combined CSV. `focal_method` is left blank — it's resolved in a
  separate step, not by this script.
- Prints a report to stderr: how many flaky matched, how many were excluded, and any flaky
  entries that did NOT appear in `all_tests.txt` (renamed, or not exercised by `mvn test`).

## Running many subjects at once

Loop steps 1–2 over each `(repo, commit, module)`. Example driving straight off
`result_matched.csv` (cols 2 = project URL, 3 = commit, 7 = module):

```bash
CSV="result_matched.csv"
rm -f nonflaky_all.csv
tail -n +2 "$CSV" | awk -F, '{print $2"|"$3"|"$7}' | sort -u |
while IFS='|' read -r url sha module; do
  slug=$(echo "$url" | sed 's#.*/##')__${sha:0:7}
  ./01_collect_tests.sh "$url" "$sha" "work/$slug" "$module"
  python3 02_exclude_flaky.py --repo-url "$url" \
    --all-tests "work/$slug/all_tests.txt" --matched-csv "$CSV" \
    --out "nonflaky_$slug.txt" --csv-out nonflaky_all.csv --sha "$sha" --module "$module"
done
# -> one nonflaky_all.csv across all subjects
```

## Notes / caveats

- **Flaky matching is by repo URL** (across any commit/module) — a test flaky for the
  project is excluded wherever it appears. This matches the dataset's own convention.
- **"Non-flaky" = "not in the flaky list(s) you provide."** The scripts do not re-run
  flakiness detection on the survivors.
- **`focal_method` is blank** in the CSV — it's filled by a separate focal-resolution step.
- **Multi-module repos:** `mvn -pl <module> test` can fail to resolve sibling-module
  dependencies. If a module build can't find its deps, add `-am` to the `mvn` line in
  `01_collect_tests.sh`.
- **Quote CSV paths with spaces** (e.g. `"result_matched (1).csv"`).
