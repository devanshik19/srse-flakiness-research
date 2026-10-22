# Non-flaky test extraction

Gets the non-flaky tests and their focal method for each Java project in `result_matched.csv`,
as a CSV.

Needs: git, Maven, a JDK, python3, `result_matched.csv`. Step 3 also needs `OPENAI_API_KEY`.

## Run

```bash
CSV="result_matched.csv"

# steps 1 + 2: list tests, drop the flaky ones -> nonflaky_all.csv
rm -f nonflaky_all.csv
tail -n +2 "$CSV" | awk -F, '{print $2"|"$3"|"$7}' | sort -u |
while IFS='|' read -r url sha module; do
  slug=$(echo "$url" | sed 's#.*/##')__${sha:0:7}
  ./01_collect_tests.sh "$url" "$sha" "work/$slug" "$module"
  python3 02_exclude_flaky.py --repo-url "$url" \
    --all-tests "work/$slug/all_tests.txt" --matched-csv "$CSV" \
    --out "nonflaky_$slug.txt" --csv-out nonflaky_all.csv --sha "$sha" --module "$module"
done

# step 3: fill in focal_method -> nonflaky_all_focal.csv
python3 03_resolve_focal.py --in nonflaky_all.csv --out nonflaky_all_focal.csv \
  --workroot work --helpers ~/agentflake-work/nonflaky
```

Output: **`nonflaky_all_focal.csv`** — proj_name, url, sha, module, non_flaky_test, focal_method.

## Notes

- `module` is `.` for single-module repos.
- Multi-module repos (hadoop, dubbo) may need `-am` added to the mvn line in `01_collect_tests.sh`.
- Add `--jaccard-only` to step 3 to skip the LLM (no API key, less accurate).
