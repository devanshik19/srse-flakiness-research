# Non-flaky test extraction

These scripts take a Java project at a given commit and give you the tests that are *not*
flaky, as a CSV.

Two steps:
- `01_collect_tests.sh` builds the project and lists every test that runs.
- `02_exclude_flaky.py` drops the known-flaky ones and writes the CSV.

## Requirements

git, Maven, a JDK, and python3. You also need the flaky-test sheet (`result_matched.csv`).

## How to run

Put `result_matched.csv` in this folder first.

```bash
chmod +x 01_collect_tests.sh
CSV="result_matched.csv"
```

Try one project first to make sure it works:

```bash
./01_collect_tests.sh https://github.com/bpsm/edn-java 4cf29ffe2d063269cb09c9bf4f6fd5c1a3cb4e1b work/edn .
python3 02_exclude_flaky.py --repo-url https://github.com/bpsm/edn-java \
  --all-tests work/edn/all_tests.txt --matched-csv "$CSV" \
  --out nonflaky_edn.txt --csv-out nonflaky_all.csv \
  --sha 4cf29ffe2d063269cb09c9bf4f6fd5c1a3cb4e1b --module .
```

Open `nonflaky_all.csv`. It should have columns: proj_name, url, sha, module,
non_flaky_test, focal_method.

To run every project in the sheet into one CSV:

```bash
rm -f nonflaky_all.csv
tail -n +2 "$CSV" | awk -F, '{print $2"|"$3"|"$7}' | sort -u |
while IFS='|' read -r url sha module; do
  slug=$(echo "$url" | sed 's#.*/##')__${sha:0:7}
  ./01_collect_tests.sh "$url" "$sha" "work/$slug" "$module"
  python3 02_exclude_flaky.py --repo-url "$url" \
    --all-tests "work/$slug/all_tests.txt" --matched-csv "$CSV" \
    --out "nonflaky_$slug.txt" --csv-out nonflaky_all.csv --sha "$sha" --module "$module"
done
```

It clones and builds each project, so it takes a while.

## Output

`nonflaky_all.csv` is the file you want. `focal_method` is left empty for now; that gets
filled in a later step.

## Notes

- `module` is `.` when the project has no sub-modules (tests sit at the repo root).
- A few big multi-module projects (hadoop, dubbo) may need `-am` added to the mvn line in
  `01_collect_tests.sh`, or their test list comes out empty.
