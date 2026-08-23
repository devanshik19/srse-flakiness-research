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

# Find all files in the patch
all_files = re.findall(r'\+\+\+ b/(\S+)', agent_patch)

# Directories/names that are NOT real test files (fixtures, sample data, config)
EXCLUDE = ('tests/roots/', '/target/', 'conftest.py', 'models.py', '__init__.py', '/fixtures/')

def is_real_test_file(f):
    if not f.endswith('.py'):
        return False
    if any(bad in f for bad in EXCLUDE):
        return False
    # a real test file usually has 'test' in the filename itself
    fname = f.split('/')[-1]
    return fname.startswith('test_') or fname.endswith('_test.py') or 'test' in fname

# Prefer a real test file; fall back to any .py with 'test' in the path
test_file = ""
for f in all_files:
    if is_real_test_file(f):
        test_file = f
        break
if not test_file:
    for f in all_files:
        if f.endswith('.py') and 'test' in f.lower() and not any(bad in f for bad in EXCLUDE):
            test_file = f
            break
if not test_file and all_files:
    test_file = all_files[0]

# Find the test function name. Prefer a NEW function added in the chosen test file.
test_name = ""
if test_file:
    # isolate the diff hunk for the chosen test file
    file_section = ""
    sections = agent_patch.split('diff --git')
    for s in sections:
        if test_file in s:
            file_section = s
            break
    func_match = re.search(r'\+\s*def (test_\w+)', file_section)
    if func_match:
        test_name = func_match.group(1)

# fallback: any added test function anywhere in the patch
if not test_name:
    func_match = re.search(r'\+\s*def (test_\w+)', agent_patch)
    test_name = func_match.group(1) if func_match else ""

with open("/home/dev4nshik/swebench_lookup.json") as f:
    lookup = json.load(f)

row = lookup.get(instance_id)
if row is None:
    print("NOTFOUND"); sys.exit(0)

with open(f"/home/dev4nshik/patches/{instance_id}_golden.patch", "w") as out:
    out.write(row["patch"])

print(f"{row['repo']}|{row['base_commit']}|{test_file}|{test_name}")

