# Flakiness of AI-Generated Java Tests — Results Log
**Question:** When ChatUniTest (gpt-4o) generates unit tests for a Java class, are the generated tests themselves flaky? <br>
**Detectors:** NonDex → implementation-dependent (ID) · iDFlakies → order-dependent (OD) · 100x loop → non-deterministic (ND) <br>
**Dataset:** test_list.csv (IDoFT known-flaky Java tests). Each project compiled from its bundled .m2, under the JDK pinned in the row.
> A test counts toward flakiness only if it first compiles and passes in normal order. Broken tests are excluded (and logged) before detection.

Generated tests for **36 classes across ~20 projects**. **35 came back completely clean (0 ID, 0 OD, 0 ND). 1 class produced a flaky test** — marine-api `Time` (details below).

## Summary
| # | Project | Class | Gen | Clean | Excl | ID | OD | ND |
|---|---------|-------|-----|-------|------|----|----|----|
| 1 | edn-java | Printers | 8 | 7 | 1 | 0/7 | 0/7 | 0 |
| 2 | JSON-java | JSONObject | 92 | 85 | 7 | 0/85 | 0/85 | 0 |
| 3 | java-classmate | ResolvedType | 21 | 7 | 13 | 0/7 | 0/7 | 0 |
| 4 | json-schema-validator | CollectorContext | 5 | 4 | 1 | 0/4 | 0/4 | 0 |
| 5 | jmeter-maven-plugin | TestConfiguration | 1 | 1 | 0 | 0/1 | 0/1 | 0 |
| 6 | emobility-smart-charging | FuseTree | 9 | 9 | 0 | 0/9 | 0/9 | 0 |
| 7 | jmeter-datadog | DatadogBackendClient | 2 | 2 | 0 | 0/2 | 0/2 | 0 |
| 8 | fosstars-rating-core | VulnerabilitiesFromOwaspDependencyCheck | 5 | 6 | 1 | 0/6 | 0/6 | 0 |
| 9 | javacpp | tools.Info | 38 | 53 | 2 | 0/53 | 0/53 | 0 |
| 10 | javacpp | ByteIndexer | 11 | 12 | 14 | 0/12 | 0/12 | 0 |
| 11 | javacpp | ULongIndexer | 13 | 10 | 19 | 0/10 | 0/10 | 0 |
| 12 | snowflake-jdbc | SnowflakeConnectionV1 | 2 | 1 | 10 | 0/1 | 0/1 | 0 |
| 13 | FluentJPA | ScopedHashSet | 12 | 13 | 7 | 0/13 | 0/13 | 0 |
| 14 | FluentJPA | ScopedHashMap | 12 | 17 | 5 | 0/17 | 0/17 | 0 |
| 15 | FluentJPA | ScopedArrayList | 13 | 6 | 14 | 0/6 | 0/6 | 0 |
| 16 | JSON-java (JDK8) | JSONArray | 28 | 68 | 8 | 0/68 | 0/68 | 0 |
| 17 | JSON-java (JDK8) | JSONTokener | 16 | 25 | 8 | 0/25 | 0/25 | 0 |
| 18 | JSON-java (JDK8) | XML | 17 | 40 | 7 | 0/40 | 0/40 | 0 |
| 19 | fastjson | SerializeWriter | 19 | 24 | 17 | 0/24 | 0/24 | 0 |
| 20 | r2dbc-mysql | MySqlConnectionConfiguration | 4 | 8 | 2 | 0/8 | 0/8 | 0 |
| 21 | r2dbc-mysql | ParameterWriter | 9 | 10 | 0 | 0/10 | 0/10 | 0 |
| 22 | r2dbc-mysql | InternalArrays | 2 | 8 | 0 | 0/8 | 0/8 | 0 |
| 23 | ormlite-core | EagerForeignCollection | 8 | 17 | 21 | 0/17 | 0/17 | 0 |
| 24 | ormlite-core | LazyForeignCollection | 15 | 20 | 12 | 0/20 | 0/20 | 0 |
| 25 | ormlite-core | Where | 3 | 2 | 7 | 0/2 | 0/2 | 0 |
| 26 | commons-lang | MutableShort | 22 | 52 | 0 | 0/52 | 0/52 | 0 |
| 27 | commons-lang | MutableByte | 22 | 27 | 5 | 0/27 | 0/27 | 0 |
| 28 | commons-collections | Flat3Map | 15 | 45 | 3 | 0/45 | 0/45 | 0 |
| 29 | commons-collections | SingletonMap | 21 | 45 | 2 | 0/45 | 0/45 | 0 |
| 30 | commons-collections | AbstractDualBidiMap | 17 | 38 | 2 | 0/38 | 0/38 | 0 |
| 31 | maven-dependency-plugin | DependencySilentLog | 12 | 12 | 0 | 0/12 | 0/12 | 0 |
| 32 | maven-dependency-plugin | Coordinates | 7 | 17 | 1 | 0/17 | 0/17 | 0 |
| 33 | maven-dependency-plugin | ProcessArtifactItemsRequest | 3 | 4 | 0 | 0/4 | 0/4 | 0 |
| 34 | marine-api | SentenceListenerExamples | 1 | 1 | 0 | 0/1 | 0/1 | 0 |
| 35 | marine-api | SentenceParser | 6 | 9 | 2 | 0/9 | 0/9 | 0 |
| 36 | marine-api | **Time** | 5 | 15 | 1 | 0/15 | — | **17/100 FLAKY** |

