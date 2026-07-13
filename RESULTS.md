# Flakiness of AI-Generated Java Tests

## The question

When ChatUniTest (using gpt-4o) generates unit tests for a Java class, are those generated tests flaky? A test is flaky if it can pass or fail on the same code depending on things it shouldn't depend on. I checked three kinds:

- **ID (implementation-dependent):** fails when the JVM changes the order of things like HashMap iteration. Detected with NonDex.
- **OD (order-dependent):** fails depending on what other tests ran before it. Detected with iDFlakies.
- **ND (non-deterministic):** fails intermittently even run by itself. Detected by running the test 100 times.

A test only counts toward flakiness if it first compiles and passes in normal order. If a generated test is just broken (fails every time), that's not flaky, it's wrong — I exclude those before running the detectors, and I log how many.

## What I found

I generated tests for **35 classes across about 20 projects** from the IDoFT dataset. Every project was compiled from its bundled dependencies under the JDK it was pinned to (8 or 11).

**Result: of the 35 classes, 34 produced only clean tests — 0 ID-flaky and 0 OD-flaky. One class produced a flaky test.**

That one flake is the interesting part.

### The flaky test: marine-api `Time`

ChatUniTest generated a test called `testToStringDefaultConstructor` for the `Time` class. It fails about **17% of the time when run completely on its own** (17 failures in 100 runs). iDFlakies also flagged it, and it reproduced across two separate detection runs.

**Why it's flaky:** the `Time` no-argument constructor reads the current system clock (`new GregorianCalendar()` → current hour/minute/second). The generated test builds its expected string with the format `%05.3f` for the seconds field. That format does not zero-pad the whole-number part. So when the current clock-seconds are a single digit (0–9), the test builds `"3.000"` while `Time.toString()` produces `"03.000"`, and the assertion fails.

Single-digit seconds happen 10 out of every 60 seconds, so the test should fail about 17% of the time — which matches the 17/100 I measured exactly.

So this isn't a flaky project or a flaky detector. The LLM wrote a test that asserts on a value that depends on what time it is when the test runs. That's a concrete example of a way LLM-generated tests can go wrong.

Example failure: `expected: <17403.000> but was: <174003.000>`

## Clean results (35 classes, 0 flaky)

| Project | Classes tested |
|---------|----------------|
| edn-java | Printers |
| JSON-java (JDK11) | JSONObject |
| JSON-java (JDK8) | JSONArray, JSONTokener, XML |
| java-classmate | ResolvedType |
| json-schema-validator | CollectorContext |
| jmeter-maven-plugin | TestConfiguration |
| emobility-smart-charging | FuseTree |
| jmeter-datadog | DatadogBackendClient |
| fosstars-rating-core | VulnerabilitiesFromOwaspDependencyCheck |
| javacpp | Info, ByteIndexer, ULongIndexer |
| snowflake-jdbc | SnowflakeConnectionV1 |
| FluentJPA | ScopedHashSet, ScopedHashMap, ScopedArrayList |
| fastjson | SerializeWriter |
| r2dbc-mysql | MySqlConnectionConfiguration, ParameterWriter, InternalArrays |
| ormlite-core | EagerForeignCollection, LazyForeignCollection, Where |
| commons-lang | MutableShort, MutableByte |
| commons-collections | Flat3Map, SingletonMap, AbstractDualBidiMap |
| maven-dependency-plugin | DependencySilentLog, Coordinates, ProcessArtifactItemsRequest |
| marine-api | SentenceListenerExamples, SentenceParser |

All 35 came back 0 ID-flaky and 0 OD-flaky. The full per-class numbers (files generated, clean count, excluded count) are in `results.md` and `flakiness_results.md`.

## Where ChatUniTest couldn't generate usable tests

Not every class produced testable output. This isn't failure — it maps out where an LLM test generator hits its limits. Grouped by cause:

| Cause | Examples |
|-------|----------|
| Project harness runs 0 tests (JUnit setup / native libraries) | json-io, snakeyaml, snakeyaml-engine, classgraph, jnr-posix |
| Class too big / parser hangs | opennlp, underscore-java, twilio |
| POJO — only getters/setters, nothing worth testing | castle-java |
| Methods take framework/complex types, all skipped | sling-servlets-get, pair-distribution-app, jinjava |
| Generated tests never compile | adyen, jackson-databind |
| Stateful void methods, nothing to assert | commons-lang StopWatch |
| Project build needs a plugin that fails on bundled sources | mybatis-3 (maven-pdf-plugin) |

## Two detectors, both checked

I didn't just trust the tools. I confirmed each one actually detects flakiness:

- **NonDex (ID):** I ran it against a known-flaky developer test (edn-java `PrinterTest#testPrettyPrinting`, the seed the dataset gives). It failed the test under a shuffled configuration and passed it clean — so it detects real ID flakiness.
- **iDFlakies (OD):** it caught the marine-api `Time` flake live, on my own generated tests, and reproduced it. That's stronger proof it works than any reference test would be.

## One thing worth flagging: build plugins can hide good tests

Early on, several projects looked like nulls ("won't compile" / "jar not built") that were actually fine. The cause was project build plugins rejecting the generated tests before they could run — Apache RAT (checks every file has a license header), animal-sniffer (API signature check), and maven-pdf-plugin. The generated tests were correct; the build failed on a license-header check.

Once I skipped those plugins, 8 classes that looked like nulls produced clean results (commons-lang, commons-collections, maven-dependency-plugin). Worth knowing for anyone doing this kind of study: an LLM-generated test won't have a license header, and some project builds will fail the whole build over that.

## How to reproduce

Pipeline scripts are in the repo (`run_one.sh`, `run_all.sh`, `screen.sh`, `patch_pom.py`). Main steps per class:

1. Pin the JDK the dataset specifies.
2. Build the project jar first (ChatUniTest needs it), skipping enforcer, gpg, javadoc, animal-sniffer, and RAT.
3. Patch the pom to add the JUnit 5 engine, platform launcher, and a pinned surefire junit-platform provider (generated tests are JUnit 5; projects with only JUnit 4 otherwise run zero of them).
4. Generate tests with ChatUniTest.
5. Exclude any test that fails in normal order (broken, not flaky) — logged.
6. Run NonDex for ID, iDFlakies for OD, and a 100x loop for ND.

`screen.sh` pre-filters classes before spending an API call — it skips POJOs, monster classes, and classes whose methods all take framework types, which predicts almost every null in advance.
