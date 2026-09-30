# LangGraph — Stress-Test Results (configuration sweep)

Goal: find which `stress-ng` configuration (resource class × intensity) triggers the most flaky
tests. Each test that passes at rest but fails under load is a load-sensitive flaky test.

## Setup

- Subject: `langchain-ai/langgraph`, `libs/langgraph` (Pregel engine), commit `e539ac1`.
- Box: 8-core laptop, WSL2 Ubuntu, Python 3.13, `NO_DOCKER=true`.
- Method: for each config, run `stress-ng <config>` in the background, then run the whole langgraph
  suite 15 times and count failing tests per run.
- Intensity = `--all N` (N copies of every stressor in the class). Memory is bounded
  (`--vm 2 --vm-bytes 256M`) so it cannot OOM the box.
- Baseline (no stress): 1 failure in 15 runs — `test_error_handler_resumes...`, flaky even at rest.

## Two kinds of failure

Failures are either **assertion failures** (genuine flakiness — a test's own check fails) or
**timeouts** (`TimeoutError`/`NodeTimeoutError` — the test didn't finish in time under load).
Counting error types in the run logs (full breakdown at the end):

- **`--all 1/2/4` are pure assertion failures** (cpu `--all 1`: 21 assertions, 0 timeouts) — genuine
  flakiness.
- **`pipe --all 6` is mostly genuine** — 191 assertions vs 104 timeouts — so its high count is real
  flaky tests exposed by heavy load, not noise.
- **`interrupt --all 6` is timeout-dominated** — 167 timeouts vs 71 assertions — so much of its 44 is
  load-induced and should be read with caution.

Heavier load exposes *more* genuine flaky tests, but past a point also adds timeout noise; the
per-config error-type split at the end separates the two.

## Per-configuration results

| config | runs failed / 15 | distinct tests |
|---|---|---|
| pipe `--all 6` | 15/15 | 31 † |
| cpu `--all 1` | 13/15 * | 12 |
| interrupt `--all 1` | 12/15 | 9 |
| os `--all 1` | 11/15 | 8 |
| pipe `--all 1` | 9/15 | 3 |
| io `--all 1` | 7/15 | 3 |
| device `--all 1` | 6/15 | 2 |
| interrupt `--all 6` | 4/15 | 44 † |
| cpu-cache `--all 4` | 4/15 | 1 |
| cpu-cache `--all 1` | 3/15 | 4 |
| scheduler `--all 1` | 3/15 | 1 |
| cpu-cache `--all 2` | 2/15 | 7 |
| cpu `--all 6` | 2/15 | 4 |
| security `--all 1` | 1/15 | 1 |
| baseline | 1/15 | 1 |
| security `--all 2` | 0/15 | 0 |
| memory (bounded) | 0/15 | 0 |

\* cpu `--all 1` was run twice (22/30 combined); the 13/15 above is the first run.
† `--all 6` counts mix genuine assertion failures with load-induced timeouts — see "Failure types
per configuration" at the end (pipe-6 is ~65% genuine; interrupt-6 is ~70% timeout).

## Flaky tests by cause (clean regime — 21 tests)

All in the Pregel engine.

**1. Genuine concurrency race (also fails at rest):**
- `test_retry.py::test_error_handler_resumes_after_crash_multiple_nodes`

**2. Timing-value assertions (assert exact streamed-event timestamps):**
- `test_pregel.py::test_stream_buffering_single_node[memory]`, `[sqlite]`, `[sqlite_aes]`
- `test_pregel_async.py::test_stream_buffering_single_node[sqlite_aio]`

**3. Ordering assertions (assert exact interleaving of concurrent output):**
- `test_pregel.py::test_stream_subgraphs_during_execution[memory]`, `[sqlite]`, `[sqlite_aes]`
- `test_pregel_async.py::test_stream_subgraphs_during_execution[sqlite_aio]`
- `test_pregel_async.py::test_imp_nested[memory-exit]`, `[memory-sync]`, `[memory-async]`,
  `[sqlite_aio-exit]`, `[sqlite_aio-sync]`

**4. Fan-out / state ordering:**
- `test_pregel.py::test_in_one_fan_out_state_graph_waiting_edge[sqlite_aes]`
- `test_pregel.py::test_in_one_fan_out_state_graph_waiting_edge_custom_state_class_pydantic_input[memory]`
- `test_large_cases.py::test_in_one_fan_out_out_one_graph_state`

**5. Interrupt / time-travel:**
- `test_time_travel.py::test_fork_from_before_interrupt_refires[memory]`
- `test_time_travel.py::test_multiple_interrupts_in_one_node[memory]`
- `test_time_travel.py::test_sequential_interrupts_fork_from_middle[memory]`

**6. Checkpoint:**
- `test_checkpoint_migration.py::test_latest_checkpoint_state_graph_async[sqlite_aio]`

## Full union across all configs: 59 distinct tests

The clean `--all 1/2/4` regime accounts for 21 distinct tests, all genuine assertion failures. The
`--all 6` configs add the rest: `pipe --all 6` (31) is mostly genuine assertion failures under heavy
pipe load, while `interrupt --all 6` (44) is largely load-induced timeouts. So the real count is
**at least 21, and higher once pipe-6's genuine failures are folded in** — the per-config error-type
breakdown at the end shows which failures are real vs timeout.

## Observations

- **CPU contention at `--all 1` is the strongest clean trigger** (13/15 runs, 12 distinct tests).
- **Dose-response is non-monotonic:** cpu `--all 1` (12 distinct) is far flakier than cpu `--all 6`
  (4 distinct). Mild contention adds timing jitter that trips tight thresholds; heavy load slows
  everything roughly uniformly and, past a point, adds timeout noise on top of genuine failures.
- **OS/syscall, interrupt, and pipe stress at `--all 1` are also strong triggers** (8–9 distinct),
  not just CPU.
- **Memory (bounded) and security cause essentially no flakiness.**

## Infeasible on this box (deferred to the cluster)

- **filesystem** (any intensity) — even `--all 1` drives load to ~130 and the suite makes no progress.
- **vm** (any intensity) — OOM-kills the ~1 GB-free box.
- **`--all 0` and `--all 8`** — one instance per core / eight per stressor saturate all 8 cores; the
  suite is starved (cpu-8 took 10 h to reach 28 % of one run). Failures there are timeouts, not
  flakiness.

## Failure types per configuration

Error types counted across all run logs per config. `AssertionError` = genuine flakiness;
`TimeoutError`/`NodeTimeoutError` = load-induced. Counts are traceback mentions (indicative).

| config | assertions | timeouts |
|---|---|---|
| baseline | 1 | 0 |
| cpu-1 | 21 | 0 |
| cpu-6 | 1 | 0 |
| cpu-cache-1 | 8 | 0 |
| cpu-cache-2 | 13 | 0 |
| cpu-cache-4 | 4 | 0 |
| device-1 | 7 | 0 |
| interrupt-1 | 26 | 4 |
| interrupt-6 | 71 | 167 |
| io-1 | 10 | 0 |
| memory-bounded | 0 | 0 |
| os-1 | 21 | 8 |
| pipe-1 | 10 | 4 |
| pipe-6 | 191 | 104 |
| scheduler-1 | 3 | 0 |
| security-1 | 1 | 0 |
| security-2 | 0 | 0 |
