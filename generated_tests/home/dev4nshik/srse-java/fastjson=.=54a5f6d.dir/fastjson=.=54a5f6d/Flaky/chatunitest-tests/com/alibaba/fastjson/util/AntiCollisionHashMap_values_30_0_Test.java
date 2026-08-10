package com.alibaba.fastjson.util;

import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
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

public class AntiCollisionHashMap_values_30_0_Test {

    private AntiCollisionHashMap<String, String> map;

    @BeforeEach
    public void setUp() {
        map = new AntiCollisionHashMap<>();
    }

    @Test
    public void testValuesWhenEmpty() {
        Collection<String> values = map.values();
        assertNotNull(values, "Values collection should not be null");
        assertTrue(values.isEmpty(), "Values collection should be empty");
    }

    @Test
    public void testValuesWhenNotEmpty() throws NoSuchFieldException, IllegalAccessException {
        map.put("key1", "value1");
        map.put("key2", "value2");
        Collection<String> values = map.values();
        assertNotNull(values, "Values collection should not be null");
        assertEquals(2, values.size(), "Values collection should contain 2 elements");
        assertTrue(values.contains("value1"), "Values collection should contain 'value1'");
        assertTrue(values.contains("value2"), "Values collection should contain 'value2'");
        // Test if the internal 'values' field is set
        Field valuesField = AntiCollisionHashMap.class.getDeclaredField("values");
        valuesField.setAccessible(true);
        Collection<String> internalValues = (Collection<String>) valuesField.get(map);
        assertNotNull(internalValues, "Internal 'values' field should not be null");
    }

    @Test
    public void testValuesCached() {
        Collection<String> firstCall = map.values();
        Collection<String> secondCall = map.values();
        assertSame(firstCall, secondCall, "Values collection should be cached and return the same instance");
    }

    @Test
    public void testValuesAfterModification() {
        map.put("key1", "value1");
        Collection<String> values = map.values();
        map.put("key2", "value2");
        assertEquals(2, values.size(), "Values collection should reflect map modifications");
        assertTrue(values.contains("value2"), "Values collection should contain 'value2' after modification");
    }

    @Test
    public void testReflectionPrivateMethod() throws Exception {
        Method method = AntiCollisionHashMap.class.getDeclaredMethod("hashString", String.class);
        method.setAccessible(true);
        int hash = (int) method.invoke(map, "testKey");
        assertNotNull(hash, "Hash result should not be null");
    }
}
