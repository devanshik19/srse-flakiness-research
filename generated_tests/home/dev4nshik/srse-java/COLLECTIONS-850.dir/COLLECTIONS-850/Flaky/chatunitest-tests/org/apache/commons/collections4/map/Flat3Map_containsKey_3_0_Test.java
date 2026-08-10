package org.apache.commons.collections4.map;

import org.apache.commons.collections4.map.Flat3Map;
import org.apache.commons.collections4.map.AbstractHashedMap;
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

class Flat3Map_containsKey_3_0_Test {

    private Flat3Map<String, String> flat3Map;

    @BeforeEach
    void setUp() {
        flat3Map = new Flat3Map<>();
    }

    @Test
    void testContainsKeyWithDelegateMap() throws Exception {
        AbstractHashedMap<String, String> delegateMap = mock(AbstractHashedMap.class);
        when(delegateMap.containsKey("key1")).thenReturn(true);
        setPrivateField(flat3Map, "delegateMap", delegateMap);
        assertTrue(flat3Map.containsKey("key1"));
        verify(delegateMap).containsKey("key1");
    }

    @Test
    void testContainsKeyWithNullKey() throws Exception {
        setPrivateField(flat3Map, "size", 3);
        setPrivateField(flat3Map, "key1", null);
        setPrivateField(flat3Map, "key2", "key2");
        setPrivateField(flat3Map, "key3", "key3");
        assertTrue(flat3Map.containsKey(null));
        setPrivateField(flat3Map, "key1", "key1");
        setPrivateField(flat3Map, "key2", null);
        assertTrue(flat3Map.containsKey(null));
        setPrivateField(flat3Map, "key2", "key2");
        setPrivateField(flat3Map, "key3", null);
        assertTrue(flat3Map.containsKey(null));
        setPrivateField(flat3Map, "key3", "key3");
        assertFalse(flat3Map.containsKey(null));
    }

    @Test
    void testContainsKeyWithNonNullKey() throws Exception {
        setPrivateField(flat3Map, "size", 3);
        setPrivateField(flat3Map, "key1", "key1");
        setPrivateField(flat3Map, "key2", "key2");
        setPrivateField(flat3Map, "key3", "key3");
        setPrivateField(flat3Map, "hash1", "key1".hashCode());
        setPrivateField(flat3Map, "hash2", "key2".hashCode());
        setPrivateField(flat3Map, "hash3", "key3".hashCode());
        assertTrue(flat3Map.containsKey("key1"));
        assertTrue(flat3Map.containsKey("key2"));
        assertTrue(flat3Map.containsKey("key3"));
        assertFalse(flat3Map.containsKey("key4"));
    }

    @Test
    void testContainsKeyWithEmptyMap() {
        assertFalse(flat3Map.containsKey("key1"));
    }

    private void setPrivateField(Object target, String fieldName, Object value) throws Exception {
        Field field = Flat3Map.class.getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(target, value);
    }
}
