#!/usr/bin/env python3
# Generate pytest tests for a repo's functions (ChatUniTest-style, GPT-5), then optionally
# VALIDATE (run each test) and REPAIR (feed the error back to the model once).
# Generated tests are written into <repo>/_gen_tests/ so they can import the repo's modules.
#
# Usage:
#   OPENAI_API_KEY=... python3 gen_tests.py <repo> <out_dir> \
#       [--limit N] [--model gpt-5-nano] [--budget USD] [--validate] [--repair]
import argparse, ast, csv, os, re, subprocess
from pathlib import Path
from openai import OpenAI

SKIP = {".git", ".venv", "venv", "env", "node_modules", "build", "dist", ".tox",
        "__pycache__", "tests", "test", "docs", "examples", "_gen_tests"}
SKIP_FILES = {"conftest.py", "setup.py", "isympy.py", "__init__.py", "setup_cython.py"}
client = OpenAI()

# USD per 1M tokens (input, output)
PRICES = {
    "gpt-5": (1.25, 10.0), "gpt-5.1": (1.25, 10.0), "gpt-5.2": (1.75, 14.0),
    "gpt-5-mini": (0.25, 2.0), "gpt-5-nano": (0.05, 0.40),
    "gpt-5.4-mini": (0.75, 4.50), "gpt-5.4-nano": (0.20, 1.25),
    "gpt-4o": (2.50, 10.0), "gpt-4o-mini": (0.15, 0.60),
}

# ChatUniTest's initial_system.ftl prompt, ported Java -> Python/pytest.
SYSTEM = (
    "Please help me generate a complete pytest test for a focal function in a focal module/class.\n"
    "I will provide the following information about the focal function:\n"
    "1. Required dependencies to import.\n"
    "2. The focal class signature.\n"
    "3. Source code of the focal function.\n"
    "4. Signatures of other methods and fields in the class.\n"
    "I need you to create a complete unit test using pytest, ensuring optimal branch and line "
    "coverage. The test must import/run without errors. No additional explanations required."
)

REPAIR_SYSTEM = (
    "You previously wrote a pytest test that failed to run. I will give you the test and its "
    "pytest error output. Fix the test so it imports and runs. Return only the corrected test "
    "code inside one ```python code block, no explanation."
)


def _call(messages, model):
    kw = dict(model=model, messages=messages)
    if model.startswith("gpt-5"):
        kw["reasoning_effort"] = "minimal"
        kw["max_completion_tokens"] = 2500
    else:
        kw["max_tokens"] = 2500
    r = client.chat.completions.create(**kw)
    text = r.choices[0].message.content or ""
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.S)
    code = (m.group(1) if m else text).strip()
    return code, r.usage.prompt_tokens, r.usage.completion_tokens


def sig(node):
    return f"{node.name}({', '.join(a.arg for a in node.args.args)})"


