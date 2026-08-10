package org.apache.commons.collections4.map;

import org.apache.commons.collections4.map.Flat3Map;
import org.apache.commons.collections4.map.AbstractHashedMap;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
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
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.collections4.IterableMap;
import org.apache.commons.collections4.MapIterator;
import org.apache.commons.collections4.ResettableIterator;
import org.apache.commons.collections4.iterators.EmptyIterator;
import org.apache.commons.collections4.iterators.EmptyMapIterator;

public class Flat3Map_keySet_13_0_Test {

    private Flat3Map<String, String> flat3Map;

    @BeforeEach
    public void setUp() {
        flat3Map = new Flat3Map<>();
    }

    @Test
    public void testKeySetWithDelegateMap() throws Exception {
        // Set up a delegate map using reflection
        AbstractHashedMap<String, String> delegate = new AbstractHashedMap<>() {

            @Override
            public Set<String> keySet() {
                return Set.of("key1", "key2");
            }
        };
        Field delegateMapField = Flat3Map.class.getDeclaredField("delegateMap");
        delegateMapField.setAccessible(true);
        delegateMapField.set(flat3Map, delegate);
        Set<String> keySet = flat3Map.keySet();
        assertNotNull(keySet);
        assertEquals(2, keySet.size());
        assertTrue(keySet.contains("key1"));
        assertTrue(keySet.contains("key2"));
    }

    @Test
    public void testKeySetWithoutDelegateMap() throws Exception {
        // Use reflection to set keys directly
        Field sizeField = Flat3Map.class.getDeclaredField("size");
        Field key1Field = Flat3Map.class.getDeclaredField("key1");
        Field key2Field = Flat3Map.class.getDeclaredField("key2");
        Field key3Field = Flat3Map.class.getDeclaredField("key3");
        sizeField.setAccessible(true);
        key1Field.setAccessible(true);
        key2Field.setAccessible(true);
        key3Field.setAccessible(true);
        sizeField.set(flat3Map, 3);
        key1Field.set(flat3Map, "key1");
        key2Field.set(flat3Map, "key2");
        key3Field.set(flat3Map, "key3");
        Set<String> keySet = flat3Map.keySet();
        assertNotNull(keySet);
        assertEquals(3, keySet.size());
        assertTrue(keySet.contains("key1"));
        assertTrue(keySet.contains("key2"));
        assertTrue(keySet.contains("key3"));
    }
}
