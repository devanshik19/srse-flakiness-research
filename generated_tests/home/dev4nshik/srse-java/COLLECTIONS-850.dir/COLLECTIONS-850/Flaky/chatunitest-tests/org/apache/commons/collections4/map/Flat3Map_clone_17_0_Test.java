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

class Flat3Map_clone_17_0_Test {

    @Test
    void testClone() throws Exception {
        // Test case 1: Cloning an empty Flat3Map
        Flat3Map<String, String> originalEmptyMap = new Flat3Map<>();
        Flat3Map<String, String> clonedEmptyMap = originalEmptyMap.clone();
        assertNotNull(clonedEmptyMap);
        assertEquals(0, getSize(clonedEmptyMap));
        // Test case 2: Cloning a Flat3Map with a few entries
        Flat3Map<String, String> originalMap = new Flat3Map<>();
        originalMap.put("key1", "value1");
        originalMap.put("key2", "value2");
        Flat3Map<String, String> clonedMap = originalMap.clone();
        assertNotNull(clonedMap);
        assertEquals(getSize(originalMap), getSize(clonedMap));
        assertEquals(originalMap.get("key1"), clonedMap.get("key1"));
        assertEquals(originalMap.get("key2"), clonedMap.get("key2"));
        // Test case 3: Cloning a Flat3Map with a delegate map
        Flat3Map<String, String> originalWithDelegate = new Flat3Map<>();
        originalWithDelegate.put("key1", "value1");
        originalWithDelegate.put("key2", "value2");
        originalWithDelegate.put("key3", "value3");
        // This should trigger delegate map usage
        originalWithDelegate.put("key4", "value4");
        Flat3Map<String, String> clonedWithDelegate = originalWithDelegate.clone();
        assertNotNull(clonedWithDelegate);
        assertEquals(getSize(originalWithDelegate), getSize(clonedWithDelegate));
        assertEquals(originalWithDelegate.get("key1"), clonedWithDelegate.get("key1"));
        assertEquals(originalWithDelegate.get("key2"), clonedWithDelegate.get("key2"));
        assertEquals(originalWithDelegate.get("key3"), clonedWithDelegate.get("key3"));
        assertEquals(originalWithDelegate.get("key4"), clonedWithDelegate.get("key4"));
        // Validate delegate map cloning
        AbstractHashedMap<String, String> originalDelegateMap = getDelegateMap(originalWithDelegate);
        AbstractHashedMap<String, String> clonedDelegateMap = getDelegateMap(clonedWithDelegate);
        if (originalDelegateMap != null) {
            assertNotSame(originalDelegateMap, clonedDelegateMap);
            assertEquals(originalDelegateMap.size(), clonedDelegateMap.size());
        }
    }

    private int getSize(Flat3Map<?, ?> map) throws Exception {
        Field sizeField = Flat3Map.class.getDeclaredField("size");
        sizeField.setAccessible(true);
        return sizeField.getInt(map);
    }

    @SuppressWarnings("unchecked")
    private AbstractHashedMap<String, String> getDelegateMap(Flat3Map<String, String> map) throws Exception {
        Field delegateMapField = Flat3Map.class.getDeclaredField("delegateMap");
        delegateMapField.setAccessible(true);
        return (AbstractHashedMap<String, String>) delegateMapField.get(map);
    }
}
