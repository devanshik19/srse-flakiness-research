#!/bin/bash
TODO=~/srse-research/docker_todo.txt
RESULTS=~/srse-research/docker_results.csv
LOGDIR=~/srse-research/docker_logs
PATCHES=~/patches
mkdir -p "$LOGDIR"
touch "$RESULTS"

while read -r ID; do
    [ -z "$ID" ] && continue
    # Skip if already done
    if grep -q "^$ID," "$RESULTS"; then
        echo "SKIP (done): $ID"; continue
    fi
    echo "=== $ID ==="
    LOG="$LOGDIR/${ID}.log"

    # Get test info from helper
    INFO=$(python3 ~/srse-research/helpers/get_instance_info4.py "$ID" 2>/dev/null)
    if [ "$INFO" == "NOTFOUND" ] || [ -z "$INFO" ]; then
        echo "$ID,,,,,,NO_INFO" >> "$RESULTS"; continue
    fi
    REPO=$(echo "$INFO" | cut -d'|' -f1)
    TEST_FILE=$(echo "$INFO" | cut -d'|' -f3)
    TEST_NAME=$(echo "$INFO" | cut -d'|' -f4)
    REPO_NAME=$(echo "$REPO" | cut -d'/' -f2)

    # Check patches exist
    if [ ! -s "$PATCHES/${ID}_golden.patch" ] || [ ! -s "$PATCHES/${ID}_agent.patch" ]; then
        echo "$ID,$REPO_NAME,,,,,NO_PATCH" >> "$RESULTS"; continue
    fi

    IMAGE="ghcr.io/epoch-research/swe-bench.eval.x86_64.${ID}:latest"
    CNAME="run_${ID//[^a-zA-Z0-9]/_}"

    # Pull image
    if ! sudo docker pull "$IMAGE" >> "$LOG" 2>&1; then
        echo "$ID,$REPO_NAME,,,,,PULL_FAIL" >> "$RESULTS"; continue
    fi

    # Start container (detached, sleep to keep alive)
    sudo docker run -d --name "$CNAME" "$IMAGE" sleep infinity >> "$LOG" 2>&1

    # Copy patches + in-container script in
    sudo docker cp "$PATCHES/${ID}_golden.patch" "$CNAME:/testbed/golden.patch" >> "$LOG" 2>&1
    sudo docker cp "$PATCHES/${ID}_agent.patch" "$CNAME:/testbed/agent.patch" >> "$LOG" 2>&1
    sudo docker cp ~/srse-research/in_container.sh "$CNAME:/in_container.sh" >> "$LOG" 2>&1

    # Run the in-container work, capture the result line
    RESULT=$(sudo docker exec "$CNAME" bash /in_container.sh "$ID" "$TEST_FILE" "$TEST_NAME" "$REPO_NAME" 2>>"$LOG" | tail -1)
    if [ -z "$RESULT" ]; then
        RESULT="$ID,$REPO_NAME,,,,,EXEC_EMPTY"
    fi
    echo "$RESULT" >> "$RESULTS"
    echo "  -> $RESULT"

    # Cleanup: stop+remove container, remove image (disk-safe)
    sudo docker rm -f "$CNAME" >> "$LOG" 2>&1
    sudo docker rmi "$IMAGE" >> "$LOG" 2>&1
done < "$TODO"
echo "ALL DONE"
