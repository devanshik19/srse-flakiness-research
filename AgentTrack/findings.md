# Agentic Framework Test-Suite Flakiness Findings

Non-determinism (ND) findings from running the **own developer test suites** of agentic frameworks under the ND
check.

## Method (shared)

**ND (non-deterministic) check:** run each test **alone, in a fresh process, in the same order**
(`-p no:randomly`, `PYTHONHASHSEED=0`), **N=50** times; any test that fails or goes missing even once is
promoted to **N=200** to characterize its rate. Any fail/miss => `FLAKY_ND`. Pytest port of `04_check_nd.sh`.
It isolates **self-contained** non-determinism only -- order-dependence (OD) and concurrency-under-load are
separate sweeps, deprioritized for this track.

## LangGraph

- **Subject:** `langchain-ai/langgraph`, `libs/langgraph` (Pregel engine), v1.2.11.
- **Coverage:** all **2003** collected tests, N=50 (flinches promoted to 200), suspect-ordered queue.
- **Result: 1 flaky / 2003.**

| Test | pass | fail | total | rate | verdict |
|---|---|---|---|---|---|
| `tests/test_retry.py::test_error_handler_resumes_after_crash_multiple_nodes` | 176 | 24 | 200 | ~12% | FLAKY_ND |

**Mechanism: concurrency race in multi-node error-handler scheduling.** Two nodes `a` and `b` run in the same superstep, each with an `error_handler`. `node_a` fails -> `handler_a` runs (sets an `Event`) -> `node_b`
unblocks and fails -> `handler_b` should run. ~12% of the time (load-sensitive) the failure is:
assert call_count["handler_b"] == 1
E assert 0 == 1 # handler_b never ran

i.e. when `handler_a` crashes, the engine sometimes tears the superstep down before `node_b`'s handler is
scheduled. Not the test's `wait(timeout=5)` (that succeeds). Leans **product race** in Pregel's error-handler
dispatch under concurrent multi-node failure; the test's docstring says both handlers should run, so it encodes
intended semantics. Evidence: `nd_results/retry_crash_fails/fail-{30,58,78}.log`.

- **Interpretation:** a mature, CI-hardened suite (explicit anti-ND measures like the `deterministic_uuids`
  fixture; LLM mocked via `FakeChatModel`) is essentially clean under ND-in-isolation, with one real concurrency  race in the error-handling path. 

## CrewAI
-

## AutoGen

-
## Codex
-
