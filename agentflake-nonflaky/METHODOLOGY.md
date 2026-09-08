# AgentFlake non-flaky-focal-method pipeline - methodology & environment

Pivot from AgentFlake OD-detection: instead of generating a test for a KNOWN flaky test's
focal method, generate a test for a NON-flaky (developer-written) test's focal method, and
check whether the LLM-generated test itself turns out flaky. Question: does ChatUniTest
introduce flakiness (or other problems) that isn't present in the original developer test?

## Pipeline per subject
1. Clone the project, checkout the pinned commit.
2. `mvn test`, then scrape every `TEST-*.xml` under `**/target/surefire-reports/` for
   `classname#name` pairs -> the full list of tests that actually ran.
3. Exclude any test matching (a) `164_AgentFlake_Flaky_Tests.csv`'s `Flaky Test Name` column
   for this repo's `Slug`, or (b) any `Fully-Qualified Test Name` IDoFT lists for this repo's
   `Project URL` (any commit, not just the pinned one -- IDoFT flags a test as flaky for the
   *project*, not one SHA). What's left is "non-flaky" (i.e. not known-flaky).
4. Per remaining test: resolve its focal method via Jaccard (`focal_method_finder_batch.py`,
   local token-overlap heuristic) intersected with an LLM pick (`llm_focal.py`, gpt-4o) --
   only accepted when both agree (`status=agreed`). Then find the `src/main` class that
   actually DECLARES that focal method (not just the test-class-name with `Test` stripped --
   that guess is only the last-resort fallback).
5. Generate a test for `CUT#focal` with ChatUniTest (`chatunitest-maven-plugin:2.1.1:method`),
   pick whichever candidate compiles and passes ALONE.
6. Check the generated test three ways:
   - **ND** (non-deterministic): run it alone, same order, N times (100). Any fail/miss -> flaky.
   - **ID** (implementation-dependent): NonDex randomizes JDK-unspecified behavior (HashMap/
     HashSet iteration order etc.) across N runs (30). Any failure -> flaky.
   - **OD** (order-dependent): run the FULL suite (this test + every developer test) under N
     randomly shuffled orders (20), stock `-Dsurefire.runOrder=random` -- check if THIS test's
     outcome changes across orders.

No Docker for this pipeline (unlike the OD-detection pipeline) -- everything runs directly on
the WSL host's own `mvn`/`java`. Scripts: `01_collect_tests.sh`, `02_exclude_flaky.py`,
`03_generate_batch.sh`, `04_check_nd.sh`, `05_check_id_nondex.sh`, `06_check_od.sh`,
plus shared helpers `add_mockito.py`, `resolve_focal.sh`, `bump_surefire.py`,
`consolidate_results.py`.

## Recurring blockers + fixes (hit on Java-WebSocket, expect these again on other subjects)

1. **Old projects pin an ancient surefire that can't see JUnit5.** ChatUniTest emits JUnit5
   (Jupiter) tests; a project pinning e.g. `maven-surefire-plugin:2.17` (pre-JUnit5) silently
   runs `Tests run: 0` with `BUILD SUCCESS` for the generated test -- no error, just nothing.
   Fix for anything we invoke directly: skip the `test` lifecycle phase, chain
   `test-compile` + an explicit `org.apache.maven.plugins:maven-surefire-plugin:3.2.5:test`
   goal call. This bypasses whatever version the pom declares, with NO pom edit, for: the
   "does the candidate pass alone" check, the ND loop, and the OD sweep.
2. **NonDex has no such CLI escape hatch.** It resolves `maven-surefire-plugin`'s version
   from the pom itself via `mojo-executor` (calling the plugin from its own Java code, not
   from anything on our command line) -- so the explicit-goal trick above doesn't reach it.
   The ONLY fix found: temporarily bump the version IN the pom (`bump_surefire.py`) right
   before the NonDex call, then ALWAYS revert via `trap ... EXIT` so it never leaks past that
   one script. `nondex-maven-plugin:2.1.7` additionally hardcodes an old `surefire-junit47:2.17`
   dependency regardless of the pom -- use `2.2.5` instead, which doesn't.
3. **`Tests run: 0` / `BUILD SUCCESS` is a silent-failure trap, not just a JUnit5 issue --
   verify actual counts, never trust exit code alone.** Hit this three separate times in one
   session (surefire 2.17, then twice more with two different NonDex versions). Every check
   script now guards against it explicitly (e.g. `05_check_id_nondex.sh` sums every
   `Tests run: N` line in the log and refuses to report `NOT_FLAKY_ID` if the total is 0).
