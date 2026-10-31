# Resource-stress flakiness check — LLM-generated tests (Java/Maven/JUnit)

Stress-testing LLM-generated unit tests to see whether **CPU / memory pressure** induces flakiness.
This is the **resource-stress** dimension of the flakiness study: separate from, and complementary to,
the order-dependence / pollution analysis. The question here is narrow and specific: *when the machine is
under heavy CPU and memory load, do any of these generated tests start passing-and-failing non-deterministically?*

## What was run
Each test method is run on its own, in a fresh JVM, **10× per regime**, and flagged **flaky** for a
regime if it both **passes and fails** in that regime (`passed > 0 AND failed > 0`).

Regimes (**I/O excluded** per the mentor):
| Regime | Load applied | stress-ng command |
|---|---|---|
| `cpu` | all logical cores busy | `stress-ng --cpu <N_CPUS>` |
| `memory` | 2 VM workers, 256 MB each | `stress-ng --vm 2 --vm-bytes 256M` |
| `baseline` | none (control) | — |

**Two-phase design (to save time):** `cpu` + `memory` are run first; **`baseline` is run only for the
methods that fail or flake under stress** (a method that passes cleanly under stress needs no control).
Exception: the non-flaky 198-method set was run with full `baseline,cpu,memory` before this optimization
was adopted, so it already has baseline for every method. Because **no method has failed or flaked under
stress so far**, the phase-2 baseline pass has been a no-op (nothing to control-check).

## Test sets and results
| Set | Files | Methods | Input CSV | Result CSV | Stress-flaky |
|---|---|---|---|---|---|
| Non-flaky (main + hadoop) | 104 | **198** (175 main + 23 hadoop) | `input/tests.csv` | `stress_nonflaky.csv` | **0** |
| Flaky | 23 | **48** | `input/flaky_generated_tests.csv` | `stress_flaky.csv` | **0** |
| Variant: agent_A_13 | 13 | **37** | `input/agent_A_13.csv` | `stress_agent_A_13.csv` | **0** |
| Variant: agent_F_11 | 11 | **38** | `input/agent_F_11.csv` | `stress_agent_F_11.csv` | **0** |
| Variant: prompt_default_8 | 8 | **23** | `input/prompt_default_8.csv` | `stress_prompt_default_8.csv` | **0** |
| Variant: prompt_cleanup_12 | 12 | **25** | `input/prompt_cleanup_12.csv` | `stress_prompt_cleanup_12.csv` | **0** |
| **TOTAL (done)** | | **369** | | | **0** |

**Headline result: 0 / 369 methods are flaky under CPU or memory stress.**

The **main non-flaky set (94 files / 175 methods)** is identical to `main_nonflaky_side_94`; hadoop
(10 files / 23 methods) is separate. 94 + 10 = 104 files; 175 + 23 = 198 methods. The **flaky 48-method set**
is byte-identical (sha256) to `main_flaky_side_23`.

### Pending / excluded
- **FC_FCV** (agent_FC_12 + agent_FCV_9 = **58 methods**, from `more_flaky_check_tests.zip`): ready to run
  (full `tests.csv`, same schema as the variants above), stressed with the same cpu+memory harness. Not yet run.
- **new10** (6 folders, ~128 methods, `flaky_checked_tests_new10/`): **excluded.** Per the mentor these tests
  "don't pass by themselves," and technically the folders ship only a thin `tests_info.csv` (no `file_here` /
  placement path / `mockito_fix`), so the harness cannot place them without reconstruction. The batch also
  contains every row in `BROKEN_DO_NOT_RUN.csv` (compile errors / NPE / wrong-length). Not run.

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
- **`scripts/run_variants_stress.sh`** — driver for the 4 generation-variant folders (agent_A_13, agent_F_11,
  prompt_default_8, prompt_cleanup_12) from `flaky_checked_tests.zip`: extracts the zip, places each test file
  at the path the harness expects (via each folder's `tests.csv`), and runs all four **cpu+memory only**,
  one split CSV per folder.
- **`scripts/run_fcfcv_stress.sh`** — same driver for the FC_FCV folders (agent_FC_12 + agent_FCV_9) from
  `more_flaky_check_tests.zip`. cpu+memory only, split CSV per folder. (Run pending.)

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

# FC_FCV (cpu+memory only, split per folder) — pending
bash scripts/run_fcfcv_stress.sh
```
Phase-2 baseline (only the stressed failures): re-run `stress_check.py` with `--regimes baseline` and one
`--only <id>` per method whose stress result had `passed==0 & fail>0` (all-failed) or `passed>0 & fail>0` (flaky).
To date no method has failed or flaked under stress, so this pass has been a no-op.

## Result and interpretation
- **0 / 369 methods stress-flaky** across baseline (where run), cpu, and memory. CPU and memory pressure do
  **not** induce flakiness in these tests.
- This is the expected outcome: the tests are **single-threaded, mocked, and deterministic**, so resource
  pressure only makes them *slower*, not *non-deterministic*. There is no race, real clock, or real I/O for
  stress to perturb.
- Consistent with the mentor's finding that generated tests are **not flaky in isolation** — the flakiness in
  this corpus is **order-dependent pollution** (unrestored static state via reflection, missing `@After`),
  an entirely different axis from resource stress. Resource stress being a clean negative is the contrast
  against which the order-dependence / cleanup-prompt result is reported.
- Runs = 10 per regime. More runs would tighten confidence in the zero but are not expected to surface flaky
  tests, since these tests have no low-probability non-determinism for extra runs to catch.
