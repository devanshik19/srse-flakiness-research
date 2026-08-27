# AgentFlake OD detection - methodology & environment

Pipeline per row: pick OD row from test_config.csv -> ReproFlake OD container -> ChatUniTest generates
a test for the named flaky test's focal method -> run generated test with the module's tests under
100 class-shuffled orders (custom Surefire testorder) -> flag if the generated test flips -> targeted
probe (known polluter first) with positive+negative controls.

## Environment
- Image flaky_base_jdk8_od_cov (Dockerfile.od: Maven 3.8.6 + TestingResearchIllinois/maven-surefire ext, JDK8).
- docker exec default cwd = /app; always pass -w /app/source.

## Five recurring blockers + fixes (hit on EVERY subject)
1. ChatUniTest 2.1.1 needs newer Maven than 3.8.6 (NoSuchMethodError parseCommaSeparatedUniqueNames).
   Install Maven 3.9.9 in the container, use ONLY for generation (-Dmaven.repo.local=/root/.m2/repository).
   Keep system mvn (has the surefire extension) for all OD runs.
2. Named victim test may be empty/inherited - read source to find the REAL focal method before -DselectMethod.
3. patch_pom.py's chatunitest-starter drags junit4 -> Surefire picks JUnit4Provider -> Tests run: 0 +
   BUILD SUCCESS (vacuous green - ALWAYS check counts). For RUNNING tests: restore pristine module pom
   (unzip -o -j <zip> "*/<module>/pom.xml"), add ONLY mockito + pinned junit5 stack; no chatunitest-starter.
4. After junit4 removed: NoSuchFieldError NOOP (launcher 1.9.1 vs parent-pinned older platform). Add
   test-scoped DIRECT deps: mockito-core & mockito-junit-jupiter 4.11.0, junit-jupiter-api & -engine 5.9.1,
   junit-platform-launcher & -engine & -commons 1.9.1.
5. This Surefire fork REQUIRES -Dtest on every run (getTest() does new File(test); null -> NPE). No bare
   full-suite run. Enumerate test classes from target/test-classes and always pass -Dtest.

## Order mechanism
-Dtest accepts an ABSOLUTE FILE PATH, one class#method per line. Methods from different classes cannot
interleave (fork coalesces by first-seen class), so order files must be class-grouped (shuffle class order,
methods contiguous + in original order per class). run_od.sh sanity-checks tests-requested vs tests-run.

## Scripts
run_od.sh (random sweep), run_targeted.sh (polluter-first probe + controls). Reusable across subjects.

## Result columns (results.csv)
subject, module, focal_method, generated_test, alone(pass/fail), sweep_orders, sweep_pass,
ctrl_polluterFirst(pass/fail), ctrl_victimFirst(pass/fail), gen_polluterFirst(pass/fail), od_verdict, notes
