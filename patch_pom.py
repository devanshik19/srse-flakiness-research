import sys, os
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace('', NS)
q = lambda t: f"{{{NS}}}{t}"
path = sys.argv[1]
key  = os.environ.get("OPENAI_API_KEY", "")
tree = ET.parse(path); root = tree.getroot()
def child(parent, tag):
    e = parent.find(q(tag))
    if e is None: e = ET.SubElement(parent, q(tag))
    return e
def has(parent, artifact):
    return any(a.text and a.text.strip()==artifact for a in parent.iter(q('artifactId')))
deps = child(root, 'dependencies')
def add_dep(g,a,v,scope=None,typ=None):
    if has(deps,a): return False
    d = ET.SubElement(deps, q('dependency'))
    ET.SubElement(d,q('groupId')).text=g
    ET.SubElement(d,q('artifactId')).text=a
    ET.SubElement(d,q('version')).text=v
    if scope: ET.SubElement(d,q('scope')).text=scope
    if typ:   ET.SubElement(d,q('type')).text=typ
    return True
added=[]
if add_dep('org.junit.jupiter','junit-jupiter-engine','5.9.3',scope='test'): added.append('jupiter-engine')
if add_dep('org.junit.platform','junit-platform-launcher','1.9.3',scope='test'): added.append('platform-launcher')
if add_dep('io.github.ZJU-ACES-ISE','chatunitest-starter','1.4.0',typ='pom'): added.append('starter')
plugins = child(child(root,'build'),'plugins')
if not has(plugins,'chatunitest-maven-plugin'):
    p = ET.SubElement(plugins,q('plugin'))
    ET.SubElement(p,q('groupId')).text='io.github.zju-aces-ise'
    ET.SubElement(p,q('artifactId')).text='chatunitest-maven-plugin'
    ET.SubElement(p,q('version')).text='2.1.1'
    c = ET.SubElement(p,q('configuration'))
    ET.SubElement(c,q('apiKeys')).text=key
    ET.SubElement(c,q('model')).text='gpt-4o'
    ET.SubElement(c,q('url')).text='https://api.openai.com/v1/chat/completions'
    added.append('plugin')
tree.write(path, encoding='utf-8', xml_declaration=True)
print("pom patched:", ", ".join(added) if added else "nothing needed")

# --- force JUnit-Platform provider: surefire auto-detects JUnit4 when junit:junit is present ---
plugins2 = child(child(root, 'build'), 'plugins')
SF = None
for p in plugins2.findall(q('plugin')):
    a = p.find(q('artifactId'))
    if a is not None and a.text == 'maven-surefire-plugin':
        SF = p; break
if SF is None:
    SF = ET.SubElement(plugins2, q('plugin'))
    ET.SubElement(SF, q('groupId')).text = 'org.apache.maven.plugins'
    ET.SubElement(SF, q('artifactId')).text = 'maven-surefire-plugin'
v = SF.find(q('version'))
cur = v.text.strip() if (v is not None and v.text) else None
if cur is None or not cur.startswith('3.'):
    if v is None: v = ET.SubElement(SF, q('version'))
    v.text = '3.2.5'
sfdeps = child(SF, 'dependencies')
if not has(sfdeps, 'surefire-junit-platform'):
    dep = ET.SubElement(sfdeps, q('dependency'))
    ET.SubElement(dep, q('groupId')).text = 'org.apache.maven.surefire'
    ET.SubElement(dep, q('artifactId')).text = 'surefire-junit-platform'
    ET.SubElement(dep, q('version')).text = v.text
    print("surefire provider pinned ->", v.text)
tree.write(path, encoding='utf-8', xml_declaration=True)
