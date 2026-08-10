package com.networknt.schema;

import java.lang.reflect.Field;
import java.util.Map;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.HashMap;
import java.util.Map.Entry;
import java.util.Set;

public class CollectorContext_add_2_0_Test {

    private CollectorContext collectorContext;

    @BeforeEach
    public void setUp() {
        collectorContext = new CollectorContext();
    }

    @Test
    public void testAdd() throws NoSuchFieldException, IllegalAccessException {
        String name = "testKey";
        Object object = "testValue";
        collectorContext.add(name, object);
        // Use reflection to access the private collectorMap field
        Field collectorMapField = CollectorContext.class.getDeclaredField("collectorMap");
        collectorMapField.setAccessible(true);
        Map<String, Object> collectorMap = (Map<String, Object>) collectorMapField.get(collectorContext);
        assertNotNull(collectorMap);
        assertTrue(collectorMap.containsKey(name));
        assertEquals(object, collectorMap.get(name));
    }
}
