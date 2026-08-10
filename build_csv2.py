import csv, json, os, re, glob

def norm(n):
    if not n: return ""
    return str(n).split("(")[0].strip().split(".")[-1]

def llm_class(raw):
    if not raw: return ""
    raw = str(raw).split("(")[0].strip()
    parts = raw.split(".")
    return parts[-2] if len(parts) >= 2 else ""

FILE = {
 "testIsTableExistsThrow":("RuntimeExceptionDaoTest","ormlite_od"),
 "testQueryRawRowMapperThrow":("RuntimeExceptionDaoTest","ormlite_od"),
 "testEndThreadConnectionThrows":("RuntimeExceptionDaoTest","ormlite_od"),
 "testCreateIfNotExistsThrow":("RuntimeExceptionDaoTest","ormlite_od"),
 "testCreateObjectInstanceThrows":("RuntimeExceptionDaoTest","ormlite_od"),
 "testCallBatchTasksNestedInTransaction":("StatementExecutorTest","ormlite_od"),
 "testChangeServiceNotExport":("ChangeTelnetHandlerTest","focal_dubbo*"),
 "testFireMultiLevelEvent":("NamingEventCoordinatorTestCase","focal_wildfly*"),
 "testLookupBinding":("ServiceBasedNamingStoreTestCase","focal_wildfly*"),
 "assertIsShutdownAlready":("ShutdownListenerManagerTest","focal_shardingsphereelasticjob*"),
 "testInitialize":("ConfigInitializerTest","focal_skywalking*"),
 "of_addition":("ExtendedMarketDataTest","focal_Strata*"),
 "journalYamlTest":("PostOfficeTest","focal_mercury*"),
 "assertInsertWithExecuteWithGeneratedKey":("EncryptStatementTest","focal_incubator-shardingsphere*"),
 "should_convert_exception_to_response_when_decode_request_failed":("RestServerCodecFilterTest","focal_SCB*"),
 "parseYamlStringToJavaType_success":("ParameterValueParsingTest","focal_TestParameterInjector*"),
 "testParametersFromOriginalPostRequest":("SaveOriginalPostRequestTestCase","focal_undertow*"),
 "testObjectToXml":("JacksonXmlHandlerTest","focal_Struts*"),
 "overrideOverridingConcreteCollectionGenericFourthLevel":("TypesResolveReturnTypeTest","focal_feign*"),
 "testTransformationReceiveObject":("StompNIOTest","focal_activemq*"),
}
ORDER = list(FILE.keys())

def load(path, key):
    try: d = json.load(open(path))
    except Exception: return {}
    return {e[key]: e for e in d if isinstance(e, dict) and key in e}

def resolve_focal_class(test_class, focal_method, proj_glob):
    if not focal_method:
        return "", "no focal method"

    guess = re.sub(r'(TestCase|Test)$', '', test_class)
    decl = re.compile(r'\b' + re.escape(focal_method) + r'\s*\(')

    # 1. check the obvious naming-convention guess first
    for d in glob.glob(proj_glob):
        for root, _, files in os.walk(d):
            if os.sep + "main" + os.sep not in root:
                continue
            fn = guess + ".java"
            if fn in files:
                try:
                    txt = open(os.path.join(root, fn), encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                if decl.search(txt):
                    return guess, "confirmed"

    # 2. fallback: search the whole project source, but don't guess if ambiguous
    hits = set()
    for d in glob.glob(proj_glob):
        for root, _, files in os.walk(d):
            if os.sep + "main" + os.sep not in root:
                continue
            for fn in files:
                if not fn.endswith(".java"):
                    continue
                try:
                    txt = open(os.path.join(root, fn), encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                if decl.search(txt):
                    hits.add(fn[:-5])
    if len(hits) == 1:
        return next(iter(hits)), "resolved"
    if len(hits) > 1:
        return guess, "unverified (ambiguous, kept convention guess)"
    return guess, "unverified (no match found)"

meta = {}
for f in ["last_10_id.csv","last_10_od.csv"]:
    for r in csv.DictReader(open(f)):
        ft = r["flaky_test"]; m = ft.split("#")[-1].split("[")[0]
        meta[m] = {"project":"/".join(r["project"].split("/")[-2:]), "sha":r["flaky_commit"],
                   "test_type":r["test_type"], "full_test":ft}

rows=[]
for t in ORDER:
    base, proj = FILE[t]; md = meta.get(t, {})
    jac = load("/tmp/focal_out_"+base+".json","test_name").get(t,{})
    llm = load("llm_"+base+".json","test_name").get(t,{})
    jm = jac.get("focal_method","") or ""
    lm_raw = llm.get("llm_focal_method","")
    lm = norm(lm_raw)
    full = md.get("full_test", t)
    test_class = full.split("#")[0].split(".")[-1]

    method_for_lookup = jm or lm
    fc, fc_status = resolve_focal_class(test_class, method_for_lookup, proj)
    # prefer the LLM's own class if it gave one and we didn't confirm via source
    if fc_status.startswith("unverified") and "." in lm_raw:
        llm_guess = llm_class(lm_raw)
        if llm_guess:
            fc, fc_status = llm_guess, "unverified (from LLM output)"

    rows.append({"project":md.get("project",""),"sha":md.get("sha",""),
                 "test_type":md.get("test_type",""),
                 "test_class":test_class,"test_name":full,
                 "focal_class":fc,"focal_class_status":fc_status,
                 "jaccard_focal_method":jm,"llm_focal_method":lm})

with open("focal_methods.csv","w",newline="") as f:
    cols=["project","sha","test_type","test_class","test_name","focal_class","focal_class_status","jaccard_focal_method","llm_focal_method"]
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
print("wrote",len(rows),"rows")
