# Agent-frameworks ND-flakiness pipeline 
 
Instead of generating a test and checking whether the GENERATED test is flaky, take an agent framework's OWN developer test suite and check whether any existing test is non-deterministic. Same ND definition as agentflake-nonflaky/04_check_nd.sh, ported from Maven/surefire to pytest. <br>

Subjects: LangGraph, AutoGen, CrewAI, Codex.

## Pipeline per subject
1. Clone the project, build a test env with uv. Run everything with NO_DOCKER=true to gate off Postgres/Redis-backed tests.
2. Collect every test id: pytest --co -q -p no:randomly | grep '::' > tests_all.txt.
3. Prioritize into a queue (prioritize.py): score node ids by keyword -- async/concurrency/streaming/checkpoint/
   retry high, pure logic low -- so suspects run first and any flake surfaces early in a long sweep.
4. ND-check each test (nd_check.sh, driven by run_nd_batch.sh): run it ALONE, fresh process, same order
   (-p no:randomly, PYTHONHASHSEED=0), N=50; promote any flinch to N=200. Any fail/miss -> FLAKY_ND.


## Scripts
prioritize.py, nd_check.sh, run_nd_batch.sh.

## Result columns
- nd_summary.csv: test_id, pass, fail, missing, total, verdict (NOT_FLAKY / FLAKY_ND).
- nd_perrun.csv: test_id, run, result (pass/fail/missing) -- every individual run.

## Reconstruct the full run log
awk -F, 'NR>1{printf ">>> [%d/%d] %s -> %s\n", NR-1, <total>, $1, $6}' nd_summary.csv > nd_run_full.log
