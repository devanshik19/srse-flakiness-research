#!/usr/bin/env python3
"""stress_check.py -- cpu + memory stress flakiness on the generated tests.

The Java/Maven analogue of the SWE-bench Django stress regime: it reuses the package's existing
`rerun` check (each test method on its own, --runs times, fresh JVM, "passes AND fails" = flaky)
and runs it UNDER stress-ng load, once per regime. Nothing in the package is modified; only
`flaky_check.py rerun` is invoked.

Run inside the flaky_check_package folder, after the archives are set up (setup_archives.py):

    python3 stress_check.py --tests task_csvs/flaky_generated_tests.csv --archive-dir extracted
    python3 stress_check.py --tests task_csvs/td_main.csv              --archive-dir extracted

Regimes (default cpu,memory -- io is intentionally excluded per the mentor):
    baseline : no stress            (optional control: --regimes baseline,cpu,memory)
    cpu      : stress-ng --cpu <N>
    memory   : stress-ng --vm 2 --vm-bytes <BYTES>

Per regime, a method that both passes and fails is stress-flaky for that regime. Writes
<out>/stress_results.csv (one row per method: pass/fail/runs + a flaky flag per regime), and the
raw per-run logs stay under <out>/<regime>/ exactly as the package's rerun writes them.

Resumable: each regime's rerun resumes per method after its last recorded run (the package handles
that). Re-running stress_check continues where rerun left off and rewrites stress_results.csv.

IMPORTANT: do not run this while a FlakeRake (TD) run is active -- stress-ng corrupts TD timing.
"""
import argparse
import csv
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

# matches the Django docker_validate.sh stress array (cpu = all-core load; memory = bounded vm)
def stressor_cmd(name, a):
    if name == "cpu":
        return ["stress-ng", "--cpu", str(a.cpu_workers)]
    if name == "memory":
        return ["stress-ng", "--vm", "2", "--vm-bytes", a.vm_bytes]
    return None  # baseline: no stressor


def rerun_counts(path):
    """{(id, test): [passed, failed, runs, errors]} -- same rule as the package's rerun_counts."""
    counts = {}
    if path.is_file():
        for r in csv.DictReader(open(path, encoding="utf-8")):
            c = counts.setdefault((r["id"], r["test"]), [0, 0, 0, 0])
            c[0] += r["outcome"] == "passed"
            c[1] += r["outcome"] in ("failed", "rerun_passed")
            c[2] += 1
            c[3] += r["outcome"] in ("error", "timeout")
    return counts


def run_regime(name, a):
    reg_out = (a.out / name).resolve()
    reg_out.mkdir(parents=True, exist_ok=True)
    sp = None
    cmd = stressor_cmd(name, a)
    if cmd:
        print(f"\n=== {name} stress: starting `{' '.join(cmd)}` ===", flush=True)
        sp = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        if sp.poll() is not None:                       # stressor died on start
            print(f"!! {name} stressor died immediately; skipping regime", file=sys.stderr)
            return reg_out / "runs.csv"
    else:
        print(f"\n=== {name} (no stress) ===", flush=True)
    try:
        rr = [sys.executable, str(HERE / "flaky_check.py"), "rerun",
              "--tests", str(a.tests), "--runs", str(a.runs), "--out", str(reg_out),
              "--maven-repo", str(a.maven_repo)]
        for d in a.archive_dir:
            rr += ["--archive-dir", str(d)]
        for o in a.only:
            rr += ["--only", o]
        if a.offline:
            rr += ["--offline"]
        subprocess.run(rr, check=False)
    finally:
        if sp:
            sp.terminate()
            try:
                sp.wait(timeout=10)
            except subprocess.TimeoutExpired:
                sp.kill()
            subprocess.run(["pkill", "-x", "stress-ng"], stderr=subprocess.DEVNULL)
    return reg_out / "runs.csv"


def main():
    a = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--tests", type=Path, required=True)
    a.add_argument("--archive-dir", type=Path, action="append", default=[])
    a.add_argument("--runs", type=int, default=10, help="runs per method per regime (default 10)")
    a.add_argument("--out", type=Path, default=HERE / "flaky_check_out" / "stress")
    a.add_argument("--only", action="append", default=[])
    a.add_argument("--maven-repo", type=Path, default=Path.home() / ".m2" / "repository")
    a.add_argument("--regimes", default="cpu,memory", help="comma list of baseline,cpu,memory")
    a.add_argument("--cpu-workers", type=int, default=os.cpu_count() or 2)
    a.add_argument("--vm-bytes", default="256M")
    a.add_argument("--offline", action="store_true", help="pass --offline to rerun after first build")
    args = a.parse_args()
    if not (HERE / "flaky_check.py").is_file():
        sys.exit(f"{HERE} is not the package folder (flaky_check.py missing). cd into it.")
    if not args.archive_dir:
        args.archive_dir = [HERE / "extracted"]
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)

    regs = [r.strip() for r in args.regimes.split(",") if r.strip()]
    counts = {}
    for name in regs:
        counts[name] = rerun_counts(run_regime(name, args))

    # ---- combine into one results table ----
    keys = set()
    for c in counts.values():
        keys |= set(c)
    fields = ["id", "test"]
    for r in regs:
        fields += [f"{r}_pass", f"{r}_fail", f"{r}_runs", f"{r}_flaky"]
    fields += ["any_stress_flaky"]
    res = args.out / "stress_results.csv"
    nflaky = 0
    with res.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        for k in sorted(keys):
            row = {"id": k[0], "test": k[1]}
            anyf = False
            for r in regs:
                p, fl, ru, er = counts[r].get(k, [0, 0, 0, 0])
                flaky = p > 0 and fl > 0                 # passed AND failed under this regime
                anyf = anyf or flaky
                row[f"{r}_pass"], row[f"{r}_fail"], row[f"{r}_runs"], row[f"{r}_flaky"] = p, fl, ru, flaky
            row["any_stress_flaky"] = anyf
            nflaky += anyf
            w.writerow(row)
    print(f"\nwrote {res}")
    print(f"regimes={regs} runs={args.runs}  methods={len(keys)}  stress-flaky={nflaky}")


if __name__ == "__main__":
    main()
