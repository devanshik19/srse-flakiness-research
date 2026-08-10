package com.alibaba.fastjson.util;

import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.IOException;
import java.io.Serializable;
import java.util.*;

public class AntiCollisionHashMap_clone_23_0_Test {

    @Test
    public void testClone() throws Exception {
        // Create an instance of AntiCollisionHashMap
        AntiCollisionHashMap<String, String> originalMap = new AntiCollisionHashMap<>();
        originalMap.put("key1", "value1");
        originalMap.put("key2", "value2");
        // Use reflection to invoke the private init method
        Method initMethod = AntiCollisionHashMap.class.getDeclaredMethod("init");
        initMethod.setAccessible(true);
        initMethod.invoke(originalMap);
        // Clone the map
        AntiCollisionHashMap<String, String> clonedMap = (AntiCollisionHashMap<String, String>) originalMap.clone();
        // Assert that the cloned map is not the same instance as the original
        assertNotSame(originalMap, clonedMap);
        // Assert that the cloned map has the same size as the original
        assertEquals(originalMap.size(), clonedMap.size());
        // Assert that the cloned map contains the same entries as the original
        for (Map.Entry<String, String> entry : originalMap.entrySet()) {
            assertTrue(clonedMap.containsKey(entry.getKey()));
            assertEquals(entry.getValue(), clonedMap.get(entry.getKey()));
        }
        // Assert that the internal state of the cloned map is correctly initialized
        assertNotNull(clonedMap.table);
        assertEquals(0, clonedMap.modCount);
        assertEquals(0, clonedMap.size);
    }
}
