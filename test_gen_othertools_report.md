
---

# Other Tools: EvoSuite

## Overview

This phase takes the focal methods where ChatUniTest failed or produced a wrong test, and runs a different generator on them to see if it does better. The generator here is EvoSuite, which is search-based and works on compiled bytecode instead of writing source from a signature. The idea is that some walls ChatUniTest hit are about writing source code (a generic type it cannot spell, a private inner class it cannot name), and a bytecode tool might not have those walls. For every method EvoSuite generates a passing test for, we run the same ND, ID, and OD pipeline.

I ran EvoSuite on the six methods ChatUniTest could not handle: wildfly lookup, wildfly fireEvent, elasticjob dataChanged, shardingsphere execute, and skywalking initialize. I used ormlite callBatchTasks as a baseline.

## Summary table

| Project | Focal method | Why ChatUniTest failed | EvoSuite reached it | ND | ID | OD |
|---|---|---|---|---|---|---|
| wildfly | lookup | wildcard-capture generics | yes, 34 tests, 6 real lookup calls | clean | clean | not measurable |
| wildfly | fireEvent | private inner dependent types | yes, 11 tests, 4 real fireEvent calls | clean | clean | not measurable |
| elasticjob | dataChanged | inner-class focal, tool NPE | yes, 2 tests, method runs | clean | clean | not measurable |
| shardingsphere | execute | non-constructible SUT | no, blocked building the object | - | - | - |
| skywalking | initialize | wrong property-to-field contract | yes, but assertions are trivial | clean | clean | - |
| ormlite | callBatchTasks | (was clean for ChatUniTest) | no, cannot reach the method | - | - | - |

**Breakdown**: EvoSuite reached four of the six methods ChatUniTest could not, and the two it missed it missed for a different reason than ChatUniTest did. Three of the four it reached are the structural cases (generics, private inner types, inner class). The fourth (skywalking) it reached but only with trivial assertions. OD came back not measurable on every EvoSuite test we could run it on, for the same reason each time (see finding 3).

## Tooling and setup notes

- **EvoSuite version -** 1.2.0, the last stable release. It is a JDK 8 era tool. Its bundled bytecode reader cannot parse classes newer than Java 8, so any target has to be compiled down to Java 8 first, and any dependency jar that ships newer classes has to be dropped from the classpath EvoSuite sees.
- **Multi-release jars break it -** h2 2.2.224 ships Java 21 classes inside META-INF/versions, and EvoSuite crashes reading them ("Unsupported class file major version 65") even though the class we target is Java 8. The fix is to strip any such jar out of the classpath handed to EvoSuite. This has to be checked per project.
- **EvoSuite output -** JUnit 4 by default, so no framework conversion is needed for OD, unlike ChatUniTest's JUnit 5 output. But every test extends an EvoSuite scaffolding class and needs the evosuite-standalone-runtime jar as a test dependency, which is not on Maven Central for 1.2.0 and has to be installed into the local repo by hand.
- **Surefire cannot see the JUnit 4 test -** in projects where ChatUniTest had earlier pulled in junit-jupiter, surefire runs zero tests on the EvoSuite JUnit 4 class. Same fix as before: remove junit-jupiter-engine so surefire uses the classic JUnit 4 provider.

## Findings

**1. EvoSuite clears the structural walls that stop ChatUniTest**
wildfly lookup has a wildcard-capture generic in its signature that ChatUniTest cannot write source against; EvoSuite generated 34 tests with 6 real calls to lookup, because it builds against erased bytecode where the wildcard is already gone. wildfly fireEvent depends on private inner types; EvoSuite reached it and even constructed one of those inner types by name. elasticjob dataChanged sits on a non-static inner class that made ChatUniTest crash before it started; EvoSuite built the whole chain by hand, the outer manager and then the inner listener through the outer.new Inner() form, and called dataChanged.

**2. EvoSuite fails on live infrastructure, not on source**
shardingsphere execute is the one structural case EvoSuite did not clear. It got further than ChatUniTest, it did try to build the object, but the object needs a live database connection to construct, and EvoSuite's sandbox blocks the socket, so construction dies before the method is reached. EvoSuite clears methods that are hard to write source for, but not methods that need a real running system (a database, and in other cases a live registry) to execute. ormlite callBatchTasks is the same kind of miss from the other direction: it takes a Callable and runs it inside a transaction against a live connection, and EvoSuite's search never synthesizes that setup, so it stalls on the outer class and never reaches the method. Notably ChatUniTest did generate a passing test here, so this is a case where the LLM tool wins and the search tool loses.

**3. EvoSuite's tests cannot be OD-measured by iDFlakies**
Every EvoSuite test passed ND and ID, but OD came back not measurable on all of them. Each EvoSuite test class wraps itself in a sandbox (a fake filesystem, network, and security layer, plus static-state reset) set up once per class. iDFlakies runs tests in its own forked process and reorders them, and the sandbox does not survive that. So inside iDFlakies the EvoSuite tests never simply pass, they error or get skipped, and which one they do changes from run to run. iDFlakies could not get a passing baseline, and every flip I saw across 30 rounds was error-to-skipped or skipped-to-error, never a real pass-to-fail. The test itself is fine, as the full suite passes 116 of 116 under normal Maven.

**4. On correctness, the two tools fail in opposite ways**
skywalking initialize is where ChatUniTest generated a wrong test: it assumed a property named key1 maps onto a field named key1, which ConfigInitializer does not do, so the test fails. EvoSuite does not make that mistake, but only because it never tests the real behavior. It covers the method (100% method coverage) but its assertions are trivial: one checks that an empty input is still empty, one just constructs the object. It never engages the property-to-field contract, so it never has the chance to be wrong. The line and mutation coverage confirm this, high method coverage but near-zero behavioral coverage. So on the correctness question neither tool produces a useful test: the LLM overreaches into the real behavior and asserts something false, and the search tool underreaches to whatever it can trivially cover.

## Conclusion

EvoSuite clears the errors that were about writing source code, a generic type or a private inner class or an inner-class target, because it works on bytecode. However, it fails on the ones that were about the method needing a real running system to execute (later in the process). EvoSuite's own tests turned out to be clean under ND and ID but not possible to measure under OD, and on the one correctness case, the two tools miss in mirror-image ways, one guessing wrong and one not guessing at all.
