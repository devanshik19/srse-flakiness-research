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

public class AntiCollisionHashMap_remove_17_0_Test {

    private AntiCollisionHashMap<String, String> map;

    @BeforeEach
    public void setUp() {
        map = new AntiCollisionHashMap<>();
    }

    @Test
    public void testRemoveExistingKey() throws Exception {
        map.put("key1", "value1");
        map.put("key2", "value2");
        String removedValue = map.remove("key1");
        assertEquals("value1", removedValue);
        assertNull(map.get("key1"));
        assertEquals("value2", map.get("key2"));
    }

    @Test
    public void testRemoveNonExistingKey() throws Exception {
        map.put("key1", "value1");
        String removedValue = map.remove("key2");
        assertNull(removedValue);
        assertEquals("value1", map.get("key1"));
    }

    @Test
    public void testRemoveNullKey() throws Exception {
        map.put(null, "value1");
        String removedValue = map.remove(null);
        assertEquals("value1", removedValue);
        assertNull(map.get(null));
    }

    @Test
    public void testRemoveFromEmptyMap() throws Exception {
        String removedValue = map.remove("key1");
        assertNull(removedValue);
    }

    @Test
    public void testRemovePrivateMethodInvocation() throws Exception {
        map.put("key1", "value1");
        Method removeEntryForKeyMethod = AntiCollisionHashMap.class.getDeclaredMethod("removeEntryForKey", Object.class);
        removeEntryForKeyMethod.setAccessible(true);
        Object entry = removeEntryForKeyMethod.invoke(map, "key1");
        assertNotNull(entry);
        String removedValue = map.remove("key1");
        assertNull(removedValue);
    }
}
