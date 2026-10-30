# Resource-stress flakiness check — LLM-generated tests (Java/Maven/JUnit)

Stress-testing LLM-generated unit tests to see whether **CPU / memory pressure** induces flakiness,
the Java/Maven analogue of the SWE-bench Django stress study. Mirrors the mentor's pipeline
(generate tests → detect flakiness: ND / ID / OD / NOD / TD); this folder covers the **resource-stress**
dimension only.

## What was run
Each test method is run on its own, in a fresh JVM, **10× per regime**, and flagged **flaky** for a
regime if it both **passes and fails** in that regime (`passed > 0 AND failed > 0`).

Regimes (per the mentor, **I/O excluded**):
| Regime | Load applied | stress-ng command |
|---|---|---|
| `cpu` | all logical cores busy | `stress-ng --cpu <N_CPUS>` |
| `memory` | 2 VM workers, 256 MB each | `stress-ng --vm 2 --vm-bytes 256M` |
| `baseline` | none (control) | — |

**Two-phase design (to save time):** `cpu` + `memory` are run first; **`baseline` is run only for the
methods that fail or flake under stress** (a method that passes cleanly under stress needs no control).
Exception: the non-flaky 198-method set was run with full `baseline,cpu,memory` before this optimization
was adopted, so it already has baseline for every method.

## Test sets
| Set | Files | Methods | Input CSV | Result |
|---|---|---|---|---|
| Non-flaky (main + hadoop) | 104 | **198** (175 main + 23 hadoop) | `input/tests.csv` | `stress_nonflaky.csv` — **0 stress-flaky** |
| Flaky | 23 | **48** | `input/flaky_generated_tests.csv` | `stress_flaky.csv` |
| Variant: agent_A | 13 | 37 | (bundled in flaky_checked_tests.zip) | `stress_agent_A_13.csv` |
| Variant: agent_F | 11 | 38 | — | `stress_agent_F_11.csv` |
| Variant: prompt_default | 8 | 23 | — | `stress_prompt_default_8.csv` |
| Variant: prompt_cleanup | 12 | 25 | — | `stress_prompt_cleanup_12.csv` |

The **main non-flaky set (94 files / 175 methods)** is identical to `main_nonflaky_side_94` in
`flaky_checked_tests.zip`; hadoop (10 files / 23 methods) is separate. 94+10 = 104 files; 175+23 = 198 methods.

## Environment (exact — captured 2026-10-31)
- **Host:** `dev4nshi@LAPTOP-VME6MC5I` (HP laptop), Windows 11 Home Single Language, running under **WSL2 Ubuntu**.
- **CPU:** **AMD Ryzen 3 7320U with Radeon Graphics** — 4 cores / 2 threads per core = **8 logical processors** (the `cpu` regime runs `stress-ng --cpu 8`).
- **RAM:** **3.8 GiB total** (~4 GB). The `memory` regime applies `--vm 2 --vm-bytes 256M` = ~512 MB of managed pressure.
- **stress-ng:** **0.20.01** (gcc 15.2.0, x86_64).
- **JDK (build + run for these sets):** **OpenJDK 1.8.0_504** (8u504, build 25.504-b01), `/usr/lib/jvm/java-8-openjdk-amd64`, selected per-test by the harness. Note: the **shell default `java` is 17.0.20.1** and Maven's default Java is 17, so builds override `JAVA_HOME` to JDK 8.
- **Maven:** **Apache Maven 3.9.12** (`/usr/share/maven`).
- **WSL kernel:** `6.18.33.2-microsoft-standard-WSL2` (x86_64).
- **Dependencies:** offline, from each project archive's bundled `.m2` repository (`--archive-dir extracted`).

## Harness
- **`scripts/stress_check.py`** — the stress runner. Reuses the flaky-check package's `rerun` check
  (per-method, fresh JVM, "passes AND fails" = flaky) run **under an active stress-ng load**, once per
  regime. Does **not** modify the package. Writes `<out>/stress_results.csv` with per-method pass/fail/runs
  and a flaky flag per regime. Resumable: re-running continues per method from the last recorded run.
- **`scripts/run_variants_stress.sh`** — driver for the 4 generation-variant folders (agent_A/F,
  prompt_default/cleanup) from `flaky_checked_tests.zip`: extracts the zip, places each test file at the
  path the harness expects, and runs all four **cpu+memory only**, one split CSV per folder.

## Reproduce
```bash
cd ~/flakecheck/flaky_check_package

# non-flaky (full baseline+cpu+memory, already done)
python3 scripts/stress_check.py --tests task_csvs/tests.csv \
  --archive-dir extracted --regimes baseline,cpu,memory --runs 10 \
  --out flaky_check_out/stress_nonflaky

# flaky (two-phase: cpu+memory first)
python3 scripts/stress_check.py --tests task_csvs/flaky_generated_tests.csv \
  --archive-dir extracted --regimes cpu,memory --runs 10 \
  --out flaky_check_out/stress_flaky

# variants (cpu+memory only, split per folder)
bash scripts/run_variants_stress.sh
```
Phase-2 baseline (only the stressed failures): re-run `stress_check.py` with `--regimes baseline` and one
`--only <id>` per method whose stress result had `passed==0 & fail>0` (all-failed) or `passed>0 & fail>0` (flaky).

## Result so far
- **Non-flaky (198 methods): 0 stress-flaky** in baseline, cpu, and memory — CPU/memory pressure does not
  induce flakiness in these tests. Consistent with the Django stress study and the mentor's finding that
  generated tests are not flaky in isolation (flakiness is order-dependent pollution).
- Flaky (48) and the 4 variant folders: in progress.
