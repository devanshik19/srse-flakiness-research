#!/usr/bin/env python3
# Phase 1 - generate N pytest tests per SWE-bench focal method (one repo), validate + repair.
# Reads swebench_focal.csv, filters to --repo, checks out each instance's base_commit,
# generates N tests for the focal function, runs each, repairs failures once.
#
# Usage:
#   OPENAI_API_KEY=... python3 phase1_focal.py swebench_focal.csv ~/sympy \
#       --repo sympy/sympy --count 10 [--limit M] [--model gpt-5-mini] [--budget 0.50] [--repair]
import argparse, ast, csv, re, subprocess
from collections import defaultdict
from pathlib import Path
from openai import OpenAI

client = OpenAI()
PRICES = {"gpt-5": (1.25, 10.0), "gpt-5-mini": (0.25, 2.0), "gpt-5-nano": (0.05, 0.40),
          "gpt-4o": (2.5, 10.0), "gpt-4o-mini": (0.15, 0.60)}

SYSTEM = (
    "Please help me generate a complete pytest test for a focal function in a focal module/class.\n"
    "I will provide: 1. Required dependencies to import. 2. The focal class signature. "
    "3. Source code of the focal function. 4. Signatures of other methods and fields in the class.\n"
    "Create a complete pytest test with good branch/line coverage. It must import/run without "
    "errors. No additional explanations required."
)
REPAIR_SYSTEM = (
    "You previously wrote a pytest test that failed to run. I give you the test and its pytest "
    "error output. Fix it so it imports and runs. Return only the corrected code in one ```python block."
)


def _call(messages, model):
    kw = dict(model=model, messages=messages)
    if model.startswith("gpt-5"):
        kw["reasoning_effort"] = "minimal"; kw["max_completion_tokens"] = 2500
    else:
        kw["max_tokens"] = 2500
    r = client.chat.completions.create(**kw)
    text = r.choices[0].message.content or ""
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    return (m.group(1) if m else text).strip(), r.usage.prompt_tokens, r.usage.completion_tokens


def sig(n):
    return f"{n.name}({', '.join(a.arg for a in n.args.args)})"


