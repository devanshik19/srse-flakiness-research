#!/usr/bin/env python3
# Clone each agent repo, collect every test (AST — no install).
# Usage: collect_agents.py <repos.csv> <out_dir>
#   repos.csv: repo,repo_url
#   writes <out_dir>/<name>_all_tests.csv  with columns: test_id,name,module,sha
import ast, csv, os, shutil, subprocess, sys, tempfile, warnings
from pathlib import Path
warnings.filterwarnings("ignore")  # some repos' test files have invalid escape seqs

SKIP = {".git", ".venv", "venv", "node_modules", "build", "dist", ".tox", "__pycache__", ".pytest_cache"}


def tests_in(path, rel):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test"):
            yield f"{rel}::{n.name}", n.name, rel
        elif isinstance(n, ast.ClassDef) and n.name.startswith("Test"):
            for s in n.body:
                if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef)) and s.name.startswith("test"):
                    yield f"{rel}::{n.name}::{s.name}", f"{n.name}.{s.name}", rel


repos_csv, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)

for r in csv.DictReader(open(repos_csv, newline="")):
    repo, url = r["repo"], r["repo_url"]
    d = Path(tempfile.mkdtemp())
    try:
        subprocess.run(["git", "clone", "--depth", "1", "-q", url, str(d)], check=True)
        sha = subprocess.check_output(["git", "-C", str(d), "rev-parse", "HEAD"], text=True).strip()
        fpath = Path(out_dir) / f"{repo.split('/')[-1]}_all_tests.csv"
        w = csv.writer(open(fpath, "w", newline=""))
        w.writerow(["test_id", "name", "module", "sha"])
        n = 0
        for dp, dn, fn in os.walk(d):
            dn[:] = [x for x in dn if x not in SKIP]
            for f in fn:
                if f.endswith(".py") and (f.startswith("test_") or f.endswith("_test.py")):
                    p = Path(dp) / f
                    rel = str(p.relative_to(d)).replace(os.sep, "/")
                    for tid, nm, mod in tests_in(p, rel):
                        w.writerow([tid, nm, mod, sha]); n += 1
        print(f"{repo}: {n} tests @ {sha} -> {fpath.name}", flush=True)
    except subprocess.CalledProcessError:
        print(f"{repo}: CLONE FAILED", file=sys.stderr, flush=True)
    finally:
        shutil.rmtree(d, ignore_errors=True)
