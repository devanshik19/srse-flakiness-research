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

## Two regimes

The results fall into two groups that must be read differently:

1. **Clean regime** — `--all 1/2/4` (and cpu at 6): genuine flakiness. A moderate load perturbs
   timing/ordering enough to expose real races, but the suite still runs normally.
2. **Starvation regime** — `pipe` and `interrupt` at `--all 6`: the box is so oversubscribed that
   timing tests **time out en masse**. The failure counts are inflated by load-induced timeouts, not
   genuine flakiness, and should be read with caution.

## Per-configuration results

| config | runs failed / 15 | distinct tests |
|---|---|---|
| pipe `--all 6` | 15/15 | 31 (starvation) |
| cpu `--all 1` | 13/15 * | 12 |
| interrupt `--all 1` | 12/15 | 9 |
| os `--all 1` | 11/15 | 8 |
| pipe `--all 1` | 9/15 | 3 |
| io `--all 1` | 7/15 | 3 |
| device `--all 1` | 6/15 | 2 |
| interrupt `--all 6` | 4/15 | 44 (starvation) |
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

The jump from 21 to 59 comes almost entirely from the two `--all 6` starvation configs
(`interrupt-6` = 44, `pipe-6` = 31). The extra ~38 tests are load-induced timeouts —
`parent_command_goto[...]`, `node_timeout`, `idle_timeout`, `entrypoint_timeout`, and similar — not
genuine flakiness. The clean-regime figure of 21 is the reportable count.

## Observations

- **CPU contention at `--all 1` is the strongest clean trigger** (13/15 runs, 12 distinct tests).
- **Dose-response is non-monotonic:** cpu `--all 1` (12 distinct) is far flakier than cpu `--all 6`
  (4 distinct). Mild contention adds timing jitter that trips tight thresholds; heavy load slows
  everything roughly uniformly and, past a point, only causes starvation timeouts.
- **OS/syscall, interrupt, and pipe stress at `--all 1` are also strong triggers** (8–9 distinct),
  not just CPU.
- **Memory (bounded) and security cause essentially no flakiness.**

## Infeasible on this box (deferred to the cluster)

- **filesystem** (any intensity) — even `--all 1` drives load to ~130 and the suite makes no progress.
- **vm** (any intensity) — OOM-kills the ~1 GB-free box.
- **`--all 0` and `--all 8`** — one instance per core / eight per stressor saturate all 8 cores; the
  suite is starved (cpu-8 took 10 h to reach 28 % of one run). Failures there are timeouts, not
  flakiness.
