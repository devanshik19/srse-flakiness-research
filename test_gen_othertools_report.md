
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
The three methods ChatUniTest could not generate for because of a language feature (a wildcard generic, private inner types, a non-static inner class), EvoSuite generated working tests for. It works on erased bytecode, so a type it cannot spell in source is not a wall. For elasticjob it even built the outer manager and the inner listener by hand and called the method.

**2. EvoSuite fails on live infrastructure, not on source**
shardingsphere execute needs a live database connection to even construct the object, and EvoSuite's sandbox blocks the socket, so it dies before the method. ormlite callBatchTasks is the reverse: it needs a Callable run inside a transaction, and EvoSuite never builds that setup, though ChatUniTest did. So the search tool loses exactly where semantic setup is needed.

**3. EvoSuite's tests cannot be OD-measured by iDFlakies**
Every EvoSuite test passed ND and ID but OD was not measurable. Each test class sets up a sandbox once per class, and iDFlakies' forked, reordered runner breaks it, so the tests error or skip instead of passing and no baseline holds. The test is fine on its own (116 of 116 under normal Maven); this is a tooling clash, not an order dependency.

**4. On correctness, the two tools fail in opposite ways**
On skywalking initialize ChatUniTest guessed the property-to-field contract wrong and failed. EvoSuite does not guess wrong only because it never tests that behavior: it covers the method but its assertions are trivial (empty input stays empty, object constructs). So the LLM overreaches and asserts something false, and the search tool underreaches to whatever it can trivially cover.

## Conclusion

EvoSuite clears the errors that were about writing source code, a generic type or a private inner class or an inner-class target, because it works on bytecode. However, it fails on the ones that were about the method needing a real running system to execute (later in the process). EvoSuite's own tests turned out to be clean under ND and ID but not possible to measure under OD, and on the one correctness case, the two tools miss in mirror-image ways, one guessing wrong and one not guessing at all.
