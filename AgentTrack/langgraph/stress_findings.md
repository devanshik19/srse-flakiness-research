# LangGraph stress-test findings (Shaker-style)

Goal: find tests that pass at rest but fail under **resource stress** — run the suite while
`stress-ng` loads CPU / memory / IO / device, and see what breaks.

- Subject: `langchain-ai/langgraph`, `libs/langgraph` (Pregel engine), v1.2.11, commit `e539ac1`.
- Box: AMD Ryzen 3 7320U (8 cores, ~3.5 GB RAM), WSL Ubuntu, Python 3.13, `NO_DOCKER=true`.
- Method: for each config, start `stress-ng <config>` in the background, then run the **whole
  ~2003-test suite 15 times** and count failing tests per run. ("N=15" = 15 full-suite runs per
  config; 4 configs = 60 suite runs ≈ 120k test executions.)
- Configs (`--all 1`; memory bounded so it doesn't OOM this ~1 GB-free box):
  `io`=`--class io --all 1`, `device`=`--class device --all 1`, `cpu`=`--class cpu --all 1` (~85
  CPU stressors), `memory`=`--vm 2 --vm-bytes 256M`.
- **Baseline (no stress) = 0 failures** across 6 prior clean whole-suite runs (baseline + 5 shuffles).

## Results

| stress config | runs with ≥1 failure / 15 | total test-failures | distinct tests failed |
|---|---|---|---|
| io | 2 | 2 | 1 |
| device | 2 | 2 | 2 |
| **cpu** | **12** | **19** | **7** |
| memory (bounded) | 2 | 2 | 1 |

Union across all configs: **8 distinct tests**. **CPU contention is by far the strongest trigger**
(~80% of runs, 7 distinct tests). io and memory only ever break the **same single test** — the
concurrency race `test_error_handler_resumes_after_crash_multiple_nodes` — which even light stress
triggers; cpu additionally trips the 6 streaming/ordering tests. All failing tests are **idle-clean**
— they only fail under load.

## Failing tests (all in the Pregel engine) — three buckets

**1. Genuine concurrency race** (also flaky *idle* at ~12% in the ND phase; load-amplified):
- `tests/test_retry.py::test_error_handler_resumes_after_crash_multiple_nodes`
  — `assert 0 == 1` (`test_retry.py:2809`): when two nodes fail in one superstep and `handler_a`
  crashes, the engine sometimes tears down before `handler_b` runs. **cpu: 11/15 runs;** also seen
  under io/device/memory. This is the single most load-sensitive test.

**2. Timing-value assertions** (assert exact timestamps/durations of streamed events → break under load):
- `tests/test_pregel.py::test_stream_buffering_single_node[sqlite]`, `[sqlite_aes]`
  — `(0.2, 'Before sleep') != (0.0, 'Before sleep')`: event expected at t=0.0, a choked CPU delayed it.
- `tests/test_pregel.py::test_sync_streaming_with_functional_api`
  — `assert 0.0386 > (0.05*0.8)`: a hard timing threshold the load pushed under.

**3. Ordering assertions** (assert exact order/interleaving of concurrent outputs → break under load):
- `tests/test_pregel_async.py::test_imp_nested[memory-async]`, `[sqlite_aio-sync]`
  — `{'submapper': '1'} != {'mapper': '00'}`
- `tests/test_pregel.py::test_stream_subgraphs_during_execution[memory]`
  — `{'retriever_two': …} != {'analyzer_one': …}`
- `tests/test_pregel.py::test_in_one_fan_out_state_graph_waiting_edge[sqlite_aes]`

## Interpretation
- **Bucket 1 = a real product race** (fails even with no stress).
- **Buckets 2–3 = test fragility**: the tests over-specify wall-clock timing / concurrent ordering
  that the engine doesn't guarantee under CPU contention. Correct at rest, flaky under load.
- Idle-clean, load-flaky → exactly the resource-stress (Shaker) signal.

## Scope — whole-repo stress
Stressed **5 of 7 packages** under all four configs (15 runs each): langgraph, checkpoint,
checkpoint-sqlite, checkpoint-conformance, prebuilt. **Only `langgraph` produced any failures** —
the other four were **0** across cpu/io/device/memory (as expected: serialization / storage /
parsing logic, nothing timing- or concurrency-sensitive to perturb). `cli` (partial, 1 run) and
`sdk-py` weren't finished — the machine died mid-run — but both are logic/SDK (mocked) and expected
clean.

Failing tests are entirely in the Pregel engine; total failure instances across all four configs:
`test_error_handler_resumes_after_crash_multiple_nodes` ×16, `test_stream_buffering_single_node`
[sqlite] ×2 / [sqlite_aes] ×1, `test_imp_nested` [memory-async] ×2 / [sqlite_aio-sync] ×1,
`test_sync_streaming_with_functional_api` ×1, `test_stream_subgraphs_during_execution[memory]` ×1,
`test_in_one_fan_out_state_graph_waiting_edge[sqlite_aes]` ×1.

## Raw results (`stress_summary.csv` — `label,config,run,exit_code,failed,skipped`)
```
io-1,"--class io --all 1": failed on runs 3, 6
device-1,"--class device --all 1": failed on runs 6, 10
cpu-1,"--class cpu --all 1": failed on runs 1,4,5,6,7,8,9,10,11,12,13,14 (2 tests on 6,7,9,11,12,13,14)
memory-1,"--vm 2 --vm-bytes 256M": failed on runs 8, 14
```
Full per-run rows: `stress_results/langgraph/stress_summary.csv`; per-run failing tests:
`<config>-failures.txt`; full pytest output: `<config>-run-<i>.log`.
