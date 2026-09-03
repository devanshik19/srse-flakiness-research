#!/bin/bash
# run_dubbo.sh -- loop od_full.sh over the remaining dubbo OD rows from test_config.csv.
# Reads rows straight from the dataset, skips any already in results.csv, handles
# download/unzip + per-zip container startup (maven 3.9.x + python-scripts), then runs the worker.
# Rows that share a zip but differ by victim (e.g. 628ad77 / 628ad771) are kept distinct in
# results via SUBJECT_OVERRIDE (the row's result_container), while SUBJDIR/ZIP stay keyed by zip.
set -uo pipefail
WORK="$HOME/agentflake-work"; DATA="$WORK/data"; REPO="$HOME/srse-research"; OUTDIR="$REPO/agentflake-od"
RESULTS="$OUTDIR/results.csv"; TC="$WORK/test_config.csv"; IMAGE=flaky_base_jdk8_od_cov
: "${OPENAI_API_KEY:?export OPENAI_API_KEY first}"
[ -f "$TC" ] || { echo "!! $TC not found"; exit 1; }
mkdir -p "$DATA"
log(){ echo "==== $* ===="; }

mapfile -t ROWS < <(python3 - "$TC" "$RESULTS" <<'PY'
import csv,sys,os
tc,res=sys.argv[1],sys.argv[2]
done=set()
if os.path.exists(res):
    for line in open(res):
        done.add(line.split(",",1)[0])
for r in csv.DictReader(open(tc)):
    if r["test_type"].strip().lower()!="od": continue
    if "dubbo" not in (r["result_container"]+r["module"]+r["flaky_test"]).lower(): continue
    if r["result_container"] in done: continue
    print("\t".join([r["result_container"],r["zip"],r["module"],r["polluter/state setter"],r["flaky_test"],r["url"]]))
PY
)
[ ${#ROWS[@]} -eq 0 ] && { echo "no remaining dubbo OD rows -- all done"; exit 0; }
echo "remaining dubbo rows: ${#ROWS[@]}"
printf '  %s\n' "${ROWS[@]}" | cut -f1,5

ensure_subject(){ local zip="$1" url="$2" sd="$DATA/$zip"
  if [ ! -d "$sd/Flaky" ]; then
    log "download+unzip $zip"
    [ -f "$DATA/$zip.zip" ] || curl -L -o "$DATA/$zip.zip" "$url" || return 1
    mkdir -p "$sd"; unzip -q -o "$DATA/$zip.zip" -d "$sd" || return 1
    if [ ! -d "$sd/Flaky" ]; then
      inner=$(find "$sd" -maxdepth 3 -name Flaky -type d | head -1)
      [ -n "$inner" ] && { pd=$(dirname "$inner"); mv "$pd"/* "$sd"/ 2>/dev/null; }
    fi
  fi
  [ -d "$sd/Flaky" ] || { echo "!! no Flaky under $sd after unzip"; return 1; }
  [ -f "$DATA/$zip.zip" ] || cp "$sd.zip" "$DATA/$zip.zip" 2>/dev/null || true
}

ensure_container(){ local zip="$1" cname="$2" sd="$DATA/$zip"
  if ! docker inspect "$cname" >/dev/null 2>&1 || [ "$(docker inspect -f '{{.State.Running}}' "$cname" 2>/dev/null)" != "true" ]; then
    docker rm -f "$cname" >/dev/null 2>&1 || true
    local m2="$sd/Flakym2/.m2"
    log "start container $cname"
    if [ -d "$m2" ]; then
      docker run -d --name "$cname" \
        --mount type=bind,source="$(cd "$sd/Flaky" && pwd)",target=/app/source \
        --mount type=bind,source="$(cd "$m2" && pwd)",target=/root/.m2 \
        -e OPENAI_API_KEY="$OPENAI_API_KEY" "$IMAGE" tail -f /dev/null >/dev/null
    else
      docker run -d --name "$cname" \
        --mount type=bind,source="$(cd "$sd/Flaky" && pwd)",target=/app/source \
        -e OPENAI_API_KEY="$OPENAI_API_KEY" "$IMAGE" tail -f /dev/null >/dev/null
    fi
  fi
  log "ensure maven 3.9.9 + python-scripts in $cname"
  docker exec "$cname" bash -lc 'ls /opt/apache-maven-3.9.9/bin/mvn >/dev/null 2>&1 || { echo installing-mvn-3.9.9; curl -sL https://archive.apache.org/dist/maven/maven-3/3.9.9/binaries/apache-maven-3.9.9-bin.tar.gz | tar xz -C /opt; }'
  docker exec "$cname" bash -lc '[ -f /app/source/python-scripts/parse_surefire_report.py ]' 2>/dev/null || docker cp "$WORK/python-scripts" "$cname:/app/source/python-scripts" >/dev/null 2>&1 || true
}

for row in "${ROWS[@]}"; do
  IFS=$'\t' read -r container zip module polluter victim url <<< "$row"
  cname="af-$zip"; sd="$DATA/$zip"
  log "ROW $container | $module | $victim"
  ensure_subject "$zip" "$url" || { echo "SKIP $container: subject prep failed"; continue; }
  ensure_container "$zip" "$cname"
  SUBJECT_OVERRIDE="$container" "$OUTDIR/od_full.sh" "$cname" "$sd" "$module" "$polluter" "$victim" \
    || echo ">> ROW $container did not complete (see raw/$cname logs); continuing"
done
log "dubbo loop done"
echo "current results.csv:"; cat "$RESULTS" 2>/dev/null
