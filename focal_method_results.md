# Focal Method Finder — Results (last set)

For 20 known-flaky tests (10 ID, 10 OD), find the focal method. Uses the
7-step approach from the UTFix paper (arxiv.org/abs/2503.14924, Section 4.1).
Pipeline: parse the test to an AST, extract its method calls, tokenize the test
name and each called method name, filter to methods defined in the project's own
`src/main`, then score each candidate by Jaccard similarity to the test name and
pick the highest. Steps 1,2,3,5 (extraction/filtering) and 4,6 (scoring/selection)
were split across two people; this covers one 20-test set end to end.

## Results

### OD tests (10/10 focal method found)
| Project | Flaky test | Focal method | Score | Note |
|---------|-----------|--------------|-------|------|
| ormlite-core | testIsTableExistsThrow | isTableExists | 0.60 | |
| ormlite-core | testQueryRawRowMapperThrow | queryRaw | 0.33 | |
| ormlite-core | testEndThreadConnectionThrows | endThreadConnection | 0.60 | |
| ormlite-core | testCreateIfNotExistsThrow | createIfNotExists | 0.67 | |
| ormlite-core | testCreateObjectInstanceThrows | createObjectInstance | 0.60 | |
| ormlite-core | testCallBatchTasksNestedInTransaction | callInTransaction | 0.43 | tie, likely callBatchTasks |
| dubbo | testChangeServiceNotExport | telnet | 0.00 | see below |
| wildfly | testFireMultiLevelEvent | fireEvent | 0.40 | |
| wildfly | testLookupBinding | lookup | 0.33 | |
| shardingsphere-elasticjob | assertRemoveLocalInstancePath | getInstance | 0.17 | tie |

### ID tests (8/10 focal method found, 2 not detected)
| Project | Flaky test | Focal method | Score | Note |
|---------|-----------|--------------|-------|------|
| skywalking | testInitialize | initialize | 0.50 | |
| Strata | of_addition | of | 0.50 | |
| mercury | journalYamlTest | getInstance | 0.00 | tie |
| shardingsphere | assertInsertWithExecuteWithGeneratedKey | execute | 0.17 | |
| servicecomb | should_convert_exception_to_response_when_decode_request_failed | onFilter | 0.00 | tie |
| TestParameterInjector | parseYamlStringToJavaType_success | parseYamlStringToJavaType | 0.86 | |
| undertow | testParametersFromOriginalPostRequest | (none) | — | see below |
| Struts | testObjectToXml | (not detected) | — | JUnit 3 |
| feign | overrideOverridingConcreteCollectionGenericFourthLevel | resolve | 0.00 | tie |
| activemq | testTransformationReceiveObject | (not detected) | — | JUnit 3 |

## Summary
- 16/20 got a focal method (one strong match, the rest weaker or flagged as ties)
- 2/20 came back with no candidates because the real call is hidden behind indirection
- 2/20 weren't picked up at all since they're JUnit 3 tests with no annotation to key on

It does well when the test calls its target directly and is named after it, like
parseYamlStringToJavaType at 0.86 or createIfNotExists at 0.67. The cases it struggles
with are below, with the tests from my set that hit each one.

## Issues

**Indirection (the real call is hidden)**: The tool only sees methods the test calls
directly. If the test gets to its target some other way, there's nothing in the AST to
grab. `undertow`'s testParametersFromOriginalPostRequest came back with no candidates
for this reason, and `dubbo`'s testChangeServiceNotExport landed on `telnet` (the
dispatch method it actually calls) instead of the handler underneath it.

**Scenario-named tests**: The whole approach assumes the test is named after the method it tests (e.g. testGetBigDecimal tests getBigDecimal). But some tests are named after the situation they check, not the method. When that happens, the test name shares no words with the real focal method, so similarity scores 0.00 even if the right method is sitting in the candidate list.

**JUnit 3 tests**: The tool spots tests by their `@Test` (or similar)
annotation. Older projects don't use annotations at all, they just name methods
`testSomething` inside a TestCase subclass. `Struts`' testObjectToXml and `activemq`'s
testTransformationReceiveObject are both like this, so neither got detected.

**Ambiguous ties** When two candidates score the same (usually
both 0, meaning nothing really matched), the tool flags it for a human rather than
picking one at random. That happened on `ormlite`'s testCallBatchTasksNestedInTransaction
(callBatchTasks vs callInTransaction), `mercury`, `servicecomb`, `feign`, and
`shardingsphere-elasticjob`. Most of these are really the indirection/naming problems
showing up as a low-confidence tie.

## Reproducing
Two steps per test file:
```
python3 focal_extract.py <TestFile.java> > candidates.json    # steps 1,2,3,5
python3 focal_method_finder_batch.py candidates.json out.json  # steps 4,6
```
`focal_extract.py` finds the project's `src/main` by walking up from the test file,
parses everything under it, and keeps only candidates the project actually defines.
If a file won't parse or has no annotated tests, it returns an empty list and logs why,
so a batch run doesn't die on one bad file.
