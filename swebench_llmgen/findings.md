# LLM-Generated Test Flakiness on SWE-bench — Findings So Far

Measure how flaky **LLM-generated tests** are. Generate pytest tests with GPT for
Python codebases (SWE-bench), then run each many times — at rest and under `stress-ng` load — and
count which ones flip verdict.

## Pipeline

| stage | script | what it does |
|---|---|---|
| targets | `extract_focal_swebench.py` | reads SWE-bench Verified gold patches, extracts the **focal method** each bug fix touches |
| generate | `phase1_focal.py` | GPT writes N pytest tests per focal method (ChatUniTest-style prompt) |
| validate + stress | `docker_validate.sh` | runs the tests inside each instance's Docker image (correct Python/deps), N× baseline + N× under CPU stress, logs each test's verdict per run |
| repair | `docker_repair.py` | feeds a broken test's error back to GPT once; reverts if no better |
| detect | `flaky.py` | flags any test whose verdict is not identical across all runs |

## Setup

- Subject benchmark: **SWE-bench Verified** (500 real GitHub bug instances, 12 Python repos).
- Focal methods extracted: **923** across the 500 instances (django 384, sympy 185, sphinx 80,
  sklearn 61, matplotlib 55, pytest 41, xarray 39, astropy 39, pylint 25, requests 9, seaborn 4,
  flask 1) → `swebench_focal.csv`.
- Execution env: per-instance **Epoch AI Docker images** (`ghcr.io/epoch-research/swe-bench.eval.*`),
  which pin the correct historical Python + dependencies (conda env `testbed`). Needed because old
  SWE-bench commits break on modern Python.
- Generation model: **gpt-5-mini** (to prove the pipeline cheaply); the real dataset run will use
  full **gpt-5**.
- Stress: `stress-ng --class cpu --all 1` on the host; the container shares host CPU.

## First batch — sympy

20 focal methods (CSV rows 1–20) → 5 instances → **200 test files / 1,200 test functions**.
Each run **15× baseline + 15× under CPU stress** (30 runs total).

| metric | value |
|---|---|
| test files generated | 200 |
| files that ran (valid) | **196 / 200 (~98%)** |
| test functions exercised | 1,200 |
| **flaky under CPU stress** | **0** |
| generation cost | ~$0.33 (gpt-5-mini) |

**Result: 0 flaky across 1,200 AI-generated sympy test functions.** This is expected, not a dud:
sympy focal methods are pure deterministic math (`distance`, `conjugate`, permutation algebra), so
CPU contention cannot change their outputs — there is nothing for load to perturb.

## Methodology note (a measurement bug we fixed)

An early run showed only 40/200 files "running" — it looked like 80% of generated tests were invalid.
Root cause was **not** test quality: pytest **aborts the entire run if any file fails to collect**,
so ~4 genuinely broken files wiped out two whole instances (150 + 10 files). Adding
`--continue-on-collection-errors` fixed it, lifting the real validity rate to ~98%. The ~4 broken
files (bad import / nonexistent API against the old commit) are exactly what the repair step targets.

Other hardening: generated tests are mounted **read-only** in Docker (so runs can't corrupt them),
and per-instance images are deleted after use to bound disk.

## Takeaways / next steps

- **CPU stress on deterministic code yields no flakiness.** sympy is confirmed a poor hunting ground.
- Flakiness in LLM-generated tests is expected to come from (a) **nondeterminism in the test itself**
  — set/dict/str ordering, unseeded `random`, time/date, hash order (common in LLM-written tests), and
  (b) **timing/ordering/I/O races** — which live in django / requests / matplotlib. (Consistent with
  the "Large Language Monkeys" paper, whose flaky SWE-bench set was 25/34 django.)
- Next: add a **nondeterminism lever** (randomize `PYTHONHASHSEED` + test order per run) and point the
  pipeline at **requests / django / matplotlib**; scale generation to full gpt-5 once the funded key
  is available.
