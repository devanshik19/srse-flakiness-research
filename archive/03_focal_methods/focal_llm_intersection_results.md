# Focal Method Finder — LLM Approach + Intersection 

The Jaccard approach picks the focal method by name-token overlap. This second approach
asks an LLM -> feed it the test name and full test body, have it return the method
calls with a probability score each, and take the highest. Then, following the UTFix paper,
the two approaches are intersected. A focal method only counts as confirmed when both the
Jaccard method and the LLM independently land on the same method. Anything else is treated
as an unresolved case.

Model used: gpt-4o. Same 20 tests as before (10 ID, 10 OD).

## Results

| Project | Test | Jaccard | LLM | Result |
|---------|------|---------|-----|--------|
| ormlite-core | testIsTableExistsThrow | isTableExists | isTableExists | confirmed |
| ormlite-core | testQueryRawRowMapperThrow | queryRaw | queryRaw | confirmed |
| ormlite-core | testEndThreadConnectionThrows | endThreadConnection | endThreadConnection | confirmed |
| ormlite-core | testCreateIfNotExistsThrow | createIfNotExists | createIfNotExists | confirmed |
| ormlite-core | testCreateObjectInstanceThrows | createObjectInstance | createObjectInstance | confirmed |
| ormlite-core | testCallBatchTasksNestedInTransaction | callInTransaction | callBatchTasks | disagree |
| dubbo | testChangeServiceNotExport | telnet | telnet | confirmed |
| wildfly | testFireMultiLevelEvent | fireEvent | fireEvent | confirmed |
| wildfly | testLookupBinding | lookup | lookup | confirmed |
| shardingsphere-elasticjob | assertRemoveLocalInstancePath | getInstance | dataChanged | disagree |
| skywalking | testInitialize | initialize | initialize | confirmed |
| Strata | of_addition | of | of | confirmed |
| mercury | journalYamlTest | getInstance | getJournaledRoutes | disagree |
| shardingsphere | assertInsertWithExecuteWithGeneratedKey | execute | getEncryptConnection | disagree |
| servicecomb | should_convert_exception_to_response_when_decode_request_failed | onFilter | onFilter | confirmed |
| TestParameterInjector | parseYamlStringToJavaType_success | parseYamlStringToJavaType | (none) | jaccard only |
| undertow | testParametersFromOriginalPostRequest | (none) | executePostRequest | llm only |
| Struts | testObjectToXml | (not detected) | (not detected) | JUnit 3 |
| feign | overrideOverridingConcreteCollectionGenericFourthLevel | resolve | resolve | confirmed |
| activemq | testTransformationReceiveObject | (not detected) | (not detected) | JUnit 3 |

## Summary
- 12/20 confirmed by both approaches
- 4/20 disagree (each approach picked a different method)
- 2/20 found by only one approach
- 2/20 not detected by either (JUnit 3 tests, no annotation to key on)

## What the two approaches together actually gave us

The LLM confirmed several cases where Jaccard scored 0. dubbo's testChangeServiceNotExport
is the clearest one. Jaccard couldn't match it because the test is named after the scenario (not the method), so it scored 0 even though `telnet` was in the candidate list. The LLM read
the test body and picked `telnet` on its own, so the two now agree and it's a confirmed
focal method. servicecomb's onFilter is the same story.

For testCallBatchTasksNestedInTransaction, Jaccard's tie-breaker chose callInTransaction but the
LLM chose callBatchTasks, and the LLM is probably right since the test is named after
callBatchTasks. So the disagreement is flagging a case where Jaccard's tie-break
went the wrong way.

The two one-sided cases, undertow's
testParametersFromOriginalPostRequest, Jaccard found nothing because the real call is reached
through indirection the AST can't follow, but the LLM read the intent and suggested
executePostRequest. Since only one side found it, it doesn't count as confirmed, but it shows
the LLM can see through indirection that name-matching can't. The reverse happened on
parseYamlStringToJavaType, where Jaccard was confident (0.86) but the LLM returned nothing.

The two JUnit 3 tests (Struts, activemq) are still not detected by either approach, since
both rely on finding annotated test methods and these old-style tests have no annotations.

## Reproducing
```
python3 llm_focal.py <TestFile.java> -o llm_out.json          # LLM approach
python3 intersect_focal.py jaccard_out.json llm_out.json final.json   # intersection
```
llm_focal.py extracts each @Test method's name and body, prompts the model for candidate
methods with probabilities, and takes the highest. Replies are cached so re-runs don't repeat
API calls. intersect_focal.py compares the two on the bare method name (the LLM often returns
Class.method, so the class prefix is stripped before comparing) and marks a focal method
confirmed only when both agree.
