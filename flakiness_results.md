# Flakiness of AI-Generated Java Tests — Results Log

**Question:** When ChatUniTest (gpt-4o) generates unit tests for a Java class, are the generated tests themselves flaky? <br>
**Detectors:** NonDex → implementation-dependent (ID) · iDFlakies → order-dependent (OD) <br>
**Dataset:** test_list.csv (IDoFT known-flaky Java tests). Each project compiled from its bundled .m2, under the JDK pinned in the row.

> A test counts toward flakiness only if it first compiles and passes in normal order. Excluded broken tests before detection.

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

**Totals: 15 projects · ~233 clean AI-generated tests · 0 ID-flaky · 0 OD-flaky.**
ND (100x non-determinism) column pending — Phase 2, reuses compiled tests, no API needed.

## Null results — when ChatUniTest could not produce testable output

| Cause | Projects |
|-------|----------|
| JUnit5 tests / project harness runs 0 | json-io, snakeyaml, snakeyaml-engine (ParserImpl, Emitter, StandardRepresenter), snowflake PreparedStatementV1 |
| Monolithic class / parse hang | opennlp, underscore-java, twilio |
| POJO — accessors only, nothing to generate | castle-java |
| Framework/complex-typed params — all methods skipped | sling-servlets-get, pair-distribution-app, jinjava |
| Repair rounds exhausted — generated tests never compile | adyen, commons-collections (Flat3Map, AbstractDualBidiMap, SingletonMap), appengine (LegacyProcessHandler, CloudSdk) |

Nulls are a finding, not a failure: they characterize *when* an LLM test generator can and cannot produce usable tests for a given class shape.


## Methodology notes (reproducibility)

1. Pin JDK per row for compile + generate + detect.
2. Build the project jar first (mvn install, skipping tests/javadoc/gpg/enforcer) — ChatUniTest needs target/*.jar.
3. Inject junit-jupiter-engine + junit-platform-launcher + a pinned surefire-junit-platform provider — generated tests are JUnit 5; projects with only junit:junit 4.x otherwise run 0 of them.
4. Bump ancient source levels (1.5/1.6/1.7 -> 1.8) so generated lambdas compile.
5. Exclude tests that fail in normal order before detection (broken != flaky; iDFlakies needs a passing baseline).
6. mvn clean test-compile before detection — iDFlakies reads .class files, so stale bytecode creates ghost tests.
7. Pre-screen each class by counting public non-accessor methods with simple-typed params; skip POJOs (accessors only) and monoliths (>150 methods) to avoid guaranteed nulls.
8. Fresh download + extract + parse-cache per run to avoid poisoned ChatUniTest class-info caches.