**Totals: 35 clean classes (0 ID-flaky, 0 OD-flaky, 0 ND-flaky) · 1 flaky class (marine-api Time).**

## The flaky test — marine-api `Time`
ChatUniTest generated `testToStringDefaultConstructor`. It **fails ~17% of the time when run entirely on its own (17 fails / 100 runs)**. iDFlakies also flagged it, and it reproduced across two separate detection runs.

**Root cause:** `Time`'s no-arg constructor reads the current system clock (`new GregorianCalendar()` → current hour/minute/second). The generated test builds its expected string with the format `%05.3f` for seconds, which does not zero-pad the whole-number part. So when the current clock-seconds are a single digit (0–9), the test builds `"3.000"` while `Time.toString()` produces `"03.000"`, and the assertion fails. Single-digit seconds occur 10 of every 60 seconds → ~17% expected, matching the measured 17/100.

The LLM wrote a test that asserts on a value depending on what time it is when the test runs. Example failure: `expected: <17403.000> but was: <174003.000>`. Proof in `finding_marine_Time/` (start with `hundred_run_proof.txt` and `assertion_detail.txt`).

## Null results — when ChatUniTest could not produce testable output
| Cause | Projects |
|-------|----------|
| JUnit5 tests / project harness runs 0 (JUnit setup or native libs) | json-io, snakeyaml, snakeyaml-engine (ParserImpl, Emitter, StandardRepresenter), snowflake PreparedStatementV1, classgraph, jnr-posix |
| Monolithic class / parse hang | opennlp, underscore-java, twilio |
| POJO — accessors only, nothing to generate | castle-java |
| Framework/complex-typed params — all methods skipped | sling-servlets-get, pair-distribution-app, jinjava |
| Generated tests never compile | adyen, appengine (LegacyProcessHandler, CloudSdk), jackson-databind |
| Stateful void methods — nothing to assert | commons-lang StopWatch |
| Project build requires a plugin that fails on bundled sources | mybatis-3 (maven-pdf-plugin) |

## Detector validation
- **NonDex (ID):** ran against a known-flaky developer test (edn-java `PrinterTest#testPrettyPrinting`, dataset seed 933178) — failed it under a shuffled configuration, passed it clean. Detects real ID flakiness.
- **iDFlakies (OD):** caught the marine-api `Time` flake live on generated tests and reproduced it. A live positive detection is stronger validation than a reference test.

## Methodology notes (reproducibility)
1. Pin JDK per row for compile + generate + detect.
2. Build the project jar first (mvn install, skipping tests/javadoc/gpg/enforcer/animal-sniffer/rat) — ChatUniTest needs target/*.jar.
3. Inject junit-jupiter-engine + junit-platform-launcher + a pinned surefire-junit-platform provider — generated tests are JUnit 5; projects with only junit:junit 4.x otherwise run 0 of them.
4. Bump ancient source levels (1.5/1.6/1.7 -> 1.8) so generated lambdas compile.
5. Exclude tests that fail in normal order before detection (broken != flaky; iDFlakies needs a passing baseline).
6. mvn clean test-compile before detection — iDFlakies reads .class files, so stale bytecode creates ghost tests.
7. Pre-screen each class by counting public non-accessor methods with simple-typed params; skip POJOs and monoliths to avoid guaranteed nulls.
8. Fresh download + extract + parse-cache per run to avoid poisoned ChatUniTest class-info caches.
