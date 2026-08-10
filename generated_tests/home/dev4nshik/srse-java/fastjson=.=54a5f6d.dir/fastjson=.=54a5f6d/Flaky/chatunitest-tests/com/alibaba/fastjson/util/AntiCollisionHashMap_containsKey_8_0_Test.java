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

public class AntiCollisionHashMap_containsKey_8_0_Test {

    private AntiCollisionHashMap<String, String> map;

    @BeforeEach
    public void setUp() {
        map = new AntiCollisionHashMap<>();
    }

    @Test
    public void testContainsKeyWithExistingKey() throws Exception {
        // Using reflection to access private method
        Method putMethod = AntiCollisionHashMap.class.getDeclaredMethod("putForCreate", Object.class, Object.class);
        putMethod.setAccessible(true);
        putMethod.invoke(map, "key1", "value1");
        assertTrue(map.containsKey("key1"));
    }

    @Test
    public void testContainsKeyWithNonExistingKey() {
        assertFalse(map.containsKey("key2"));
    }

    @Test
    public void testContainsKeyWithNullKey() throws Exception {
        // Using reflection to access private method
        Method putMethod = AntiCollisionHashMap.class.getDeclaredMethod("putForCreate", Object.class, Object.class);
        putMethod.setAccessible(true);
        putMethod.invoke(map, null, "valueForNullKey");
        assertTrue(map.containsKey(null));
    }

    @Test
    public void testContainsKeyWithEmptyMap() {
        assertFalse(map.containsKey("anyKey"));
    }

    @Test
    public void testContainsKeyWithCollision() throws Exception {
        // Assuming hash collision scenario
        Method putMethod = AntiCollisionHashMap.class.getDeclaredMethod("putForCreate", Object.class, Object.class);
        putMethod.setAccessible(true);
        putMethod.invoke(map, "key1", "value1");
        // Assume key1 and key2 produce same hash
        putMethod.invoke(map, "key2", "value2");
        assertTrue(map.containsKey("key1"));
        assertTrue(map.containsKey("key2"));
    }
}
