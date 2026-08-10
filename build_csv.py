import csv, json, os

def norm(n):
    if not n: return ""
    return str(n).split("(")[0].strip().split(".")[-1]

FILE = {
 "testIsTableExistsThrow":"RuntimeExceptionDaoTest","testQueryRawRowMapperThrow":"RuntimeExceptionDaoTest",
 "testEndThreadConnectionThrows":"RuntimeExceptionDaoTest","testCreateIfNotExistsThrow":"RuntimeExceptionDaoTest",
 "testCreateObjectInstanceThrows":"RuntimeExceptionDaoTest","testCallBatchTasksNestedInTransaction":"StatementExecutorTest",
 "testChangeServiceNotExport":"ChangeTelnetHandlerTest","testFireMultiLevelEvent":"NamingEventCoordinatorTestCase",
 "testLookupBinding":"ServiceBasedNamingStoreTestCase","assertIsShutdownAlready":"ShutdownListenerManagerTest",
 "testInitialize":"ConfigInitializerTest","of_addition":"ExtendedMarketDataTest","journalYamlTest":"PostOfficeTest",
 "assertInsertWithExecuteWithGeneratedKey":"EncryptStatementTest",
 "should_convert_exception_to_response_when_decode_request_failed":"RestServerCodecFilterTest",
 "parseYamlStringToJavaType_success":"ParameterValueParsingTest",
 "testParametersFromOriginalPostRequest":"SaveOriginalPostRequestTestCase","testObjectToXml":"JacksonXmlHandlerTest",
 "overrideOverridingConcreteCollectionGenericFourthLevel":"TypesResolveReturnTypeTest","testTransformationReceiveObject":"StompNIOTest",
}
ORDER = list(FILE.keys())

def load(path, key):
    try: d = json.load(open(path))
    except Exception: return {}
    return {e[key]: e for e in d if isinstance(e, dict) and key in e}

meta = {}
for f in ["last_10_id.csv","last_10_od.csv"]:
    for r in csv.DictReader(open(f)):
        ft = r["flaky_test"]; m = ft.split("#")[-1].split("[")[0]
        meta[m] = {"project": "/".join(r["project"].split("/")[-2:]), "sha": r["flaky_commit"],
                   "test_type": r["test_type"], "full_test": ft}

rows=[]
for t in ORDER:
    base = FILE[t]; md = meta.get(t, {})
    jac = load(f"/tmp/focal_out_{base}.json","test_name").get(t,{})
    llm = load(f"llm_{base}.json","test_name").get(t,{})
    rows.append({"project":md.get("project",""),"sha":md.get("sha",""),
                 "test_type":md.get("test_type",""),"test_name":md.get("full_test",t),
                 "jaccard_focal_method":jac.get("focal_method","") or "",
                 "llm_focal_method":norm(llm.get("llm_focal_method",""))})

with open("focal_methods.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["project","sha","test_type","test_name","jaccard_focal_method","llm_focal_method"])
    w.writeheader(); w.writerows(rows)
print("wrote",len(rows),"rows")
print(open("focal_methods.csv").read())
