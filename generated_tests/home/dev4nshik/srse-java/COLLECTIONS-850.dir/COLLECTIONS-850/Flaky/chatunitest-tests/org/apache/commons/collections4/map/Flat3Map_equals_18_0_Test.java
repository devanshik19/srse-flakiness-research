package org.apache.commons.collections4.map;

import org.apache.commons.collections4.map.Flat3Map;
import org.apache.commons.collections4.map.AbstractHashedMap;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.AbstractCollection;
import java.util.AbstractSet;
import java.util.Collection;
import java.util.Iterator;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.Set;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.collections4.IterableMap;
import org.apache.commons.collections4.MapIterator;
import org.apache.commons.collections4.ResettableIterator;
import org.apache.commons.collections4.iterators.EmptyIterator;
import org.apache.commons.collections4.iterators.EmptyMapIterator;

public class Flat3Map_equals_18_0_Test {

    private Flat3Map<String, String> flat3Map;

    @BeforeEach
    public void setUp() {
        flat3Map = new Flat3Map<>();
    }

    @Test
    public void testEquals_SameInstance() {
        assertTrue(flat3Map.equals(flat3Map));
    }

    @Test
    public void testEquals_DifferentType() {
        assertFalse(flat3Map.equals("someString"));
    }

    @Test
    public void testEquals_EmptyMaps() {
        Map<String, String> otherMap = new HashMap<>();
        assertTrue(flat3Map.equals(otherMap));
    }

    @Test
    public void testEquals_NonEmptyMapsWithSameEntries() throws Exception {
        setPrivateField(flat3Map, "size", 1);
        setPrivateField(flat3Map, "key1", "key1");
        setPrivateField(flat3Map, "value1", "value1");
        Map<String, String> otherMap = new HashMap<>();
        otherMap.put("key1", "value1");
        assertTrue(flat3Map.equals(otherMap));
    }

    @Test
    public void testEquals_NonEmptyMapsWithDifferentSizes() throws Exception {
        setPrivateField(flat3Map, "size", 1);
        setPrivateField(flat3Map, "key1", "key1");
        setPrivateField(flat3Map, "value1", "value1");
        Map<String, String> otherMap = new HashMap<>();
        otherMap.put("key1", "value1");
        otherMap.put("key2", "value2");
        assertFalse(flat3Map.equals(otherMap));
    }

    @Test
    public void testEquals_NonEmptyMapsWithDifferentEntries() throws Exception {
        setPrivateField(flat3Map, "size", 1);
        setPrivateField(flat3Map, "key1", "key1");
        setPrivateField(flat3Map, "value1", "value1");
        Map<String, String> otherMap = new HashMap<>();
        otherMap.put("key1", "differentValue");
        assertFalse(flat3Map.equals(otherMap));
    }

    @Test
    public void testEquals_WithDelegateMap() throws Exception {
        AbstractHashedMap<String, String> delegateMap = new AbstractHashedMap<>() {

            @Override
            public boolean equals(Object obj) {
                return obj instanceof Map && ((Map<?, ?>) obj).size() == 0;
            }
        };
        setPrivateField(flat3Map, "delegateMap", delegateMap);
        Map<String, String> otherMap = new HashMap<>();
        assertTrue(flat3Map.equals(otherMap));
    }

    private void setPrivateField(Object target, String fieldName, Object value) throws Exception {
        Field field = Flat3Map.class.getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(target, value);
    }
}
