# scripts — LangGraph flaky-test (ND) pipeline

## Setup

1. Install `uv` (manages Python + the venv):
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Clone the target repo and build its test env. For LangGraph:
   ```
   git clone --depth 1 https://github.com/langchain-ai/langgraph
   cd langgraph/libs/langgraph
   uv sync --frozen --no-dev --group test --python 3.13
   uv pip install pytest-randomly pytest-rerunfailures
   ```
   (Python is pinned to 3.13 — the repo doesn't support 3.14 yet.)
3. For the stress run only, install stress-ng:
   ```
   sudo apt-get install -y stress-ng
   ```
   Always run with `NO_DOCKER=true` in front

## The files

- `prioritize.py` - orders the test list so the likely-flaky tests (async, streaming, checkpoint, retry) run first
- `nd_check.sh` - ND check for ONE test id
- `run_nd_batch.sh` - runs `nd_check.sh` over a whole list of tests; resumable

Paths below assume the LangGraph clone is at `~/langgraph/libs/langgraph` and results go under
`~/srse-research/AgentTrack/langgraph/`.

## 1. ND check

Collect the test list, order it, then run each test 50 times (any test that fails even once is automatically re-run 200 times to measure how often):

```
cd ~/langgraph/libs/langgraph
NO_DOCKER=true uv run --no-sync pytest --co -q -p no:randomly | grep '::' > ~/srse-research/AgentTrack/langgraph/tests_all.txt
cd ~/srse-research/AgentTrack
python3 scripts/prioritize.py langgraph/tests_all.txt langgraph/tests_queue.txt
scripts/run_nd_batch.sh ~/langgraph/libs/langgraph langgraph/tests_queue.txt langgraph/nd_results 50 200
```

- Results:
  - `nd_summary.csv` — one row per test: `test_id,pass,fail,missing,total,verdict`
  - `nd_perrun.csv` — every single run
  - a test is flaky if its verdict is `FLAKY_ND`
