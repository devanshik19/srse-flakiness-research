#!/usr/bin/env python3
"""bump_surefire.py <pom.xml> <version> -- set/override maven-surefire-plugin's
<version> in <build><plugins>. Used only as a temporary, always-reverted workaround
for tools (like NonDex) that resolve the surefire version from the pom itself and
offer no CLI override to force a newer one. Idempotent: if a plugin entry already
exists, updates its version; otherwise creates one."""
import sys
import xml.etree.ElementTree as ET

NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace('', NS)
q = lambda t: f"{{{NS}}}{t}"

path, version = sys.argv[1], sys.argv[2]
tree = ET.parse(path)
root = tree.getroot()

def child(parent, tag):
    e = parent.find(q(tag))
    if e is None:
        e = ET.SubElement(parent, q(tag))
    return e

build = child(root, 'build')
plugins = child(build, 'plugins')

sf = None
for p in plugins.findall(q('plugin')):
    a = p.find(q('artifactId'))
    if a is not None and a.text == 'maven-surefire-plugin':
        sf = p
        break

if sf is None:
    sf = ET.SubElement(plugins, q('plugin'))
    ET.SubElement(sf, q('groupId')).text = 'org.apache.maven.plugins'
    ET.SubElement(sf, q('artifactId')).text = 'maven-surefire-plugin'
    v = ET.SubElement(sf, q('version'))
    v.text = version
    print(f"added maven-surefire-plugin {version}")
else:
    v = sf.find(q('version'))
    old = v.text if v is not None else None
    if v is None:
        v = ET.SubElement(sf, q('version'))
    v.text = version
    print(f"bumped maven-surefire-plugin {old} -> {version}")

tree.write(path, encoding='utf-8', xml_declaration=True)
