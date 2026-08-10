package org.apache.commons.collections4.map;

import java.lang.reflect.Field;
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
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.Set;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.collections4.IterableMap;
import org.apache.commons.collections4.MapIterator;
import org.apache.commons.collections4.ResettableIterator;
import org.apache.commons.collections4.iterators.EmptyIterator;
import org.apache.commons.collections4.iterators.EmptyMapIterator;

public class Flat3Map_remove_9_0_Test {

    private Flat3Map<String, String> flat3Map;

    @BeforeEach
    public void setUp() {
        flat3Map = new Flat3Map<>();
    }

    @Test
    public void testRemoveFromEmptyMap() {
        assertNull(flat3Map.remove("key1"));
    }

    @Test
    public void testRemoveNullKeyFromEmptyMap() {
        assertNull(flat3Map.remove(null));
    }

    @Test
    public void testRemoveFromSingleEntryMap() throws Exception {
        setField(flat3Map, "size", 1);
        setField(flat3Map, "key1", "key1");
        setField(flat3Map, "value1", "value1");
        setField(flat3Map, "hash1", "key1".hashCode());
        assertEquals("value1", flat3Map.remove("key1"));
        assertNull(flat3Map.remove("key1"));
    }

    @Test
    public void testRemoveNullKeyFromSingleEntryMap() throws Exception {
        setField(flat3Map, "size", 1);
        setField(flat3Map, "key1", null);
        setField(flat3Map, "value1", "value1");
        setField(flat3Map, "hash1", 0);
        assertEquals("value1", flat3Map.remove(null));
        assertNull(flat3Map.remove(null));
    }

    @Test
    public void testRemoveFromTwoEntriesMap() throws Exception {
        setField(flat3Map, "size", 2);
        setField(flat3Map, "key1", "key1");
        setField(flat3Map, "value1", "value1");
        setField(flat3Map, "hash1", "key1".hashCode());
        setField(flat3Map, "key2", "key2");
        setField(flat3Map, "value2", "value2");
        setField(flat3Map, "hash2", "key2".hashCode());
        assertEquals("value2", flat3Map.remove("key2"));
        assertNull(flat3Map.remove("key2"));
    }

    @Test
    public void testRemoveNullKeyFromTwoEntriesMap() throws Exception {
        setField(flat3Map, "size", 2);
        setField(flat3Map, "key1", null);
        setField(flat3Map, "value1", "value1");
        setField(flat3Map, "hash1", 0);
        setField(flat3Map, "key2", "key2");
        setField(flat3Map, "value2", "value2");
        setField(flat3Map, "hash2", "key2".hashCode());
        assertEquals("value1", flat3Map.remove(null));
        assertNull(flat3Map.remove(null));
    }

    @Test
    public void testRemoveFromThreeEntriesMap() throws Exception {
        setField(flat3Map, "size", 3);
        setField(flat3Map, "key1", "key1");
        setField(flat3Map, "value1", "value1");
        setField(flat3Map, "hash1", "key1".hashCode());
        setField(flat3Map, "key2", "key2");
        setField(flat3Map, "value2", "value2");
        setField(flat3Map, "hash2", "key2".hashCode());
        setField(flat3Map, "key3", "key3");
        setField(flat3Map, "value3", "value3");
        setField(flat3Map, "hash3", "key3".hashCode());
        assertEquals("value3", flat3Map.remove("key3"));
        assertNull(flat3Map.remove("key3"));
    }

    private void setField(Object target, String fieldName, Object value) throws Exception {
        Field field = target.getClass().getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(target, value);
    }
}
