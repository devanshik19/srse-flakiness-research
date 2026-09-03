import sys,xml.etree.ElementTree as ET
NS="http://maven.apache.org/POM/4.0.0";ET.register_namespace("",NS);q=lambda t:f"{{{NS}}}{t}"
p=sys.argv[1];tr=ET.parse(p);r=tr.getroot()
d=r.find(q("dependencies"))
if d is None: d=ET.SubElement(r,q("dependencies"))
def has(a): return any(x.text and x.text.strip()==a for x in d.iter(q("artifactId")))
def add(g,a,v):
    if has(a): return
    e=ET.SubElement(d,q("dependency"))
    ET.SubElement(e,q("groupId")).text=g;ET.SubElement(e,q("artifactId")).text=a
    ET.SubElement(e,q("version")).text=v;ET.SubElement(e,q("scope")).text="test"
    ex=ET.SubElement(e,q("exclusions"))
    for eg in ("org.junit.jupiter","org.junit.platform"):
        x=ET.SubElement(ex,q("exclusion"))
        ET.SubElement(x,q("groupId")).text=eg;ET.SubElement(x,q("artifactId")).text="*"
add("org.mockito","mockito-core","4.11.0")
add("org.mockito","mockito-junit-jupiter","4.11.0")
add("org.mockito","mockito-inline","4.11.0")
if not has("junit-jupiter"):
    e=ET.SubElement(d,q("dependency"));ET.SubElement(e,q("groupId")).text="org.junit.jupiter";ET.SubElement(e,q("artifactId")).text="junit-jupiter";ET.SubElement(e,q("version")).text="5.9.3";ET.SubElement(e,q("scope")).text="test"
tr.write(p,encoding="utf-8",xml_declaration=True);print("pom: pristine + mockito + junit-jupiter 5.9.3")
