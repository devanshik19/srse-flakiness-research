import sys, json, re

instance_id = sys.argv[1]

with open("/home/dev4nshik/swt_predictions/swt-verified/lstar_agent_verified.json") as f:
    data = json.load(f)

entry = next((e for e in data if e["instance_id"] == instance_id), None)
if entry is None:
    print("NOTFOUND"); sys.exit(0)

agent_patch = entry["model_patch"]
with open(f"/home/dev4nshik/patches/{instance_id}_agent.patch", "w") as out:
    out.write(agent_patch)

file_match = re.search(r'\+\+\+ b/(\S+)', agent_patch)
test_file = file_match.group(1) if file_match else ""
func_match = re.search(r'\+def (test_\w+)', agent_patch)
test_name = func_match.group(1) if func_match else ""

with open("/home/dev4nshik/swebench_lookup.json") as f:
    lookup = json.load(f)

row = lookup.get(instance_id)
if row is None:
    print("NOTFOUND"); sys.exit(0)

with open(f"/home/dev4nshik/patches/{instance_id}_golden.patch", "w") as out:
    out.write(row["patch"])

print(f"{row['repo']}|{row['base_commit']}|{test_file}|{test_name}")