def find_focal(repo, file, name):
    """Locate the focal function by name in <repo>/<file>; return its context or None."""
    try:
        src = (Path(repo) / file).read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(src)
    except Exception:
        return None
    lines = src.splitlines()
    body = lambda n: "\n".join(lines[n.lineno - 1:n.end_lineno])
    imports = [body(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name:
            return {"name": name, "module": file, "cls": None, "fields": [], "siblings": [],
                    "src": body(n), "imports": imports}
        if isinstance(n, ast.ClassDef):
            methods = [m for m in n.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
            for m in methods:
                if m.name == name:
                    fields = [t.id for mm in n.body if isinstance(mm, ast.Assign)
                              for t in mm.targets if isinstance(t, ast.Name)]
                    return {"name": name, "module": file, "cls": n.name, "fields": fields,
                            "siblings": [sig(x) for x in methods], "src": body(m), "imports": imports}
    return None


def build_prompt(fc):
    return "\n".join([
        f"Module path: {fc['module']}", "",
        "1. Required dependencies to import:", ("\n".join(fc["imports"]) or "(none)"), "",
        "2. Focal class signature:",
        (f"class {fc['cls']}:" if fc["cls"] else "(module-level function, not in a class)"), "",
        "3. Source code of the focal function:", fc["src"], "",
        "4. Other methods and fields in the class:",
        (f"fields: {', '.join(fc['fields']) or 'none'}\nmethods: {', '.join(fc['siblings'])}"
         if fc["cls"] else "(n/a)"), "",
        "Note: this is a historical/older version of the codebase. Use ONLY the functions, classes, "
        "and imports shown above (plus the Python standard library). Do NOT assume any newer API "
        "exists. Prefer a focused, minimal test over using many helpers.",
        "",
        f"Write the pytest test for `{fc['name']}`. Return only the test code in one ```python block.",
    ])


def run_test(repo, code, fname):
    g = Path(repo) / "_gen_tests"; g.mkdir(exist_ok=True)
    (g / fname).write_text(code)
    try:
        r = subprocess.run(["python", "-m", "pytest", f"_gen_tests/{fname}", "-q", "-p", "no:cacheprovider"],
                           cwd=repo, capture_output=True, text=True, timeout=120)
        return r.returncode == 0, (r.stdout + r.stderr)[-1500:]
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("focal_csv")
    ap.add_argument("repo_dir")
    ap.add_argument("--repo", required=True, help="repo column value, e.g. sympy/sympy")
    ap.add_argument("--count", type=int, default=10, help="tests per focal method")
    ap.add_argument("--limit", type=int, default=0, help="process this many focal rows (0=all)")
    ap.add_argument("--skip", type=int, default=0, help="skip the first N focal rows (for batching)")
    ap.add_argument("--model", default="gpt-5-mini")
    ap.add_argument("--budget", type=float, default=0.0)
    ap.add_argument("--repair", action="store_true")
    ap.add_argument("--validate", action="store_true",
                    help="run tests locally (off by default — use Docker for SWE-bench commits)")
    ap.add_argument("--out", default="gen_out")
    a = ap.parse_args()

    pin, pout = PRICES.get(a.model, (0.0, 0.0))
    spent = 0.0
    rows = [r for r in csv.DictReader(open(a.focal_csv, newline=""))
            if r["repo"] == a.repo and r["focal_function"]]
    groups = defaultdict(list)
    for r in rows:
        groups[r["base_commit"]].append((r["instance_id"], r["file"], r["focal_function"]))

    Path(a.out).mkdir(parents=True, exist_ok=True)
    man = csv.writer(open(Path(a.out) / "manifest.csv", "w", newline=""))
    man.writerow(["instance_id", "commit", "file", "function", "test_idx", "test_file", "status"])

    seen = 0            # focal rows passed (for --skip/--limit windowing)
    methods_done = 0
    for commit, items in groups.items():
        checked_out = False
        for instance, file, func in items:
            seen += 1
            if seen <= a.skip:
                continue
            if a.limit and seen > a.skip + a.limit:
                print(f"batch done: rows {a.skip + 1}-{a.skip + a.limit}, ${spent:.4f} spent"); return
            if not checked_out:
                subprocess.run(["git", "-C", a.repo_dir, "checkout", "-q", commit], check=False)
                checked_out = True
            fc = find_focal(a.repo_dir, file, func)
            if not fc:
                man.writerow([instance, commit, file, func, "", "", "not_found"]); continue
            for k in range(a.count):
                try:
                    code, it, ot = _call([{"role": "system", "content": SYSTEM},
                                          {"role": "user", "content": build_prompt(fc)}], a.model)
                except Exception as e:
                    print(f"  SKIP {func} ({e})", flush=True); continue
                spent += it / 1e6 * pin + ot / 1e6 * pout
                fname = f"test_{func}__{k}.py"
                status = "generated"
                if a.validate:
                    ok, err = run_test(a.repo_dir, code, fname)
                    status = "pass" if ok else "fail"
                    if not ok and a.repair:
                        try:
                            code, rit, rot = _call([{"role": "system", "content": REPAIR_SYSTEM},
                                                    {"role": "user", "content": f"# Test:\n{code}\n\n# error:\n{err}\n\nFix it."}], a.model)
                            spent += rit / 1e6 * pin + rot / 1e6 * pout
                            ok, err = run_test(a.repo_dir, code, fname)
                            status = "pass(repaired)" if ok else "fail(repaired)"
                        except Exception:
                            status = "repair_error"
                outp = Path(a.out) / instance; outp.mkdir(parents=True, exist_ok=True)
                (outp / fname).write_text(code)
                man.writerow([instance, commit, file, func, k, str(outp / fname), status])
                print(f"  {instance} | {func} #{k+1}/{a.count} | {status} | ${spent:.4f}", flush=True)
                if a.budget and spent >= a.budget:
                    print(f"BUDGET ${a.budget} reached (${spent:.4f})."); return
            methods_done += 1
            print(f"[row {seen}] done {instance}::{func}", flush=True)
    print(f"done {methods_done} methods ({seen} rows seen), ${spent:.4f} spent")


if __name__ == "__main__":
    main()
