package com.networknt.schema;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.Map.Entry;
import java.util.Set;

public class CollectorContext_reset_6_0_Test {

    private CollectorContext collectorContext;

    @BeforeEach
    public void setUp() {
        collectorContext = new CollectorContext();
    }

    @Test
    public void testReset() throws NoSuchFieldException, IllegalAccessException {
        // Access the private fields using reflection
        Field collectorMapField = CollectorContext.class.getDeclaredField("collectorMap");
        Field collectorLoadMapField = CollectorContext.class.getDeclaredField("collectorLoadMap");
        collectorMapField.setAccessible(true);
        collectorLoadMapField.setAccessible(true);
        // Add some data to the maps
        Map<String, Object> testMap = new HashMap<>();
        testMap.put("key1", "value1");
        testMap.put("key2", "value2");
        collectorMapField.set(collectorContext, testMap);
        collectorLoadMapField.set(collectorContext, testMap);
        // Verify that the maps are not empty before reset
        assertFalse(((Map<?, ?>) collectorMapField.get(collectorContext)).isEmpty());
        assertFalse(((Map<?, ?>) collectorLoadMapField.get(collectorContext)).isEmpty());
        // Call the reset method
        collectorContext.reset();
        // Verify that the maps are empty after reset
        assertTrue(((Map<?, ?>) collectorMapField.get(collectorContext)).isEmpty());
        assertTrue(((Map<?, ?>) collectorLoadMapField.get(collectorContext)).isEmpty());
    }
}
