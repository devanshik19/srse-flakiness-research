#!/usr/bin/env python3
# flaky_report.py <docker_results.csv> [--md django_flaky.md] [--repo-prefix flaky_tests/django]
#
# One source of truth for the flakiness numbers. Reads the per-run verdict log
# (columns: instance,phase,run,test,verdict) and reports, at function and file level:
#   - which tests are flaky and in WHICH regime(s) they flip
#   - per-regime flaky counts (how the paper's by-regime table is built)
#   - a category per flaky test: ND / NOD / OD (see classify() below)
# Optionally (--md) regenerates the file-level django_flaky.md deliverable.
#
# A test is flaky if its verdict is not identical across all runs of a regime.
# Regimes expected in the new runs: baseline, cpu, io, memory, hashseed, order.
import csv, sys, argparse
from collections import defaultdict

# regimes that are resource-stress (timing/race), vs the two isolation levers
STRESS = {"cpu", "io", "memory"}


def load(path):
    """(instance, func) -> {phase: set(verdicts)}"""
    funcs = defaultdict(lambda: defaultdict(set))
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            key = (r["instance"], r["test"].strip('"'))
            funcs[key][r["phase"]].add(r["verdict"])
    return funcs


def flips_in(phasemap):
    """regimes where this function changed verdict across runs."""
    return {p for p, vs in phasemap.items() if len(vs) > 1}


def classify(regimes):
    """Bucket a flaky test by the strongest cause present.
       ND  = flips with fixed order AND fixed seed (baseline) -> intrinsic non-determinism
       NOD = flips under random hash seed only (not order)    -> hash-ordering dependence
       OD  = flips only under random test order               -> order-dependent (isolation)
    """
    if "baseline" in regimes:
        return "ND"
    if "order" in regimes and "hashseed" not in regimes:
        return "OD"
    if "hashseed" in regimes and "order" not in regimes:
        return "NOD"
    if "order" in regimes or "hashseed" in regimes:
        return "OD+NOD"            # flips under both levers
    if regimes & STRESS:
        return "STRESS"            # only under cpu/io/memory load
    return "OTHER"


def verdicts_only_errorfail(phasemap, regimes):
    """True if every flipping regime only toggles ERROR<->FAILED (a broken test with a
       nondeterministic failure TYPE), not a real PASS<->FAIL flake."""
    seen = set()
    for p in regimes:
        seen |= phasemap[p]
    return seen and seen <= {"ERROR", "FAILED"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--md", help="write file-level markdown here (e.g. django_flaky.md)")
    ap.add_argument("--repo-prefix", default="flaky_tests/django",
                    help="path prefix for test body links in the markdown")
    a = ap.parse_args()

    funcs = load(a.csv)
    all_phases = sorted({p for pm in funcs.values() for p in pm})

    flaky = []   # (inst, func, regimes, category, errorfail_only)
    for (inst, func), pm in sorted(funcs.items()):
        regimes = flips_in(pm)
        if regimes:
            flaky.append((inst, func, regimes, classify(regimes),
                          verdicts_only_errorfail(pm, regimes)))

    flaky_files = {(i, fn.split("::")[0]) for i, fn, *_ in flaky}
    all_files = {(i, fn.split("::")[0]) for (i, fn) in funcs}

    # ---- per-test detail (what regime each flips in) ----
    for inst, func, regimes, cat, ef in flaky:
        pm = funcs[(inst, func)]
        detail = "  ".join(f"{p}={sorted(pm[p])}" for p in all_phases if p in pm)
        tag = f"{cat}" + (" [ERROR/FAILED-only]" if ef else "")
        print(f"FLAKY [{tag}]  {inst}  {func}")
        print(f"       {detail}")

    # ---- totals ----
    print(f"\nfunctions: {len(flaky)} flaky / {len(funcs)} total")
    print(f"files:     {len(flaky_files)} flaky / {len(all_files)} total")

    # ---- per-regime counts (a function can flip in several -> columns overlap) ----
    print("\nby regime (overlapping):")
    for p in all_phases:
        fns = sum(1 for _, _, regs, *_ in flaky if p in regs)
        fls = len({(i, fn.split('::')[0]) for i, fn, regs, *_ in flaky if p in regs})
        print(f"  {p:9s} functions={fns:3d}  files={fls:3d}")

    # ---- by category ----
    print("\nby category:")
    cats = defaultdict(int)
    for *_, cat, ef in flaky:
        cats[cat] += 1
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {c:8s} {n}")
    pf = sum(1 for *_, ef in flaky if not ef)
    print(f"  (of these, {pf} are real PASS<->FAIL flakes; "
          f"{len(flaky)-pf} only toggle ERROR<->FAILED of a broken test)")

    if a.md:
        write_md(a.md, flaky, flaky_files, all_files, a.repo_prefix)
        print(f"\nwrote {a.md}")


def write_md(path, flaky, flaky_files, all_files, prefix):
    import re as _re
    ORDER = ["baseline", "cpu", "io", "memory", "hashseed", "order"]

    def focal_of(base):            # test_collect__3.py -> collect
        return _re.sub(r"^test_", "", _re.sub(r"__\d+\.py$", "", base))

    def run_of(base):              # test_collect__3.py -> 4  (sample k -> run k+1)
        m = _re.search(r"__(\d+)\.py$", base)
        return int(m.group(1)) + 1 if m else 0

    # inst -> focal -> run -> {file, n flaky funcs, regimes}
    tree = defaultdict(lambda: defaultdict(dict))
    for inst, func, regimes, cat, ef in flaky:
        base = func.split("::")[0].split("/")[-1]
        rec = tree[inst][focal_of(base)].setdefault(run_of(base),
                                                     {"base": base, "n": 0, "regimes": set()})
        rec["n"] += 1
        rec["regimes"] |= regimes

    lines = []
    lines.append("# Django — Flaky LLM-Generated Test Files\n")
    lines.append(f"**{len(flaky_files)} flaky test files** (of {len(all_files)} that ran), from "
                 f"**{sum(len(v) for v in tree.values())} focal methods**. Grouped by instance → focal "
                 "method → generation run (run N = the Nth of the 10 generated samples for that method). "
                 "Each run links to its test body; \"flaky functions\" = how many `def test_` in it flip; "
                 "\"flips in\" = the regime(s) where flipping occurs. Regimes: baseline, cpu/io/memory "
                 "stress, hashseed (random `PYTHONHASHSEED`, fixed order), order (random test order).\n")
    for inst in sorted(tree):
        lines.append(f"\n## {inst}\n")
        for focal in sorted(tree[inst]):
            runs = tree[inst][focal]
            lines.append(f"### focal method: `{focal}`  ({len(runs)} flaky run(s))\n")
            lines.append("| run | file | flaky functions | flips in |")
            lines.append("|---|---|---|---|")
            for rn in sorted(runs):
                rec = runs[rn]
                regs = ",".join([r for r in ORDER if r in rec["regimes"]]
                                + sorted(rec["regimes"] - set(ORDER)))
                link = f"{prefix}/{inst}/{rec['base']}"
                lines.append(f"| {rn} | [`{rec['base']}`]({link}) | {rec['n']} | {regs} |")
            lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
