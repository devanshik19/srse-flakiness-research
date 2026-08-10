package com.lazerycode.jmeter.json;

import com.lazerycode.jmeter.json.TestConfiguration;
import java.util.HashMap;
import java.util.Map;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.lazerycode.jmeter.properties.ConfigurationFiles;
import com.lazerycode.jmeter.properties.PropertiesMapping;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

public class TestConfiguration_equals_15_0_Test {

    @Test
    public void testEquals_sameObject() {
        TestConfiguration config = new TestConfiguration();
        assertTrue(config.equals(config));
    }

    @Test
    public void testEquals_nullObject() {
        TestConfiguration config = new TestConfiguration();
        assertFalse(config.equals(null));
    }

    @Test
    public void testEquals_differentClass() {
        TestConfiguration config = new TestConfiguration();
        assertFalse(config.equals("A String"));
    }

    @Test
    public void testEquals_equalObjects() {
        TestConfiguration config1 = new TestConfiguration();
        TestConfiguration config2 = new TestConfiguration();
        config1.setExecutionID("123");
        config1.setJmeterDirectoryPath("/path/to/jmeter");
        config1.setResultsOutputIsCSVFormat(true);
        config1.setGenerateReports(true);
        config1.setResultFilesLocations(List.of("file1.csv", "file2.csv"));
        config2.setExecutionID("123");
        config2.setJmeterDirectoryPath("/path/to/jmeter");
        config2.setResultsOutputIsCSVFormat(true);
        config2.setGenerateReports(true);
        config2.setResultFilesLocations(List.of("file1.csv", "file2.csv"));
        assertTrue(config1.equals(config2));
    }

    @Test
    public void testEquals_nonEqualObjects() {
        TestConfiguration config1 = new TestConfiguration();
        TestConfiguration config2 = new TestConfiguration();
        config1.setExecutionID("123");
        config1.setJmeterDirectoryPath("/path/to/jmeter");
        config1.setResultsOutputIsCSVFormat(true);
        config1.setGenerateReports(true);
        config1.setResultFilesLocations(List.of("file1.csv", "file2.csv"));
        // Different executionID
        config2.setExecutionID("124");
        config2.setJmeterDirectoryPath("/path/to/jmeter");
        config2.setResultsOutputIsCSVFormat(true);
        config2.setGenerateReports(true);
        config2.setResultFilesLocations(List.of("file1.csv", "file2.csv"));
        assertFalse(config1.equals(config2));
    }

    @Test
    public void testEquals_differentResultFilesLocations() {
        TestConfiguration config1 = new TestConfiguration();
        TestConfiguration config2 = new TestConfiguration();
        config1.setExecutionID("123");
        config1.setJmeterDirectoryPath("/path/to/jmeter");
        config1.setResultsOutputIsCSVFormat(true);
        config1.setGenerateReports(true);
        config1.setResultFilesLocations(List.of("file1.csv", "file2.csv"));
        config2.setExecutionID("123");
        config2.setJmeterDirectoryPath("/path/to/jmeter");
        config2.setResultsOutputIsCSVFormat(true);
        config2.setGenerateReports(true);
        // Different files
        config2.setResultFilesLocations(List.of("file3.csv", "file4.csv"));
        assertFalse(config1.equals(config2));
    }

    @Test
    public void testEquals_differentGenerateReports() {
        TestConfiguration config1 = new TestConfiguration();
        TestConfiguration config2 = new TestConfiguration();
        config1.setExecutionID("123");
        config1.setJmeterDirectoryPath("/path/to/jmeter");
        config1.setResultsOutputIsCSVFormat(true);
        config1.setGenerateReports(true);
        config2.setExecutionID("123");
        config2.setJmeterDirectoryPath("/path/to/jmeter");
        config2.setResultsOutputIsCSVFormat(true);
        // Different generateReports
        config2.setGenerateReports(false);
        assertFalse(config1.equals(config2));
    }
}
