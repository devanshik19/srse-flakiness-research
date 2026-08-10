package com.alibaba.fastjson.util;

import java.lang.reflect.Field;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.IOException;
import java.io.Serializable;
import java.util.*;

@ExtendWith(MockitoExtension.class)
class AntiCollisionHashMap_putAll_16_0_Test {

    private AntiCollisionHashMap<String, Integer> map;

    @BeforeEach
    void setUp() {
        map = new AntiCollisionHashMap<>();
    }

    @Test
    void testPutAllWithEmptyMap() {
        Map<String, Integer> emptyMap = new HashMap<>();
        map.putAll(emptyMap);
        assertEquals(0, getSize(map));
    }

    @Test
    void testPutAllWithNonEmptyMap() {
        Map<String, Integer> nonEmptyMap = new HashMap<>();
        nonEmptyMap.put("One", 1);
        nonEmptyMap.put("Two", 2);
        map.putAll(nonEmptyMap);
        assertEquals(2, getSize(map));
        assertEquals(1, map.put("One", 1));
        assertEquals(2, map.put("Two", 2));
    }

    @Test
    void testPutAllTriggersResize() throws Exception {
        // Assuming the initial capacity is 16 and load factor is 0.75
        // Resize should trigger if adding more than 12 items
        Map<String, Integer> largeMap = new HashMap<>();
        for (int i = 0; i < 20; i++) {
            largeMap.put("Key" + i, i);
        }
        map.putAll(largeMap);
        assertEquals(20, getSize(map));
        // Use reflection to check private field `threshold`
        Field thresholdField = AntiCollisionHashMap.class.getDeclaredField("threshold");
        thresholdField.setAccessible(true);
        int threshold = (int) thresholdField.get(map);
        assertTrue(threshold >= 20);
    }

    private int getSize(AntiCollisionHashMap<String, Integer> map) {
        try {
            Field sizeField = AntiCollisionHashMap.class.getDeclaredField("size");
            sizeField.setAccessible(true);
            return sizeField.getInt(map);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
