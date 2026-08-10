package org.apache.commons.collections4.map;

import org.apache.commons.collections4.map.Flat3Map;
import org.apache.commons.collections4.map.AbstractHashedMap;
import java.lang.reflect.Field;
import java.util.Collection;
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

public class Flat3Map_values_14_0_Test {

    private Flat3Map<String, String> flat3Map;

    private AbstractHashedMap<String, String> delegateMap;

    @BeforeEach
    public void setUp() {
        flat3Map = new Flat3Map<>();
    }

    @Test
    public void testValuesWithDelegateMap() throws Exception {
        // Prepare a delegate map
        delegateMap = new AbstractHashedMap<>() {

            @Override
            public Collection<String> values() {
                return Map.of("key1", "value1", "key2", "value2").values();
            }
        };
        // Use reflection to set the delegateMap field
        Field delegateMapField = Flat3Map.class.getDeclaredField("delegateMap");
        delegateMapField.setAccessible(true);
        delegateMapField.set(flat3Map, delegateMap);
        // Test the values method
        Collection<String> values = flat3Map.values();
        assertEquals(2, values.size());
        assertTrue(values.contains("value1"));
        assertTrue(values.contains("value2"));
    }

    @Test
    public void testValuesWithoutDelegateMap() throws Exception {
        // Use reflection to set the size and values directly
        Field sizeField = Flat3Map.class.getDeclaredField("size");
        sizeField.setAccessible(true);
        sizeField.set(flat3Map, 2);
        Field value1Field = Flat3Map.class.getDeclaredField("value1");
        value1Field.setAccessible(true);
        value1Field.set(flat3Map, "value1");
        Field value2Field = Flat3Map.class.getDeclaredField("value2");
        value2Field.setAccessible(true);
        value2Field.set(flat3Map, "value2");
        // Test the values method
        Collection<String> values = flat3Map.values();
        assertEquals(2, values.size());
        assertTrue(values.contains("value1"));
        assertTrue(values.contains("value2"));
    }
}
