# Docker recipe for import-failure SWE-bench instances (iPFlakies)

## Summary
SWE-bench's per-instance Docker images (Epoch AI registry) ship the correct Python +
prebuilt deps per instance, recovering instances that fail at import on the shared
3.10 venv (collections.Mapping etc.). iPFlakies runs inside the container.

## Validated recipes (4 working)
| Repo    | Python | Config for testpaths      | Plugin disables                 | Instances |
|---------|--------|---------------------------|---------------------------------|-----------|
| sympy   | 3.9    | none -> create pytest.ini | none                            | 30 |
| sphinx  | 3.9    | setup.cfg (testpaths=tests)| none                           | 29 |
| sklearn | 3.6    | none -> create pytest.ini | none                            | 20 |
| astropy | 3.6    | setup.cfg (line ~17/62)   | doctestplus, openfiles, arraydiff, astropy_header, filter_subpackage, remotedata | 7 |

## Deferred (structurally incompatible)
| Repo       | Instances | Reason |
|------------|-----------|--------|
| matplotlib | 15        | C-extension recompile per commit too slow/fragile |
| requests   | 8         | Test suite needs live network; containers have no internet -> 34 tests fail/hang, single run ~82s, blows iPFlakies timeout |
| django     | 231       | Needs own settings-configured runner (runtests.py); won't run under plain pytest |

## Per-instance steps
1. (host) docker pull ghcr.io/epoch-research/swe-bench.eval.x86_64.<INSTANCE_ID>
2. (host) docker run -it --name <name> <image> /bin/bash       # repo at /testbed
3. (host) docker cp <golden>.patch <name>:/testbed/golden.patch
   (host) docker cp <agent>.patch  <name>:/testbed/agent.patch
4. (container) cd /testbed && git apply golden.patch && git apply agent.patch
5. (container) pip install ipflakies pytest-random-order pytest-csv   # pulls pytest 6.2.5
6. (container) patch ipflakies utils.py terminal crash:
   IPF_UTILS=$(find /opt/miniconda3/envs/testbed -name utils.py -path "*ipflakies*" | head -1)
   wrap os.get_terminal_size() WIDTH/HEIGHT in try/except (read+write UTF-8)
7. (container) scope testpaths to the test file:
   - repo has testpaths in setup.cfg -> sed that line
   - no testpaths config -> create pytest.ini: [pytest]\ntestpaths = <test_file>
8. (container) astropy only: add -p no:doctestplus -p no:openfiles -p no:arraydiff
   -p no:astropy_header -p no:filter_subpackage -p no:remotedata to addopts
9. (container) COLUMNS=80 PYTHONUNBUFFERED=1 timeout 900 python -m ipflakies -i 10

## Key learnings
- Container Python is per-instance correct (3.6 or 3.9) -> fixes the collections import family.
- pip install always upgrades pytest to 6.2.5 (good for iPFlakies; breaks astropy's old plugins -> step 8).
- Most repos are CLEAN (no plugin disables). astropy was the only fussy one.
- sklearn's Cython extensions work because the container prebuilt them (venv couldn't).
- Proven: astropy-7166, sympy-13798, sphinx-7454, sklearn-14983 (all 0 flaky, all failed 100/100 on venv).

## astropy sub-limitation (found during batch run)
astropy is heterogeneous - splits into 3 groups:
- ~4 OLD: Python 3.6 + collections.Mapping -> WORKS with doctestplus plugin disables
- ~16 NEW: setup.cfg has "minversion = 7.0" -> requires pytest>=7.0, but iPFlakies needs
  pytest 6.2.5 -> INCOMPATIBLE. Marked ALWAYS_FAIL/NO_RESULT_FILE. Documented limitation.
- 2 (astropy-8872, astropy-8707): C-extension "Rebuilding extension modules" import error.
TODO maybe: check if iPFlakies works on pytest>=7 (would unlock the 16 NEW astropy).