def focal_contexts(path, rel):
    try:
        src = path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(src)
    except Exception:
        return
    lines = src.splitlines()
    body = lambda n: "\n".join(lines[n.lineno - 1:n.end_lineno])
    imports = [body(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and not n.name.startswith("_"):
            yield {"name": n.name, "module": rel, "cls": None, "fields": [], "siblings": [],
                   "src": body(n), "imports": imports}
        elif isinstance(n, ast.ClassDef):
            methods = [m for m in n.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
            fields = [t.id for m in n.body if isinstance(m, ast.Assign)
                      for t in m.targets if isinstance(t, ast.Name)]
            sigs = [sig(m) for m in methods]
            for m in methods:
                if m.name.startswith("_") and m.name != "__init__":
                    continue
                yield {"name": m.name, "module": rel, "cls": n.name, "fields": fields,
                       "siblings": sigs, "src": body(m), "imports": imports}


def build_prompt(fc):
    parts = [
        f"Module path: {fc['module']}", "",
        "1. Required dependencies to import:", ("\n".join(fc["imports"]) or "(none)"), "",
        "2. Focal class signature:",
        (f"class {fc['cls']}:" if fc["cls"] else "(module-level function, not in a class)"), "",
        "3. Source code of the focal function:", fc["src"], "",
        "4. Other methods and fields in the class:",
        (f"fields: {', '.join(fc['fields']) or 'none'}\nmethods: {', '.join(fc['siblings'])}"
         if fc["cls"] else "(n/a)"), "",
        f"Write the pytest test for `{fc['name']}`. Return only the test code in one ```python block.",
    ]
    return "\n".join(parts)


def generate(fc, model):
    return _call([{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": build_prompt(fc)}], model)


def repair(fc, code, err, model):
    msg = f"# Test for `{fc['name']}`:\n{code}\n\n# pytest error output:\n{err}\n\nFix it."
    return _call([{"role": "system", "content": REPAIR_SYSTEM},
                  {"role": "user", "content": msg}], model)


def run_test(repo, code, fname):
    gendir = Path(repo) / "_gen_tests"
    gendir.mkdir(exist_ok=True)
    (gendir / fname).write_text(code)
    try:
        r = subprocess.run(
            ["python", "-m", "pytest", f"_gen_tests/{fname}", "-q", "-p", "no:cacheprovider"],
            cwd=repo, capture_output=True, text=True, timeout=120,
        )
        return r.returncode == 0, (r.stdout + r.stderr)[-1500:]
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("out")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default="gpt-5-nano")
    ap.add_argument("--budget", type=float, default=0.0, help="stop when spend exceeds USD (0=no cap)")
    ap.add_argument("--validate", action="store_true", help="run each generated test")
    ap.add_argument("--repair", action="store_true", help="on failure, ask the model to fix it once")
    a = ap.parse_args()

    pin, pout = PRICES.get(a.model, (0.0, 0.0))
    spent = 0.0
    repo, out = Path(a.repo), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    man = csv.writer(open(out / "manifest.csv", "w", newline=""))
    man.writerow(["module", "class", "function", "test_file", "status"])

    n = 0
    for dp, dn, fn in os.walk(repo):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            if not f.endswith(".py") or f.startswith("test_") or f in SKIP_FILES:
                continue
            p = Path(dp) / f
            rel = str(p.relative_to(repo)).replace(os.sep, "/")
            for fc in focal_contexts(p, rel):
                try:
                    code, it, ot = generate(fc, a.model)
                except Exception as e:
                    print(f"  SKIP {rel}::{fc['name']} ({e})", flush=True)
                    continue
                spent += it / 1e6 * pin + ot / 1e6 * pout
                fname = "test_" + re.sub(r"[^A-Za-z0-9]+", "_", rel[:-3]) + f"__{fc['name']}.py"
                status = "generated"
                if a.validate:
                    ok, err = run_test(repo, code, fname)
                    status = "pass" if ok else "fail"
                    if not ok and a.repair:
                        try:
                            code, rit, rot = repair(fc, code, err, a.model)
                            spent += rit / 1e6 * pin + rot / 1e6 * pout
                            ok, err = run_test(repo, code, fname)
                            status = "pass(repaired)" if ok else "fail(repaired)"
                        except Exception as e:
                            status = f"repair_error"
                (Path(repo) / "_gen_tests" / fname).write_text(code)
                man.writerow([fc["module"], fc["cls"] or "", fc["name"], fname, status])
                n += 1
                print(f"[{n}] {rel}::{fc['name']} | {status} | ${spent:.4f}", flush=True)
                if a.budget and spent >= a.budget:
                    print(f"BUDGET ${a.budget} reached (${spent:.4f}). Stopping."); return
                if a.limit and n >= a.limit:
                    print(f"done (limit) {n}, ${spent:.4f} spent"); return
    print(f"done {n}, ${spent:.4f} spent")


if __name__ == "__main__":
    main()
