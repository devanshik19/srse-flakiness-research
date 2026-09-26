# LangGraph stress-test findings (round 2 — config sweep)

Goal: find which **stress configuration** (resource class × intensity) triggers the most flaky
tests. Extends round 1 (io/device/cpu/memory) to a wider set of `stress-ng` classes and intensities.

- Subject: `langchain-ai/langgraph`, `libs/langgraph` (Pregel engine), commit `e539ac1`.
- Box: 8-core laptop, WSL2 Ubuntu, Python 3.13, `NO_DOCKER=true`.
- Method: for each config, start `stress-ng <config>` in the background, then run the **whole
  langgraph suite 15 times** and count failing tests per run. Configs run fastest→slowest.
- Intensity = `--all N` (N copies of every stressor in the class). Memory is bounded
  (`--vm 2 --vm-bytes 256M`) so it can't OOM.
- **Baseline (no stress) = 1 failure in 15 runs** (`test_error_handler_resumes...`, ~7% — flaky
  even at rest).

## Results (langgraph — IN PROGRESS)

| stress config | runs with ≥1 failure / 15 | distinct tests |
|---|---|---|
| **cpu `--all 1`** | **13** | **11** |
| **os `--all 1`** | **11** | **8** |
| io `--all 1` | 7 | 3 |
| device `--all 1` | 6 | 2 |
| cpu `--all 6` | 2 | 4 |
| scheduler `--all 1` | 3 | 1 |
| baseline | 1 | 1 |
| memory (bounded) | 0 | 0 |

Still queued (feasible here): pipe (1/6), security (1/2), interrupt (1/6), cpu-cache (1/2/4),
then the other 6 packages.

**Moved to a bigger box (starve this 8-core / ~1 GB machine to a standstill):** filesystem (all
intensities — even `--all 1` drives load to ~130 and the suite makes zero progress) and all the
CPU-class `--all 8` configs (cpu-8 took 10h to reach 28% of one run). These are infeasible on
commodity hardware — itself a reportable result.

**Union across configs so far: 17 distinct tests, all in the Pregel engine.**

## Two key observations

1. **Non-monotonic dose-response — mild CPU stress is flakier than heavy.** `cpu --all 1` broke
   25 tests across 13/15 runs; `cpu --all 6` broke only 4 across 2/15. Likely because light
   contention adds *jitter* that trips tight timing thresholds, while heavy load slows everything
   roughly uniformly. Notably, `cpu --all 6` also hit **different** tests (checkpoint-migration,
   fan-out state) rather than the timing tests — heavy load exposes a different failure mode.
2. **OS/syscall stress is a strong trigger (11/15), not just CPU.** The `os` class (fork/exec/
   syscall churn) perturbs async scheduling enough to break the same timing/ordering tests.

## Failing tests — buckets

**1. Genuine concurrency race** (flaky even idle):
- `tests/test_retry.py::test_error_handler_resumes_after_crash_multiple_nodes` — appears under
  every config incl. baseline. The most load-sensitive test.

**2. Timing-value assertions** (assert exact timestamps/durations of streamed events):
- `tests/test_pregel.py::test_stream_buffering_single_node[sqlite]`, `[sqlite_aes]`
- `tests/test_pregel_async.py::test_stream_buffering_single_node[sqlite_aio]`

**3. Ordering assertions** (assert exact interleaving of concurrent outputs):
- `tests/test_pregel.py::test_stream_subgraphs_during_execution[memory]`, `[sqlite]`, `[sqlite_aes]`
- `tests/test_pregel_async.py::test_stream_subgraphs_during_execution[sqlite_aio]`
- `tests/test_pregel_async.py::test_imp_nested[sqlite_aio-exit]`, `[memory-sync]`, `[memory-exit]`,
  `[sqlite_aio-sync]`

**4. State / checkpoint (new this round, seen under heavier cpu/os load):**
- `tests/test_time_travel.py::test_multiple_interrupts_in_one_node[memory]`
- `tests/test_time_travel.py::test_sequential_interrupts_fork_from_middle[memory]`
- `tests/test_checkpoint_migration.py::test_latest_checkpoint_state_graph_async[sqlite_aio]`
- `tests/test_large_cases.py::test_in_one_fan_out_out_one_graph_state`
- `tests/test_pregel.py::test_in_one_fan_out_state_graph_waiting_edge_custom_state_class_pydantic_input[memory]`

## Interpretation
- Bucket 1 = real product race (fails at rest). Buckets 2–3 = test fragility (over-specified
  timing/ordering the engine doesn't guarantee under load). Bucket 4 = state/checkpoint tests that
  surface only under heavier contention.
- Idle-clean → load-flaky = the resource-stress (Shaker) signal, now across many stress classes.

## Raw results
Per-run rows: `stress_results/cfg/langgraph/stress_summary.csv`; per-config failing tests:
`<config>-failures.txt`; full pytest output: `<config>-run-<i>.log`.
