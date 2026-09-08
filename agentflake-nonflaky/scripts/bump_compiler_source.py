#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET

NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(t):
    return f"{{{NS}}}{t}"

def main():
    pom_path = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) > 2 else "8"

    tree = ET.parse(pom_path)
    root = tree.getroot()

    build = root.find(tag("build"))
    if build is None:
        build = ET.SubElement(root, tag("build"))
    plugins = build.find(tag("plugins"))
    if plugins is None:
        plugins = ET.SubElement(build, tag("plugins"))

    compiler_plugin = None
    for p in plugins.findall(tag("plugin")):
        artifact_id = p.find(tag("artifactId"))
        if artifact_id is not None and artifact_id.text == "maven-compiler-plugin":
            compiler_plugin = p
            break

    if compiler_plugin is None:
        compiler_plugin = ET.SubElement(plugins, tag("plugin"))
        ET.SubElement(compiler_plugin, tag("groupId")).text = "org.apache.maven.plugins"
        ET.SubElement(compiler_plugin, tag("artifactId")).text = "maven-compiler-plugin"
        print("added maven-compiler-plugin (was missing entirely)")

    config = compiler_plugin.find(tag("configuration"))
    if config is None:
        config = ET.SubElement(compiler_plugin, tag("configuration"))

    source_el = config.find(tag("source"))
    target_el = config.find(tag("target"))
    old_source = source_el.text if source_el is not None else None
    old_target = target_el.text if target_el is not None else None

    if source_el is None:
        source_el = ET.SubElement(config, tag("source"))
    if target_el is None:
        target_el = ET.SubElement(config, tag("target"))

    source_el.text = level
    target_el.text = level

    tree.write(pom_path, xml_declaration=True, encoding="UTF-8")
    print(f"maven-compiler-plugin source/target: {old_source}/{old_target} -> {level}/{level} (permanent, not reverted)")

if __name__ == "__main__":
    main()
