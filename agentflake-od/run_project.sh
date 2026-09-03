#!/bin/bash
# run_project.sh <project> -- master-sheet-driven OD loop for one project (README-canonical).
# Drives off master-sheet.csv (test_type=od, the canonical unique-test list), joins test_config.csv
# by container==result_container to get the runnable config (zip/module/polluter/victim/url).
# Skips rows already in results.csv; records unmatched canonical tests as NA_NO_CONFIG.
# Handles download/unzip + per-zip container startup; resumable; continues past a failing row.
#   usage: ./run_project.sh ormlite      (or wildfly, shardingsphere, accumulo, ...)
set -uo pipefail
PROJECT="${1:?usage: run_project.sh <project-substring, e.g. ormlite>}"
WORK="$HOME/agentflake-work"; DATA="$WORK/data"; REPO="$HOME/srse-research"; OUTDIR="$REPO/agentflake-od"
RESULTS="$OUTDIR/results.csv"; MS="$WORK/master-sheet.csv"; TC="$WORK/test_config.csv"; IMAGE=flaky_base_jdk8_od_cov
: "${OPENAI_API_KEY:?export OPENAI_API_KEY first}"
[ -f "$MS" ] || { echo "!! master-sheet.csv not found at $MS"; exit 1; }
[ -f "$TC" ] || { echo "!! test_config.csv not found at $TC"; exit 1; }
mkdir -p "$DATA"
log(){ echo "==== $* ===="; }

# canonical join: master-sheet(od, project) -> test_config(container). Emits rows OR marks NA_NO_CONFIG.
mapfile -t ROWS < <(python3 - "$MS" "$TC" "$RESULTS" "$PROJECT" <<'PY'
import csv,sys,os
ms,tc,res,proj=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4].lower()
cfg={r["result_container"]:r for r in csv.DictReader(open(tc))}
done=set()
if os.path.exists(res):
    for line in open(res): done.add(line.split(",",1)[0])
for r in csv.DictReader(open(ms)):
    if r["test_type"].strip().lower()!="od": continue
    cont=r["container"].strip()
    if proj not in (cont+r["Flaky Test Name"]).lower(): continue
    if cont in done: continue
    c=cfg.get(cont)
    if not c:
        print("\t".join([cont,"NA","NA","NA",r["Flaky Test Name"],"NA"])); continue
    print("\t".join([cont,c["zip"],c["module"],c["polluter/state setter"],c["flaky_test"],c["url"]]))
PY
)
[ ${#ROWS[@]} -eq 0 ] && { echo "no remaining $PROJECT OD rows -- all done or none match"; exit 0; }
echo "remaining $PROJECT OD rows: ${#ROWS[@]}"; printf '  %s\n' "${ROWS[@]}" | cut -f1,5

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
  [ -d "$sd/Flaky" ] || { echo "!! no Flaky under $sd"; return 1; }
  [ -f "$DATA/$zip.zip" ] || cp "$sd.zip" "$DATA/$zip.zip" 2>/dev/null || true
}
ensure_container(){ local zip="$1" cname="$2" sd="$DATA/$zip"
  if ! docker inspect "$cname" >/dev/null 2>&1 || [ "$(docker inspect -f '{{.State.Running}}' "$cname" 2>/dev/null)" != "true" ]; then
    docker rm -f "$cname" >/dev/null 2>&1 || true
    local m2="$sd/Flakym2/.m2"
    log "start container $cname"
    if [ -d "$m2" ]; then
      docker run -d --name "$cname" --mount type=bind,source="$(cd "$sd/Flaky" && pwd)",target=/app/source \
        --mount type=bind,source="$(cd "$m2" && pwd)",target=/root/.m2 -e OPENAI_API_KEY="$OPENAI_API_KEY" "$IMAGE" tail -f /dev/null >/dev/null
    else
      docker run -d --name "$cname" --mount type=bind,source="$(cd "$sd/Flaky" && pwd)",target=/app/source \
        -e OPENAI_API_KEY="$OPENAI_API_KEY" "$IMAGE" tail -f /dev/null >/dev/null
    fi
  fi
  log "ensure maven 3.9.9 + python-scripts in $cname"
  docker exec "$cname" bash -lc 'ls /opt/apache-maven-3.9.9/bin/mvn >/dev/null 2>&1 || { echo installing-mvn-3.9.9; curl -sL https://archive.apache.org/dist/maven/maven-3/3.9.9/binaries/apache-maven-3.9.9-bin.tar.gz | tar xz -C /opt; }'
  docker exec "$cname" bash -lc '[ -f /app/source/python-scripts/parse_surefire_report.py ]' 2>/dev/null || docker cp "$WORK/python-scripts" "$cname:/app/source/python-scripts" >/dev/null 2>&1 || true
}

for row in "${ROWS[@]}"; do
  IFS=$'\t' read -r container zip module polluter victim url <<< "$row"
  if [ "$zip" = "NA" ]; then
    log "ROW $container -- no test_config match, recording NA_NO_CONFIG"
    [ -f "$RESULTS" ] || echo "subject,module,focal_method,generated_test,alone,sweep_orders,sweep_pass,ctrl_polluterFirst,ctrl_victimFirst,gen_polluterFirst,od_verdict,notes" > "$RESULTS"
    echo "$container,NA,$victim,NONE,na,0,0,na,na,na,NA_NO_CONFIG,canonical OD test with no test_config entry (not runnable via config)" >> "$RESULTS"
    continue
  fi
  cname="af-$zip"; sd="$DATA/$zip"
  log "ROW $container | $module | $victim"
  ensure_subject "$zip" "$url" || { echo "SKIP $container: subject prep failed"; continue; }
  ensure_container "$zip" "$cname"
  SUBJECT_OVERRIDE="$container" "$OUTDIR/od_full.sh" "$cname" "$sd" "$module" "$polluter" "$victim" \
    || echo ">> ROW $container did not complete (see raw/$cname); continuing"
done
log "$PROJECT loop done"; echo "results now:"; tail -n +2 "$RESULTS" | wc -l; echo "rows total"
