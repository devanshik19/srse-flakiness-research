# AI Test Generation and Flakiness Evaluation

## Overview

This phase takes the focal methods identified earlier (Jaccard and LLM, intersected) and runs the experiment the focal-method work was building toward: generate an AI test that targets each focal method, then check whether that generated test is flaky. The generator is ChatUniTest. Flakiness is checked three ways: ND (plain reruns), ID (NonDex), and OD (iDFlakies).

The pipeline for each target is:
1. Build the project so ChatUniTest has a compiled jar to work against.
2. Add the test dependencies ChatUniTest needs (JUnit 5 and Mockito), since its generated tests use them even when the project itself is on JUnit 4.
3. Generate a test for the focal method.
4. Copy the generated test into src/test, isolate it, confirm it compiles and passes.
5. Run ND, ID, and OD detection on it. For OD, the generated test is run inside the full developer suite so the original polluters are present, since OD is a two-test interaction and cannot be seen on an isolated test.

## Summary table

| Project | Set | Focal method | Generated | ND | ID | OD | Notes |
|---|---|---|---|---|---|---|---|
| ormlite | OD | createIfNotExists | yes | clean | clean | OD-flaky | order-dependent in the full suite |
| ormlite | OD | createObjectInstance | yes | clean | clean | OD-flaky | order-dependent in the full suite |
| ormlite | OD | queryRaw | yes | clean | clean | OD-flaky | order-dependent in the full suite |
| ormlite | OD | endThreadConnection | yes | clean | clean | OD-flaky | order-dependent in the full suite |
| ormlite | OD | isTableExists | yes | clean | clean | clean | |
| ormlite | OD | callBatchTasks | yes | clean | clean | clean | |
| skywalking | ID | initialize | yes | - | - | - | generated but incorrect (wrong property-to-field assumption) |
| Strata | ID | of | yes | clean | clean | clean | |
| servicecomb | ID | onFilter | yes | clean | clean | clean | |
| mercury | ID | getJournaledRoutes | yes | FLAKY | *(see below) | - | reproduces flakiness |
| TestParameterInjector | ID | parseYamlStringToJavaType | yes | clean | clean | clean | OD measured after JUnit 4 conversion |
| feign | ID | resolve | yes | clean | clean | clean | OD measured after JUnit 4 conversion |
| dubbo | OD | telnet | yes | clean | clean | clean | |
| wildfly | OD | fireEvent | no | - | - | - | dependent types are private inner classes ([log](https://drive.google.com/file/d/1kCwtnJDU5im8dlLOjmPSz_JEYjUnE1l6/view?usp=drive_link)) |
| wildfly | OD | lookup | no | - | - | - | the method's signature uses a wildcard generic that ChatUniTest cannot write a working test for ([log](https://drive.google.com/file/d/1hQP-9rx_F7Lr-NLwcQBzG-7AgIz9oWgJ/view?usp=drive_link)) |
| shardingsphere-elasticjob | OD | dataChanged | no | - | - | - | focal method on inner class, tool cannot target ([log](https://drive.google.com/file/d/1N_MG7LjgtkZWAs01cqT_TlSpQJZUaJHL/view?usp=drive_link)) |
| shardingsphere | ID | execute | no | - | - | - | non-constructible SUT (no default constructor, needs real connection and rules) ([log](https://drive.google.com/file/d/15X-Ie6UiQafrGEdbUASthMfY1zp7LmEV/view?usp=drive_link)) |
| undertow | ID | (none) | no | - | - | - | no focal-method candidate found ([log](https://drive.google.com/file/d/1oSKCD4vjMPxVRJ5VhvplhtE5TG9iQdd3/view?usp=drive_link)) |
| Struts | ID | fromObject | partial | - | - | - | generates and compiles, but JUnit 3 harness blocks execution |
| activemq | ID | (none) | no | - | - | - | no unit-level SUT to target ([log](https://drive.google.com/file/d/1NQksrj_aCMVltb2KQA_z4fKWmeeDhBU9/view?usp=drive_link)) |

 *ID and OD are not reported for mercury. NonDex could not give a clean ID reading because the test is already unstable on its own, and OD does not apply since the flakiness comes from shared static state, not test ordering.

**Breakdown**: generated and flakiness-checked on 13 focal methods across 8 projects. Of those, 4 were OD-flaky (all in ormlite), 1 was ND-flaky (mercury), 7 were clean on every axis measured, and 1 (skywalking) generated but was incorrect. The rest could not be generated for, because the focal method is inaccessible to the tool (inner class, wildcard generics, private inner types), the SUT cannot be constructed, or no real focal method exists.

## Tooling and setup notes

- **ChatUniTest version -** Only 2.1.1 installs. 2.0.0 and 2.1.0 fail to resolve on Maven Central (missing chatunitest-core jar). Confirmed by trying both.
- **JUnit 5 plus Mockito -** Generated tests use both, so JUnit 4 projects needed them added before the tests would compile.
- **Per-project build workarounds -** Every project needed something different to build: feign needed several plugin skips (rat, license, sundr, sortpom, enforcer); skywalking needed checkstyle skipped; servicecomb needed spotbugs skipped; mercury had broken pre-existing Kotlin tests that had to be moved aside; dubbo needed its surefire version bumped and a mockito-core version pinned.
- **OD detection and mixed frameworks -** iDFlakies refuses to run when a JUnit 5 generated test sits in a JUnit 4 developer suite (throws an error "this project contains both JUnit 4 and JUnit 5 tests"). The fix is to convert the generated test to JUnit 4 so the suite is single-framework, then remove junit-jupiter-engine so surefire uses the classic JUnit 4 provider. This is what made OD measurable on TestParameterInjector and feign. 

## Findings

**1. AI-generated tests can regenerate OD flakiness, at a meaningful rate.**
In ormlite, 4 of the 6 focal methods that generate produced OD-flaky tests. Each one is clean under ND and ID in isolation, and only becomes flaky when run inside the full developer suite, where a polluter leaves shared state that changes the test's result depending on order. Targeting a focal method does not regenerate ND or ID flakiness, but it does regenerate order-dependent flakiness, because the generated tests do not guard against shared-state pollution. This was reproduced with freshly, independently generated test bodies, so it is not an artifact of just one generation.

**2. The one ND-flaky test (mercury) came from shared mutable state.**
getJournaledRoutes reads a static map populated from journal.yaml, while the test assumes it is empty. The map’s state is not reset or controlled between executions, so it can contain the two journaled routes in some runs and be empty in others. This causes the test to randomly receive 2 instead of the expected 0, producing non-deterministic flakiness.

**3. Many generated tests are incorrect, separately from flakiness.**
A number of generated tests fail because they are wrong, not flaky. skywalking's initialize test assumes a property named key1 maps straight onto a field named key1, which ConfigInitializer does not do, so the field stays null. Strata's null-argument tests (in one candidate) expect NullPointerException where the code throws IllegalArgumentException. dubbo's generated test stubbed a static method with plain Mockito and included a reflection test for a method that does not exist. The recurring pattern is the *AI reaching into internals with wrong assumptions about a method's contract*. Notably, correctness holds up for simple methods (a pure YAML parser, a plain factory) and breaks down where the method's behavior is not obvious from its signature.

**4. Some focal methods are structurally out of reach for the generator.**
wildfly fireEvent depends on private inner classes the generated test cannot see; wildfly lookup has wildcard-capture generics in its signature that ChatUniTest cannot produce a compiling test for; shardingsphere-elasticjob's focal method is on an inner (nested) class; shardingsphere execute's SUT has no default constructor and needs a real connection and rules to build.

## Conclusion

The pipeline works end to end, though getting each project to build and getting OD to run took real per-project effort. The main new result is that AI-generated tests targeting focal methods do regenerate flakiness, but the flakiness is order-dependent, not ND or ID: 4 of 6 ormlite focal methods produced OD-flaky tests, all clean in isolation and flaky only in the full suite, driven by shared-state pollution the generated tests do not defend against. Alongside that, the more frequent problem is correctness rather than flakiness, since several generated tests fail outright on wrong assumptions about a method's contract, and correctness degrades exactly where that contract is not visible from the signature.
