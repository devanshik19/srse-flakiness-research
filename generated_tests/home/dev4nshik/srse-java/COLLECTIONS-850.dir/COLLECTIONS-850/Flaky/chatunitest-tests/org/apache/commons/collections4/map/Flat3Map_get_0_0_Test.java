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

public class Flat3Map_get_0_0_Test {

    private Flat3Map<String, String> flat3Map;

    @BeforeEach
    public void setUp() {
        flat3Map = new Flat3Map<>();
    }

    private void setPrivateField(String fieldName, Object value) throws Exception {
        Field field = Flat3Map.class.getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(flat3Map, value);
    }

    @Test
    public void testGetWithDelegateMap() throws Exception {
        AbstractHashedMap<String, String> delegateMap = new AbstractHashedMap<String, String>() {

            @Override
            public String get(Object key) {
                return "delegateValue";
            }
        };
        setPrivateField("delegateMap", delegateMap);
        assertEquals("delegateValue", flat3Map.get("anyKey"));
    }

    @Test
    public void testGetWithKey1() throws Exception {
        setPrivateField("size", 1);
        setPrivateField("key1", "key1");
        setPrivateField("value1", "value1");
        setPrivateField("hash1", "key1".hashCode());
        assertEquals("value1", flat3Map.get("key1"));
        assertNull(flat3Map.get("key2"));
    }

    @Test
    public void testGetWithKey2() throws Exception {
        setPrivateField("size", 2);
        setPrivateField("key1", "key1");
        setPrivateField("value1", "value1");
        setPrivateField("hash1", "key1".hashCode());
        setPrivateField("key2", "key2");
        setPrivateField("value2", "value2");
        setPrivateField("hash2", "key2".hashCode());
        assertEquals("value2", flat3Map.get("key2"));
        assertNull(flat3Map.get("key3"));
    }

    @Test
    public void testGetWithKey3() throws Exception {
        setPrivateField("size", 3);
        setPrivateField("key1", "key1");
        setPrivateField("value1", "value1");
        setPrivateField("hash1", "key1".hashCode());
        setPrivateField("key2", "key2");
        setPrivateField("value2", "value2");
        setPrivateField("hash2", "key2".hashCode());
        setPrivateField("key3", "key3");
        setPrivateField("value3", "value3");
        setPrivateField("hash3", "key3".hashCode());
        assertEquals("value3", flat3Map.get("key3"));
        assertNull(flat3Map.get("key4"));
    }

    @Test
    public void testGetWithNullKey() throws Exception {
        setPrivateField("size", 3);
        setPrivateField("key1", null);
        setPrivateField("value1", "value1");
        setPrivateField("key2", "key2");
        setPrivateField("value2", "value2");
        setPrivateField("key3", "key3");
        setPrivateField("value3", "value3");
        assertEquals("value1", flat3Map.get(null));
    }

    @Test
    public void testGetWithEmptyMap() {
        assertNull(flat3Map.get("anyKey"));
    }
}
