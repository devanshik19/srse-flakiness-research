# LLM-Generated Test Flakiness on SWE-bench — Findings So Far

Goal: measure how flaky **LLM-generated tests** are. We generate pytest tests with GPT for real
Python codebases (SWE-bench), then run each many times — at rest and under `stress-ng` load — and
count which ones flip verdict. A test that passes at rest but fails under load (or flips run-to-run)
is flaky.

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

## Django — first flaky tests found

To run Django's ORM-coupled focal methods, generation gets a Django-aware prompt (use real ORM/models,
no mocks) and validation adds a `conftest.py` that configures Django + a migrated in-memory test DB via
pytest-django (DB access auto-enabled for every test). Model: **gpt-4o-mini** (ChatUniTest's model class).
A sixth regime, **shuffle**, was added: random test order + random `PYTHONHASHSEED` each run.

Sample: **20 Django instances, 273 test files, 895 test functions**, each run 10x in six regimes
(baseline, cpu, io, memory, shuffle).

**Result: 75 flaky functions / 895 (~8.4%); 30 flaky files / 273 (~11%).**

- **All flakiness is in the `shuffle` regime.** baseline/cpu/io/memory verdicts are stable; tests flip
  only when order + hash seed are randomized. So Django flakiness here is **order-dependence /
  nondeterminism, not resource stress** — consistent with sympy (cpu/io/mem = 0 flaky everywhere).
- **Mechanism (verified in the test source):** the generated tests are **not isolated** — they reuse
  fixture identities (`User.objects.create(username='testuser')`, `'testuser1'`, … across independent
  samples) and omit `@pytest.mark.django_db`. Run together, duplicate rows collide (`UNIQUE constraint`)
  depending on order, so a test passes or fails based on what ran before it — the classic **victim/
  polluter order-dependent flakiness** (the category iPFlakies targets).
- **Confirmed by isolation:** running a flaky file alone, 5x with shuffled order, gives the *same*
  verdicts every time (stable). It is only flaky *in a suite* → the flakiness is order-dependent, not
  intrinsic.

## Takeaways / next steps

- **Resource stress (cpu/io/memory) causes ~0 flakiness** in generated unit tests, across both sympy
  (1,200 fns) and Django (895 fns). Deterministic code does not flake under load.
- **Order/hash randomization (`shuffle`) is the lever that finds flakiness** — ~8.4% of Django generated
  tests flake, almost entirely **order-dependent** (shared-state / test-isolation failures).
- Next: run all 211 Django instances for the dataset-wide rate; add an **isolation mode** to separate
  intrinsic vs order-dependent flakiness as two numbers; scale generation to full gpt-5 once the funded
  key is available.
