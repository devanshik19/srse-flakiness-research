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

class CollectorContext_add_1_0_Test {

    private CollectorContext collectorContext;

    @BeforeEach
    void setUp() {
        collectorContext = new CollectorContext();
    }

    @Test
    void testAdd() throws NoSuchFieldException, IllegalAccessException {
        // Arrange
        String name = "testCollector";
        Collector<String> collector = new Collector<>();
        // Act
        collectorContext.add(name, collector);
        // Assert
        Field collectorMapField = CollectorContext.class.getDeclaredField("collectorMap");
        collectorMapField.setAccessible(true);
        Map<String, Object> collectorMap = (Map<String, Object>) collectorMapField.get(collectorContext);
        assertEquals(1, collectorMap.size());
        assertEquals(collector, collectorMap.get(name));
    }

    // A simple Collector class for testing purposes
    static class Collector<E> {
        // Add necessary methods or fields if required
    }
}
