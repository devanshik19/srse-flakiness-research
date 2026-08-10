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

public class AntiCollisionHashMap_put_10_0_Test {

    private AntiCollisionHashMap<String, String> map;

    @BeforeEach
    public void setUp() {
        map = new AntiCollisionHashMap<>();
    }

    @Test
    public void testPutWithNullKey() throws Exception {
        String value = "value";
        assertNull(invokePutForNullKey(map, value));
        assertEquals(value, invokeGetForNullKey(map));
    }

    @Test
    public void testPutWithExistingKey() {
        map.put("key1", "value1");
        assertEquals("value1", map.put("key1", "value2"));
        assertEquals("value2", map.put("key1", "value3"));
    }

    @Test
    public void testPutWithNewKey() {
        assertNull(map.put("key2", "value2"));
        assertEquals("value2", map.put("key2", "value2"));
    }

    @Test
    public void testPutWithDifferentKeyTypes() {
        AntiCollisionHashMap<Object, String> mixedMap = new AntiCollisionHashMap<>();
        mixedMap.put("stringKey", "value1");
        assertNull(mixedMap.put(123, "value2"));
        assertEquals("value2", mixedMap.put(123, "value3"));
    }

    // Helper method to invoke private method putForNullKey using reflection
    private String invokePutForNullKey(AntiCollisionHashMap<String, String> map, String value) throws Exception {
        Method method = AntiCollisionHashMap.class.getDeclaredMethod("putForNullKey", Object.class);
        method.setAccessible(true);
        return (String) method.invoke(map, value);
    }

    // Helper method to invoke private method getForNullKey using reflection
    private String invokeGetForNullKey(AntiCollisionHashMap<String, String> map) throws Exception {
        Method method = AntiCollisionHashMap.class.getDeclaredMethod("getForNullKey");
        method.setAccessible(true);
        return (String) method.invoke(map);
    }
}
