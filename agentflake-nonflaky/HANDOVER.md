# HANDOVER — AgentFlake non-flaky-focal-method pipeline (session 1)

Living doc — update this after every finding so the next session doesn't rediscover the same
bugs or re-ask settled questions. See `METHODOLOGY.md` for the pipeline design and
the full list of blockers+fixes (don't duplicate that list here, just point to it and note
NEW findings as they happen).

## Status as of 2026-09-08 (end of session 1)

**Java-WebSocket is COMPLETE: all 90/90 non-flaky tests processed.** Ran in 3 batches
(pilot 5, batch2 20, batch3 65). Final tally in `results.csv`/`results.md`:

- **32 generated a candidate that passed alone and was fully checked ND(100)/ID(30)/OD(20)
  -- 0 confirmed flaky.** This is the headline finding for Java-WebSocket: across every
  non-flaky developer test we could generate a test for, ChatUniTest did not introduce any
  ND/ID/OD flakiness. Sample size caveat still applies (32 checked tests, not 90 -- see
  below for why the other 58 didn't reach a check).
- 3 `INCONCLUSIVE_OVERWRITE` -- NOT flaky findings, a pipeline artifact (see blocker #7 in
  `METHODOLOGY.md`): when multiple source tests share one focal method, only the LAST
  generated candidate survives on disk by the time Stage 2 runs. Confirmed via the
  ND=100%-missing + ID=NO_TESTS_RUN signature on all 3.
- 13 `CANDIDATE_FAILED` -- a candidate compiled but didn't pass alone. Worth inspecting
  `generated-failed/round-N/` for these before writing them off.
- 4 `GEN_FAILED` -- no candidate ever compiled across all 5 rounds.
- 38 `SKIPPED_FOCAL` -- Jaccard+LLM did not agree on a focal method (`disagreed`,
  `neither found a method`, or the newly-observed `llm only`, where the LLM found something
  but the local Jaccard heuristic didn't).

**That's a ~36% full-generation-and-check rate (32/90), much lower than the pilot's 80%.**
The `SKIPPED_FOCAL` count alone is 38/90 (42%) -- worth digging into next: is Jaccard+LLM
genuinely struggling on this later slice of tests (`issues.*`, `framing.*` constructor/
extends tests, `protocols.ProtoclHandshakeRejectionTest`), or is there a resolver bug? See
"Immediate next steps" below.

**Pipeline built and validated end-to-end on Java-WebSocket.** 6 scripts
(`01_collect_tests.sh` through `06_check_od.sh`) plus 3 helpers (`add_mockito.py` --
unmodified from the OD-detection repo, `resolve_focal.sh` + its 4 python helpers -- also
unmodified, `bump_surefire.py` -- new this session) plus `consolidate_results.py` (joins
generation + check CSVs into final rows, auto-detects the overwrite artifact) take a subject
from "clone at a pinned commit" through "N generated tests, each checked for ND/ID/OD
flakiness." All 7 blockers in `METHODOLOGY.md` were hit and fixed on Java-WebSocket
specifically; expect at least some of them to recur on the other 4 subjects (different
old-pom quirks are likely).

**Live logging added to all 4 check scripts this session** (they used to redirect Maven
output to a log file with no terminal feedback -- fixed via `tee` on single-call steps,
progress lines per iteration on looped steps). If a future session finds a script has
regressed to a silent blank-screen wait during a real run, that's a bug to fix, not expected
behavior.

**Known script bug, not yet fixed:** `04_check_nd.sh`, `05_check_id_nondex.sh`, and
`06_check_od.sh` don't write a header row into their own output CSV -- `run_batch3_checks.sh`
seeds each file empty (`: > file.csv`) and relies on the check scripts to append, but nothing
ever writes the header line. `consolidate_results.py` (and anything else using
`csv.DictReader`) will silently misparse the first data row as a header and then KeyError.
Worked around this time by prepending the header line by hand after the run finished. Fix
before the next subject: either have the check scripts write the header on first touch, or
have the runner script (`run_batch3_checks.sh`) seed it instead of `: > file`.

## Cloud session <-> WSL box workflow (read this before doing anything)

This Claude Code session (wherever it's running) has **no filesystem or shell access to the
WSL box** (`dev4nshi@LAPTOP-VME6MC5I`), and there is **no shared filesystem** between the two
even when paths look similar (e.g. both mentioning `C:\Users\...`) -- confirmed by a failed
`cp` across them in session 1. The only working pattern: hand Shinae ready-to-paste heredocs
or public-URL `curl`/`git clone` commands, she runs them on the WSL box, pastes output back.
Never claim to have "run" or "checked" anything there -- only report what she's actually
pasted.

## Where things live

- Scripts + all working state: `~/agentflake-work/nonflaky/` on the WSL box (NOT git-tracked --
  these are the pipeline scripts + helpers + per-subject clones like `java-websocket/`,
  which are large/disposable and don't belong in git). A copy of just the scripts (no clones)
  now also lives in `~/srse-research/agentflake-nonflaky/scripts/` for git tracking.
- `results.csv`, `results.md`, `METHODOLOGY.md`, this handover (as `HANDOVER.md`): live in
  `~/srse-research/agentflake-nonflaky/`, mirroring the existing `agentflake-od/` layout.
  Pushed to GitHub end of session 1.
- 164-flaky-test CSV: Shinae's local Downloads folder (`164_AgentFlake_Flaky_Tests.csv`),
  also reachable from WSL via `/mnt/c/Users/Amita/Downloads/...` (this one DOES work across
  the WSL mount, unlike the cloud session's own scratch-workspace paths).
- IDoFT flaky data: fetched fresh each time from
  `https://raw.githubusercontent.com/TestingResearchIllinois/idoft/main/pr-data.csv` (public).

## The 5 subjects (mentor-assigned)

1. **Java-WebSocket** (`TooTallNate/Java-WebSocket`) -- commit `fa3909c391195178ccf5a92d4ac342a30ae247c8`
   (from the 164 CSV). **DONE: 90/90 non-flaky tests processed, 0 confirmed flaky.** See the
   status summary above for the full breakdown (32 clean, 3 overwrite-artifact, 13
   candidate-failed, 4 gen-failed, 38 skipped-focal).
2. **http-request** -- repo owner unconfirmed (likely `kevinsawicki/http-request`), no commit yet.
3. **doanduyhai/Achilles** -- possible commit/setup reference at
   `shanto-Rahman/NOD-Test-Repair/blob/master/tdrepro/runAll.sh` (not yet checked).
4. **javadelight/delight-nashorn-sandbox** -- no commit yet.
5. **qos-ch/logback** -- commit `0f57531977287fd3d8c9046e9f68e281715f3b10` (from the 164 CSV,
   row 89, `SMTPAppender_GreenTest#testCustomBufferSize`).

## Immediate next steps

1. **Investigate the ~65-ish non-passing batch3 tests** (13 CANDIDATE_FAILED + 4 GEN_FAILED +
   38 SKIPPED_FOCAL = 55 of 90 total). This hit rate (32/90 = 36%) is much lower than the
   pilot's (4/5 = 80%). Worth checking: is `SKIPPED_FOCAL` genuinely correct here (these ARE
   harder cases -- `Issue580Test`'s 13 `runCloseBlockingTestScenario*`/
   `runNoCloseBlockingTestScenario*` methods and `ProtoclHandshakeRejectionTest`'s 5
   parameterized rejection-case methods all came back `status=llm` -- LLM found a focal
   method, Jaccard didn't -- plausible for heavily-parameterized/scenario-style tests with
   generic names), or is something else going on (e.g. `testConstructor`/`testExtends`
   pattern tests across `BinaryFrameTest`/`CloseFrameTest`/`ContinuousFrameTest`/
   `PingFrameTest`/`PongFrameTest`/`TextFrameTest` all disagreeing/neither -- these look like
   trivial inheritance-check tests that may not HAVE a meaningful single focal method, which
   would mean `SKIPPED_FOCAL` is the CORRECT outcome, not a bug to fix).
2. Fix blocker #7 (file-overwrite when source tests share a focal method) before scaling to
   subject #2 -- either unique-path-per-source-test in `03_generate_batch.sh`, or run Stage 2
   immediately after each Stage 1 generation instead of batching it at the end.
3. Fix the missing-CSV-header bug in `04_check_nd.sh`/`05_check_id_nondex.sh`/
   `06_check_od.sh` (see above) before the next subject's Stage 2 run.
4. Get commits for http-request and Achilles (check the NOD-Test-Repair `runAll.sh` link
   above for Achilles; http-request needs a source -- IDoFT? ask Shinae?), then start
   subject #2.
5. Longer-term open question (from the advisors' Slack thread, carried over from the prior
   OD-detection handovers): how do you know a test is truly non-flaky just because it's
   absent from IDoFT and the 164 CSV -- IDoFT is not exhaustive. Not resolved, not blocking
   current work, but worth keeping in mind when writing up findings.

## Correction log (mistakes made this session -- don't repeat)

- Assumed the cloud session's scratch-workspace path would be reachable from WSL via
  `/mnt/c/...` because both mention `C:\Users\Amita`. It is NOT -- these are different
  machines/filesystems despite the superficially similar path. Always hand over file
  CONTENT (heredoc or public URL), never a path from this session's own sandbox.
- Reused `od_full.sh`'s per-row "delete generated test files" cleanup inside a loop over
  MANY tests sharing one checkout -- this silently deleted earlier iterations' already-
  passing generated tests. Caused a false "FLAKY_ND" (files were gone, not flaky) before
  being caught by manually verifying the files still existed. See blocker #5 in the
  methodology doc.
- Trusted NonDex's exit code (0 = success) without checking whether it actually ran any
  tests. Twice. Both times it had silently run `Tests run: 0` across all configs. Now
  guarded in the script itself (sums `Tests run:` counts, refuses to report a verdict if the
  total is 0) -- but the underlying lesson applies to any tool integration: check that the
  thing you asked for actually happened, don't trust "BUILD SUCCESS" alone.
- `04/05/06_check_*.sh` never write a header into their own output CSV; `run_batch3_checks.sh`
  seeds the file empty and expects the check scripts to append -- nothing ever writes the
  header line, so `consolidate_results.py`'s `csv.DictReader` misparsed the first data row
  as a header and KeyError'd. Worked around by hand this time (`sed -i '1i ...'`); real fix
  still pending, see "Immediate next steps" #3.
