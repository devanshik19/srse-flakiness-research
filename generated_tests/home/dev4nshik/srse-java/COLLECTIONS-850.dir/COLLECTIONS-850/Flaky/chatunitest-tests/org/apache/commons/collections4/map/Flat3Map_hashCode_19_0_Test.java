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

public class Flat3Map_hashCode_19_0_Test {

    private Flat3Map<String, String> flat3Map;

    @BeforeEach
    public void setUp() {
        flat3Map = new Flat3Map<>();
    }

    @Test
    public void testHashCodeWithDelegateMap() throws Exception {
        AbstractHashedMap<String, String> delegateMap = new AbstractHashedMap<String, String>() {

            @Override
            public int hashCode() {
                return 42;
            }
        };
        setPrivateField(flat3Map, "delegateMap", delegateMap);
        assertEquals(42, flat3Map.hashCode());
    }

    @Test
    public void testHashCodeWithSizeZero() throws Exception {
        setPrivateField(flat3Map, "size", 0);
        assertEquals(0, flat3Map.hashCode());
    }

    @Test
    public void testHashCodeWithSizeOne() throws Exception {
        setPrivateField(flat3Map, "size", 1);
        setPrivateField(flat3Map, "hash1", 10);
        setPrivateField(flat3Map, "value1", "value1");
        assertEquals(10 ^ "value1".hashCode(), flat3Map.hashCode());
    }

    @Test
    public void testHashCodeWithSizeTwo() throws Exception {
        setPrivateField(flat3Map, "size", 2);
        setPrivateField(flat3Map, "hash1", 10);
        setPrivateField(flat3Map, "value1", "value1");
        setPrivateField(flat3Map, "hash2", 20);
        setPrivateField(flat3Map, "value2", "value2");
        assertEquals((10 ^ "value1".hashCode()) + (20 ^ "value2".hashCode()), flat3Map.hashCode());
    }

    @Test
    public void testHashCodeWithSizeThree() throws Exception {
        setPrivateField(flat3Map, "size", 3);
        setPrivateField(flat3Map, "hash1", 10);
        setPrivateField(flat3Map, "value1", "value1");
        setPrivateField(flat3Map, "hash2", 20);
        setPrivateField(flat3Map, "value2", "value2");
        setPrivateField(flat3Map, "hash3", 30);
        setPrivateField(flat3Map, "value3", "value3");
        assertEquals((10 ^ "value1".hashCode()) + (20 ^ "value2".hashCode()) + (30 ^ "value3".hashCode()), flat3Map.hashCode());
    }

    @Test
    public void testHashCodeWithInvalidSize() throws Exception {
        setPrivateField(flat3Map, "size", 4);
        assertThrows(IllegalStateException.class, () -> flat3Map.hashCode());
    }

    private void setPrivateField(Object object, String fieldName, Object value) throws Exception {
        Field field = object.getClass().getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(object, value);
    }
}
