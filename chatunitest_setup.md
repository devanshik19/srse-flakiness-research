# ChatUniTest generation setup

## Plugin

Only version 2.1.1 resolves on Maven Central. 2.0.0 and 2.1.0 fail (missing chatunitest-core jar).

## Per-project setup, before generating

1. Set JAVA_HOME to the JDK the project needs (check the CSV's java column).
```bash
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64   # or java-11, java-17
```

2. Build the project so ChatUniTest has a compiled jar to work against.
```bash
mvn install -DskipTests -Dcheckstyle.skip=true -Drat.skip=true -Dmaven.javadoc.skip=true -Denforcer.skip=true
```

3. Add JUnit 5 and Mockito as test dependencies if the project doesn't already have them (ChatUniTest's generated tests use both, even on JUnit 4 projects). In the module's `pom.xml`, inside `<dependencies>`:
```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-api</artifactId>
    <version>5.9.3</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-engine</artifactId>
    <version>5.9.3</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <version>4.11.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-junit-jupiter</artifactId>
    <version>4.11.0</version>
    <scope>test</scope>
</dependency>
```

## Generate a test for one focal method

```bash
mvn io.github.zju-aces-ise:chatunitest-maven-plugin:2.1.1:method \
  -DselectMethod="fully.qualified.ClassName#methodName" \
  -DapiKeys="$OPENAI_API_KEY" \
  -Durl=https://api.openai.com/v1/chat/completions \
  -Dmodel=gpt-4o-mini \
  -Dcheckstyle.skip=true 2>&1 | tee gen_logs/gen_<project>_<method>.log
```

Output lands in `<module>/chatunitest-tests/`. It doesn't reliably stop after the first passing candidate, so watch the log for `compile and execute successfully` or `generated successfully`, take that candidate, and Ctrl-C if it keeps looping.

## Stage the generated test and confirm it actually passes

```bash
mkdir -p src/test/java/path/to/package
cp chatunitest-tests/path/to/package/ClassName_method_N_N_Test.java src/test/java/path/to/package/
mvn test -Dtest="ClassName_method_N_N_Test" -Dcheckstyle.skip=true -Denforcer.skip=true -DfailIfNoTests=false
```
