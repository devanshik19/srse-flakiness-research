package com.lazerycode.jmeter.json;

import com.lazerycode.jmeter.json.TestConfiguration;
import com.lazerycode.jmeter.properties.ConfigurationFiles;
import com.lazerycode.jmeter.properties.PropertiesMapping;
import java.util.HashMap;
import java.util.Map;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

public class TestConfiguration_hashCode_16_0_Test {

    @Test
    public void testHashCode() throws Exception {
        // Create a TestConfiguration instance
        TestConfiguration config = new TestConfiguration();
        // Set fields using reflection
        java.lang.reflect.Field executionIDField = TestConfiguration.class.getDeclaredField("executionID");
        executionIDField.setAccessible(true);
        executionIDField.set(config, "testExecutionID");
        java.lang.reflect.Field jmeterDirectoryPathField = TestConfiguration.class.getDeclaredField("jmeterDirectoryPath");
        jmeterDirectoryPathField.setAccessible(true);
        jmeterDirectoryPathField.set(config, "/path/to/jmeter");
        java.lang.reflect.Field resultsOutputIsCSVFormatField = TestConfiguration.class.getDeclaredField("resultsOutputIsCSVFormat");
        resultsOutputIsCSVFormatField.setAccessible(true);
        resultsOutputIsCSVFormatField.set(config, true);
        java.lang.reflect.Field generateReportsField = TestConfiguration.class.getDeclaredField("generateReports");
        generateReportsField.setAccessible(true);
        generateReportsField.set(config, false);
        java.lang.reflect.Field resultFilesLocationsField = TestConfiguration.class.getDeclaredField("resultFilesLocations");
        resultFilesLocationsField.setAccessible(true);
        resultFilesLocationsField.set(config, new String[] { "result1.csv", "result2.csv" });
        // Create a propertiesMap
        Map<ConfigurationFiles, PropertiesMapping> propertiesMap = new HashMap<>();
        java.lang.reflect.Field propertiesMapField = TestConfiguration.class.getDeclaredField("propertiesMap");
        propertiesMapField.setAccessible(true);
        propertiesMapField.set(config, propertiesMap);
        // Calculate expected hash code
        int expectedHashCode = java.util.Objects.hash("testExecutionID", "/path/to/jmeter", true, false);
        expectedHashCode = 31 * expectedHashCode + java.util.Arrays.hashCode(new String[] { "result1.csv", "result2.csv" });
        // Validate hashCode method
        assertEquals(expectedHashCode, config.hashCode());
    }
}
