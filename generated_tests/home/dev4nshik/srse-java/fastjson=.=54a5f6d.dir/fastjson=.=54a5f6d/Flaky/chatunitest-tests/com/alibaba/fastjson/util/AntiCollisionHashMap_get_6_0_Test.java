package com.alibaba.fastjson.util;

import java.lang.reflect.Field;
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

public class AntiCollisionHashMap_get_6_0_Test {

    private AntiCollisionHashMap<String, String> map;

    @BeforeEach
    public void setUp() {
        map = new AntiCollisionHashMap<>();
    }

    @Test
    public void testGetForNullKey() throws Exception {
        // Use reflection to access the private method getForNullKey
        Method getForNullKeyMethod = AntiCollisionHashMap.class.getDeclaredMethod("getForNullKey");
        getForNullKeyMethod.setAccessible(true);
        // Initially, the map is empty, so getForNullKey should return null
        assertNull(getForNullKeyMethod.invoke(map));
        // Add a null key to the map
        addEntryToTable(null, "NullValue", 0);
        // Now, getForNullKey should return the value associated with the null key
        assertEquals("NullValue", getForNullKeyMethod.invoke(map));
    }

    @Test
    public void testGetWithStringKey() throws Exception {
        // Prepare the map with a string key
        addEntryToTable("key1", "value1", hashString("key1"));
        // Test get method with an existing key
        assertEquals("value1", map.get("key1"));
        // Test get method with a non-existing key
        assertNull(map.get("key2"));
    }

    @Test
    public void testGetWithNonStringKey() throws Exception {
        // Prepare the map with an integer key
        addEntryToTable(123, "value123", hash(123));
        // Test get method with an existing key
        assertEquals("value123", map.get(123));
        // Test get method with a non-existing key
        assertNull(map.get(456));
    }

    // Helper method to add entries to the map's table using reflection
    private void addEntryToTable(Object key, String value, int hash) {
        try {
            Field tableField = AntiCollisionHashMap.class.getDeclaredField("table");
            tableField.setAccessible(true);
            Map.Entry<?, ?>[] table = (Map.Entry<?, ?>[]) tableField.get(map);
            int index = indexFor(hash, table.length);
            // Create a new entry and add it to the table
            Entry newEntry = new Entry(hash, key, value, (Entry) table[index]);
            table[index] = newEntry;
            // Update the size field
            Field sizeField = AntiCollisionHashMap.class.getDeclaredField("size");
            sizeField.setAccessible(true);
            sizeField.setInt(map, sizeField.getInt(map) + 1);
        } catch (Exception e) {
            fail("Failed to add entry to table: " + e.getMessage());
        }
    }

    // Helper method to calculate hash for a string using reflection
    private int hashString(String key) throws Exception {
        Method hashStringMethod = AntiCollisionHashMap.class.getDeclaredMethod("hashString", String.class);
        hashStringMethod.setAccessible(true);
        return (int) hashStringMethod.invoke(map, key);
    }

    // Helper method to calculate hash for an integer using reflection
    private int hash(int h) throws Exception {
        Method hashMethod = AntiCollisionHashMap.class.getDeclaredMethod("hash", int.class);
        hashMethod.setAccessible(true);
        return (int) hashMethod.invoke(null, h);
    }

    // Helper method to calculate index for a hash using reflection
    private int indexFor(int h, int length) throws Exception {
        Method indexForMethod = AntiCollisionHashMap.class.getDeclaredMethod("indexFor", int.class, int.class);
        indexForMethod.setAccessible(true);
        return (int) indexForMethod.invoke(null, h, length);
    }

    // Inner class to simulate the Entry<K, V> class in the AntiCollisionHashMap
    private static class Entry implements Map.Entry<Object, Object> {

        final int hash;

        final Object key;

        Object value;

        Entry next;

        Entry(int hash, Object key, Object value, Entry next) {
            this.hash = hash;
            this.key = key;
            this.value = value;
            this.next = next;
        }

        public Object getKey() {
            return key;
        }

        public Object getValue() {
            return value;
        }

        public Object setValue(Object newValue) {
            Object oldValue = value;
            value = newValue;
            return oldValue;
        }
    }
}
