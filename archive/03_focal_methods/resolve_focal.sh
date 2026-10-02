#!/bin/bash
# resolve_focal.sh -- AgentFlake focal-method resolution (Jaccard + LLM -> intersection)
set -uo pipefail
TESTFILE="${1:?usage: resolve_focal.sh <VictimTest.java> <victimTestMethod> [model]}"
VICTIM_METHOD="${2:?need the victim test method name, e.g. testGetInvoker}"
MODEL="${3:-gpt-4o}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
[ -f "$TESTFILE" ] || { echo "!! test file not found: $TESTFILE"; exit 1; }
: "${OPENAI_API_KEY:?set OPENAI_API_KEY in your shell first (LLM half needs it)}"
python3 -c 'import javalang' 2>/dev/null || {
  echo ">> installing javalang (one-time)"; pip3 install --quiet javalang || pip3 install --quiet --break-system-packages javalang; }
echo ">> [1/4] extract candidates from $(basename "$TESTFILE")"
python3 "$HERE/focal_extract.py" "$TESTFILE" > "$WORK/jaccard_in.json" 2> "$WORK/extract.err" \
  || { echo "!! focal_extract failed:"; cat "$WORK/extract.err"; exit 1; }
grep -q '"test_name"' "$WORK/jaccard_in.json" || { echo "!! no @Test methods parsed. stderr:"; cat "$WORK/extract.err"; exit 1; }
echo ">> [2/4] Jaccard pick"
python3 "$HERE/focal_method_finder_batch.py" "$WORK/jaccard_in.json" "$WORK/jaccard_out.json" >/dev/null \
  || { echo "!! jaccard batch failed"; exit 1; }
echo ">> [3/4] LLM pick (model=$MODEL)"
python3 "$HERE/llm_focal.py" "$TESTFILE" -o "$WORK/llm_out.json" --model "$MODEL" --cache "$WORK/llm_cache.json" 2> "$WORK/llm.err" \
  || { echo "!! llm_focal failed:"; cat "$WORK/llm.err"; exit 1; }
echo ">> [4/4] intersection (confirmed only when Jaccard == LLM)"
python3 "$HERE/intersect_focal.py" "$WORK/jaccard_out.json" "$WORK/llm_out.json" "$WORK/intersect_out.json" \
  || { echo "!! intersect failed"; exit 1; }
echo "----------------------------------------------------------------"
python3 - "$WORK/intersect_out.json" "$VICTIM_METHOD" <<'PY'
import json, sys
data = json.load(open(sys.argv[1])); victim = sys.argv[2]
entry = next((e for e in data if e.get("test_name") == victim), None)
if entry is None:
    names = ", ".join(e.get("test_name","?") for e in data)
    sys.stderr.write(f"!! victim method '{victim}' not among parsed @Test methods: {names}\n")
    print(f"FOCAL=  STATUS=victim-not-found"); sys.exit(3)
fm, st = entry.get("focal_method"), entry.get("status")
print(f"jaccard={entry.get('jaccard_focal')} (score={entry.get('jaccard_score')})  "
      f"llm={entry.get('llm_focal')} (p={entry.get('llm_probability')})")
print(f"FOCAL={fm or ''}  STATUS={st}")
sys.exit(0 if st == "agreed" else 2)
PY
rc=$?
echo "----------------------------------------------------------------"
[ $rc -eq 0 ] && echo ">> OK: confirmed focal, safe to feed ChatUniTest as <CUT>#<FOCAL>" \
             || echo ">> NOT confirmed (rc=$rc): disagreed or victim missing -- inspect before trusting."
exit $rc