4. **Lambda syntax in generated tests vs. an old `-source`.** Some projects compile at
   `-source 1.6` (pre-Java-8); ChatUniTest's Mockito-based tests can use lambdas. Fix:
   `-Dmaven.compiler.testSource=8 -Dmaven.compiler.testTarget=8` on every mvn call -- affects
   ONLY test compilation, main source stays at whatever the project declares.
5. **Path bugs from re-using a single checkout across many tests, not one-zip-per-row.**
   `REPODIR`/`TESTLIST`/`RESULTS` must be resolved to absolute paths BEFORE any `cd`, or
   later references silently resolve relative to the wrong directory. And do NOT reuse
   `od_full.sh`'s per-row "delete all generated test files" cleanup inside a loop that
   processes MANY tests against the SAME checkout -- it deletes every prior iteration's
   already-passing generated test, not just the current attempt's stale scratch files.
   Fix: clean up a FAILED candidate specifically (archived to `generated-failed/round-N/`,
   not deleted -- keep the source for inspecting what the model got wrong), never touch a
   candidate that already won.
6. **Generation is genuinely non-deterministic run to run.** The same focal method can
   produce a passing candidate in one run and a wrong-assertion candidate in the next (seen
   directly on `Draft_6455#acceptHandshakeAsClient`). Don't treat one `CANDIDATE_FAILED` as
   final -- note it and move on; it's often worth a retry rather than a real dead end.
7. **Two DIFFERENT source tests that resolve to the SAME focal method can silently
   overwrite each other's generated file on disk.** ChatUniTest derives the generated
   class's filename from the CUT + focal method (e.g. `ByteBufferUtils_transferByteBuffer_
   0_0_Test.java`), not from the source test's name. `03_generate_batch.sh` copies each
   winning candidate to that SAME path, so if multiple source tests in one batch share a
   focal method (common -- e.g. 6 different `ByteBufferUtilsTest#testTransferByteBuffer*`
   tests all map to `ByteBufferUtils#transferByteBuffer`), only the LAST one processed in
   the batch survives physically -- earlier ones' passing candidates are gone by the time
   Stage 2 (ND/ID/OD) runs, even though `alone_result=pass` was correctly recorded for all
   of them at generation time. Symptom in the check scripts: `04_check_nd.sh` reports
   100% `missing` (not `fail`) and `05_check_id_nondex.sh` reports `NO_TESTS_RUN` -- both
   correctly detecting the method no longer exists. `06_check_od.sh`'s verdict for these
   rows is NOT trustworthy (it appears to match by class rather than exact test name, so it
   reports a false `NOT_OD`/pass). `consolidate_results.py` detects this signature
   (ND=100% missing AND ID=NO_TESTS_RUN) automatically and marks the row
   `INCONCLUSIVE_OVERWRITE` instead of `FLAKY_ND` -- these are excluded from the flaky
   count, not counted as clean either. Not yet fixed at the source (would need
   `03_generate_batch.sh` to copy each winning candidate to a per-source-test unique path,
   or run ND/ID/OD checks immediately after each individual generation instead of batching
   Stage 2 after all of Stage 1 finishes) -- flagged as a real fix to make before scaling
   past Java-WebSocket, since every subject will have some tests sharing a focal method.

## Focal-method derivation notes
- The flaky-test CSV/test list gives a TEST name, not the class under test. Strip
  `Test`/`TestCase`/`Tests`/`IT`/`ITCase`/`ITest` suffixes for CANDIDATE simple names, but
  the actual CUT is whichever `src/main` class DECLARES the resolved focal method -- prefer
  a stripped-name match, fall back to any class declaring it (preferring same package), and
  only fall back to naive name-stripping if nothing in `src/main` declares it at all.
- Jaccard+LLM intersection (`status=agreed`) has been reliable in this session (5/5 pilot
  tests agreed) -- same finding as the OD-detection pipeline.

## Result columns (results.csv)
subject, module, commit, source_test, focal_method, generated_test, alone_result,
nd_pass, nd_total, nd_verdict (NOT_FLAKY / FLAKY_ND / INCONCLUSIVE_OVERWRITE -- see
blocker #7), id_runs, id_verdict (NOT_FLAKY_ID / FLAKY_ID / NO_TESTS_RUN), od_pass,
od_total, od_verdict (NOT_OD / OD_SUSPECT / NO_TESTS_RUN), notes

`INCONCLUSIVE_OVERWRITE` rows are excluded from both the "clean" and "flaky" counts --
they mean the generated file was overwritten by a later batch item before Stage 2 could
check it, not that the test was run and found unstable. See blocker #7.
