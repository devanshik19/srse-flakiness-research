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

Each instance's files were run as a **suite** 10× in **6 regimes**. The earlier combined `shuffle`
regime was split into two one-variable regimes — **hashseed** (random seed, fixed order) and **order**
(random order) — so order-dependence and hash-ordering can be reported separately:

| regime | test order | `PYTHONHASHSEED` | stress | isolates |
|---|---|---|---|---|
| baseline | fixed | fixed | none | intrinsic non-determinism |
| cpu / io / memory | fixed | fixed | stress-ng | timing / race under load |
| hashseed | fixed | random | none | hash-ordering dependence |
| order | random | fixed | none | order-dependence / isolation |

| project | validated instances | test files in those instances | files that ran | test functions | flaky functions | flaky files |
|---|---|---|---|---|---|---|
| **sympy** | 5 (all) | 200 | **196** | **1,200** | **0** | **0** |
| **django** | **20 (sample)** | 310 | **273** | **895** | **75 (8.4%)** | **30 (11%)** |

- django was validated on a **20-instance sample only**, not all 211 (each instance pulls a ~1 GB image;
  full sweep pending). sympy was validated fully.
- "files that ran" < "generated" because broken generations fail at collection (no import).

## Django flakiness by regime

Counts overlap (a function can flip in more than one regime), so columns sum to more than the unique total.
The earlier combined `shuffle` row is split here into **order** and **hashseed**; all other counts are
unchanged from the original run.

| regime | flaky functions | flaky files |
|---|---|---|
| **order** (random order) | **69** | **27** |
| **hashseed** (random `PYTHONHASHSEED`) | **2** | **1** |
| baseline (fixed order, no stress) | 8 | 4 |
| cpu stress | 2 | 1 |
| io stress | 2 | 1 |
| memory stress | 0 | 0 |
| **unique total** | **75** | **30** |

Full per-test list, each linked to its test body:
[django_flaky.md](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/django_flaky.md)

## What the numbers mean

- **Flakiness is overwhelmingly order-dependent.** 69/75 flaky functions (27/30 files) flip when test
  *order* is randomized: **victim/polluter isolation failures** — the generated tests reuse DB
  identities like `username='testuser'` and omit `@pytest.mark.django_db`, so rows collide depending on
  what ran before. Confirmed: a flaky file run **in isolation** is stable.
- **Hash-ordering (`hashseed`) is a thin slice** — only 2 functions / 1 file flip under a random
  `PYTHONHASHSEED`, and they also flip under `order`. Splitting the old `shuffle` regime shows almost
  all of its signal was order, not hash seed.
- **Small stress / baseline tails** — a handful of functions flip under cpu/io or in baseline; the
  baseline ones include the `django-11141 test_load_disk` cases that toggle ERROR↔FAILED (a broken
  test's nondeterministic failure *type* rather than a pass↔fail flake).
- **Resource stress is not a major driver** — consistent with sympy (1,200 fns, 0 flaky under any
  stress). Deterministic code does not flake under load.

## Proof / artifacts

- Focal method list: [swebench_focal.csv](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/swebench_focal.csv)
- Django per-test flaky list + bodies: [django_flaky.md](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/django_flaky.md)
- Raw django verdict log (every test × run): [gen_django/docker_results.csv](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/gen_django/docker_results.csv)
- Method writeup: [findings.md](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/findings.md)
- Generator / validator: [phase1_focal.py](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/phase1_focal.py), [docker_validate.sh](https://github.com/devanshik19/srse-flakiness-research/blob/main/swebench_llmgen/docker_validate.sh)
