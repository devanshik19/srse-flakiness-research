# AI Test Generation and Flakiness Evaluation

## Overview

This phase takes the focal methods identified earlier (Jaccard and LLM, intersected)
and runs the experiment the focal-method work was building toward: generate an AI test
that targets each focal method, then check whether that generated test is flaky. The
generator is ChatUniTest. Flakiness is checked three ways: ND (plain reruns), ID
(NonDex), and OD (iDFlakies).

The pipeline for each target is:
1. Build the project so ChatUniTest has a compiled jar to work against.
2. Add the test dependencies ChatUniTest needs (JUnit 5 and Mockito), since its
   generated tests use them even when the project itself is on JUnit 4.
3. Generate a test for the focal method.
4. Copy the generated test into src/test, isolate it, confirm it compiles and passes.
5. Run ND, ID, and OD detection on it.

## Summary table

| Project | Set | Focal method | Generated | ND | ID | OD | Notes |
|---|---|---|---|---|---|---|---|
| ormlite | OD | createIfNotExists | yes | clean | clean | blocked | |
| ormlite | OD | createObjectInstance | yes | clean | clean | blocked | |
| ormlite | OD | queryRaw | yes | clean | clean | blocked | |
| ormlite | OD | callBatchTasks | yes | clean | clean | blocked | |
| ormlite | OD | isTableExists | no | - | - | - | skipped by tool |
| ormlite | OD | endThreadConnection | no | - | - | - | skipped by tool |
| skywalking | ID | initialize | yes | clean | clean | blocked | one of two generated methods is incorrect |
| Strata | ID | of | yes | clean | clean | clean | |
| servicecomb | ID | onFilter | yes | clean | clean | clean | |
| mercury | ID | getJournaledRoutes | yes | FLAKY | - | - | reproduces flakiness |
| TestParameterInjector | ID | parseYamlStringToJavaType | yes | clean | clean | clean | |
| feign | ID | resolve | no | - | - | - | package-private, tool cannot target it |
| dubbo | OD | telnet | no | - | - | - | not completed |
| wildfly | OD | fireEvent | no | - | - | - | blocked on missing JBoss deps |
| wildfly | OD | lookup | no | - | - | - | blocked on missing JBoss deps |
| shardingsphere-elasticjob | OD | dataChanged | no | - | - | - | focal method on inner class, tool cannot target |
| shardingsphere | ID | execute | no | - | - | - | not completed |
| undertow | ID | (none) | no | - | - | - | no focal-method candidate found |
| Struts | ID | (none) | no | - | - | - | JUnit 3, no annotation to detect |
| activemq | ID | (none) | no | - | - | - | JUnit 3, no annotation to detect |

Breakdown: generated and evaluated for flakiness on 8 focal methods across 6 projects.
Of those, 7 were clean and 1 (mercury) was flaky. The rest could not be generated for,
because the focal method is inaccessible to the tool (package-private, inner class), the
build is blocked, or no focal method exists (JUnit 3, indirection).

## Tooling and setup notes

- **ChatUniTest version.** Only 2.1.1 installs. 2.0.0 and 2.1.0 fail to resolve on Maven
  Central (missing chatunitest-core jar). Confirmed by trying both.
- **Method goal.** The method goal throws an ArrayIndexOutOfBoundsException in some
  environments; the class goal is the reliable fallback. On a fresh setup the method goal
  worked with a Class#method selector.
- **JUnit 5 plus Mockito.** Generated tests use both, so JUnit 4 projects needed them
  added before the tests would compile.
- **Per-project build workarounds.** Every project needed something different to build:
  feign needed several plugin skips (rat, license, sundr, sortpom, enforcer); skywalking
  needed checkstyle skipped; servicecomb needed spotbugs skipped and a @SuppressWarnings
  for -Werror; mercury had broken pre-existing Kotlin tests that had to be moved aside.
- **OD detection is blocked at the tool level.** iDFlakies locates the tests but exits
  with a non-zero code before running any rounds, even against a clean baseline. Tried
  baseline cleanup, junit-platform-launcher, version comparison, and debug logging.
  Appears to be an iDFlakies-side issue; flagged to Shanto. Also worth noting: OD is a
  two-test interaction, so detecting it on a single isolated test needs the original
  polluter present in the suite.

## Findings

**1. The AI-generated tests are, with one exception, not flaky.**
Out of the roughly twenty focal methods, tests were generated and flakiness-checked for
eight, and only one came out flaky. The other seven were clean on both ND and ID. So the
headline is that targeting a focal method does not, on its own, regenerate flakiness;
the generated tests are mostly stable.

**2. The one flaky test (mercury) came from shared mutable state.**
The generated test for getJournaledRoutes fails nondeterministically, alternating between
one and two failures across fifteen reruns with no code changes. The method reads a shared
static map on the EventEmitter singleton, and the test asserts on that map's size with no
cleanup between test methods. The map accumulates entries across methods and JVM state, so
the assertions see 0, 2, or 4 entries depending on what ran before. The AI assumed the
singleton starts empty and in a known state, which is not guaranteed. This is a classic
shared-state / test-isolation flake, and it is the single case where the AI regenerated
flakiness on a focal method.

**3. Many generated tests are incorrect, separately from flakiness.**
A number of generated tests fail because they are wrong, not flaky. ormlite tests expect
a SQLException where the code throws RuntimeException; skywalking's initialize test uses
reflection into a private helper with the wrong signature and expects the wrong exception;
mercury's reflection assumes a private field is static. The recurring pattern is the AI
reaching into private internals through reflection with wrong assumptions and making
fragile assumptions about shared state. This is a real result about AI test quality that
holds independent of the flakiness question.

**4. Some focal methods are structurally out of reach for the generator.**
feign's resolve is package-private and shardingsphere-elasticjob's real focal method is on
an inner class. ChatUniTest targets neither. These are limits of the tool, not fixable
setup problems.

## Conclusion

The pipeline works end to end, though getting each project to build took real per-project
effort and the OD detector could not be made to run on the generated JUnit 5 tests. The
main takeaway is that AI-generated tests targeting focal methods are largely not flaky:
only one of eight generated tests was flaky, caused by an unsafe assumption about shared
singleton state. The more frequent problem is not flakiness but correctness, since many
generated tests fail outright on wrong exceptions, broken reflection, or bad state
assumptions.
