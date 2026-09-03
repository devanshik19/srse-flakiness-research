import sys, xml.etree.ElementTree as ET
NS="http://maven.apache.org/POM/4.0.0"; ET.register_namespace('',NS); q=lambda t:f"{{{NS}}}{t}"
path=sys.argv[1]; tree=ET.parse(path); root=tree.getroot()
def child(p,t):
    e=p.find(q(t))
    if e is None: e=ET.SubElement(p,q(t))
    return e
def has(p,a): return any(x.text and x.text.strip()==a for x in p.iter(q('artifactId')))
deps=child(root,'dependencies'); added=[]
WANT=[('org.mockito','mockito-core','4.11.0'),
      ('org.mockito','mockito-junit-jupiter','4.11.0'),
      ('org.junit.jupiter','junit-jupiter-api','5.9.1'),
      ('org.junit.jupiter','junit-jupiter-engine','5.9.1'),
      ('org.junit.vintage','junit-vintage-engine','5.9.1'),
      ('org.junit.platform','junit-platform-launcher','1.9.1'),
      ('org.junit.platform','junit-platform-engine','1.9.1'),
      ('org.junit.platform','junit-platform-commons','1.9.1')]
for g,a,v in WANT:
    if has(deps,a): continue
    d=ET.SubElement(deps,q('dependency'))
    ET.SubElement(d,q('groupId')).text=g; ET.SubElement(d,q('artifactId')).text=a
    ET.SubElement(d,q('version')).text=v; ET.SubElement(d,q('scope')).text='test'
    added.append(a)
tree.write(path,encoding='utf-8',xml_declaration=True)
print("ensure_deps added:", ", ".join(added) if added else "nothing (all present)")
