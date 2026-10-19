# SWE-bench LLM-Generated Test Flakiness — Results Summary

Single source of truth for all counts. Generated with ChatUniTest-style prompts on SWE-bench Verified
focal methods, run many times under perturbation regimes in per-instance Docker images, flakiness
detected as verdict changes across runs.

## Terminology (so every number is unambiguous)

| term | meaning |
|---|---|
| **instance** | one SWE-bench bug (a repo at a specific commit), e.g. `django__django-11087` |
| **focal method** | the function a bug fix touched — the generation target. One instance can have several. |
| **test file** | one generated file `test_<method>__<k>.py`; **10 generated per focal method** (10 samples) |
| **test function** | a `def test_...` inside a file; a file usually holds several. **Flakiness is measured here.** |

## Focal methods (generation targets)

**923 focal methods total** (909 with a resolved function name), extracted from the gold patches of all
500 SWE-bench Verified instances. Source: [swebench_focal.csv](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/swebench_focal.csv)

| repo | focal methods | repo | focal methods |
|---|---|---|---|
| django | 384 | astropy | 39 |
| sympy | 185 | pylint | 25 |
| sphinx | 80 | requests | 9 |
| scikit-learn | 61 | seaborn | 4 |
| matplotlib | 55 | flask | 1 |
| pytest | 41 | xarray | 39 |

## Generated so far

| project | model | focal methods (total) | methods generated | instances | test files generated |
|---|---|---|---|---|---|
| **sympy** | gpt-5-mini | 185 | **20** | 5 | **200** |
| **django** | gpt-4o-mini | 384 | **308** | 211 | **3,080** |

- sympy: only 20/185 methods (pipeline proof); django: 308/384 (the other 76 focal rows are blank
  functions or target a *class*, which the extractor skips).
- Models here are pilots; the full 909-method dataset is planned on **gpt-5** (pending the funded key).

## Validated so far

Each instance's files were run as a **suite** 10× in **5 regimes** (baseline; cpu/io/memory stress;
shuffle = random test order + random `PYTHONHASHSEED`).

| project | validated instances | test files in those instances | files that ran | test functions | flaky functions | flaky files |
|---|---|---|---|---|---|---|
| **sympy** | 5 (all) | 200 | **196** | **1,200** | **0** | **0** |
| **django** | **20 (sample)** | 310 | **273** | **895** | **75 (8.4%)** | **30 (11%)** |

- django was validated on a **20-instance sample only**, not all 211 (each instance pulls a ~1 GB image;
  full sweep pending). sympy was validated fully.
- "files that ran" < "generated" because broken generations fail at collection (no import).

## Django flakiness by regime

Counts overlap (a function can flip in more than one regime), so columns sum to more than the unique total.

| regime | flaky functions | flaky files |
|---|---|---|
| **shuffle** (random order + hash seed) | **69** | **27** |
| baseline (fixed order, no stress) | 8 | 4 |
| cpu stress | 2 | 1 |
| io stress | 2 | 1 |
| memory stress | 0 | 0 |
| **unique total** | **75** | **30** |

Full per-test list, each linked to its test body:
[django_flaky.md](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/django_flaky.md)

## What the numbers mean

- **Resource stress (cpu/io/memory) ≈ 0 flakiness** — on both sympy (1,200 fns) and django (895 fns).
  Deterministic code doesn't flake under load.
- **Flakiness is order/nondeterminism, found by `shuffle`** — ~92% of django's flaky functions (69/75)
  flip only when test order + hash seed are randomized: **order-dependent flakiness** from inadequate
  test isolation (generated tests reuse DB identities like `username='testuser'` and collide by order).
  Confirmed: a flaky file run **in isolation** is stable → order-dependent, not intrinsic.
- **A smaller intrinsic-ND tail** — the 8 baseline flaky functions flip in *fixed* order, so they are not
  order-caused; they come from Python's random `PYTHONHASHSEED`. Confirmed: fixing the seed
  (`PYTHONHASHSEED=0`) makes them deterministic. (Caveat: some of these flip ERROR↔FAILED — a
  nondeterministic *failure type* of a broken test, not a pass↔fail flake.)

## Proof / artifacts

- Focal method list: [swebench_focal.csv](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/swebench_focal.csv)
- Django per-test flaky list + bodies: [django_flaky.md](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/django_flaky.md)
- Raw django verdict log (every test × run): [gen_django/docker_results.csv](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/gen_django/docker_results.csv)
- Method writeup: [findings.md](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/findings.md)
- Generator / validator: [phase1_focal.py](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/phase1_focal.py), [docker_validate.sh](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/docker_validate.sh)
