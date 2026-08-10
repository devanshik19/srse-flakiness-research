import csv, json, os, re, glob
import javalang

def norm(n):
    if not n: return ""
    return str(n).split("(")[0].strip().split(".")[-1]

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

def find_test_file(base, proj_glob):
    for d in glob.glob(proj_glob):
        for root,_,files in os.walk(d):
            if "/result/" in root: continue
            if base+".java" in files:
                return os.path.join(root, base+".java")
    return None

def receiver_type(test_file, test_method, focal_method):
    """find focal_method call in the test, return the receiver variable's type"""
    if not test_file or not focal_method: return ""
    try:
        src = open(test_file, encoding="utf-8", errors="ignore").read()
        tree = javalang.parse.parse(src)
    except Exception:
        return ""
    var_types = {}
    for _, node in tree.filter(javalang.tree.LocalVariableDeclaration):
        tn = node.type.name if node.type else None
        for d in node.declarators:
            var_types[d.name] = tn
    # also class fields
    for _, node in tree.filter(javalang.tree.FieldDeclaration):
        tn = node.type.name if node.type else None
        for d in node.declarators:
            var_types[d.name] = tn
    from collections import Counter
    hits = []
    for _, node in tree.filter(javalang.tree.MethodInvocation):
        if node.member == focal_method:
            q = node.qualifier
            if q in var_types: hits.append(var_types[q])
            elif q: hits.append(q)   # static call: qualifier is the class itself
    return Counter(hits).most_common(1)[0][0] if hits else ""

def class_path(cls, proj_glob):
    """full path (from project dir) to the .java file defining this class"""
    if not cls: return ""
    for d in glob.glob(proj_glob):
        for root,_,files in os.walk(d):
            if "/result/" in root: continue
            if os.sep+"main"+os.sep not in root: continue
            if cls+".java" in files:
                full = os.path.join(root, cls+".java")
                # strip everything up to and including the Flaky/ wrapper dir
                m = re.search(r'/Flaky/(.*)', full)
                return m.group(1) if m else full
    return ""

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
    lm = norm(llm.get("llm_focal_method",""))
    tf = find_test_file(base, proj)
    jclass = receiver_type(tf, t, jm) if jm else ""
    lclass = receiver_type(tf, t, lm) if lm else ""
    jpath = class_path(jclass, proj)
    lpath = class_path(lclass, proj)
    rows.append({"project":md.get("project",""),"sha":md.get("sha",""),
                 "test_type":md.get("test_type",""),
                 "test_class":md.get("full_test","").split("#")[0].split(".")[-1],
                 "test_name":md.get("full_test",t),
                 "jaccard_focal_method":jm,"jaccard_focal_class":jclass,"jaccard_focal_class_path":jpath,
                 "llm_focal_method":lm,"llm_focal_class":lclass,"llm_focal_class_path":lpath})

cols=["project","sha","test_type","test_class","test_name",
      "jaccard_focal_method","jaccard_focal_class","jaccard_focal_class_path",
      "llm_focal_method","llm_focal_class","llm_focal_class_path"]
with open("focal_methods.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
print("wrote",len(rows),"rows\n")
# print compact view
for r in rows:
    print(f"{r['project'][:20]:20} | {r['test_name'].split('#')[-1][:30]:30}")
    print(f"    jac: {r['jaccard_focal_method']:20} class={r['jaccard_focal_class']:20} path={r['jaccard_focal_class_path']}")
    print(f"    llm: {r['llm_focal_method']:20} class={r['llm_focal_class']:20} path={r['llm_focal_class_path']}")
