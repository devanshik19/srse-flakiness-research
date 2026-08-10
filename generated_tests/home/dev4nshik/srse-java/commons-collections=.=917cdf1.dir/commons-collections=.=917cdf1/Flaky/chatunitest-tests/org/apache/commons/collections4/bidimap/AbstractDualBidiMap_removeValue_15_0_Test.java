package org.apache.commons.collections4.bidimap;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import org.apache.commons.collections4.BidiMap;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.Collection;
import java.util.Iterator;
import java.util.Objects;
import java.util.function.Predicate;
import org.apache.commons.collections4.MapIterator;
import org.apache.commons.collections4.ResettableIterator;
import org.apache.commons.collections4.collection.AbstractCollectionDecorator;
import org.apache.commons.collections4.iterators.AbstractIteratorDecorator;
import org.apache.commons.collections4.keyvalue.AbstractMapEntryDecorator;

public class AbstractDualBidiMap_removeValue_15_0_Test {

    private AbstractDualBidiMap<Object, Object> bidiMap;

    private Map<Object, Object> normalMap;

    private Map<Object, Object> reverseMap;

    @BeforeEach
    public void setUp() throws Exception {
        normalMap = new HashMap<>();
        reverseMap = new HashMap<>();
        // Using reflection to instantiate the abstract class
        bidiMap = new AbstractDualBidiMap<Object, Object>(normalMap, reverseMap) {

            @Override
            protected BidiMap<Object, Object> createBidiMap(Map<Object, Object> normalMap, Map<Object, Object> reverseMap, BidiMap<Object, Object> inverseBidiMap) {
                return null;
            }
        };
        Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
        normalMapField.setAccessible(true);
        normalMapField.set(bidiMap, normalMap);
        Field reverseMapField = AbstractDualBidiMap.class.getDeclaredField("reverseMap");
        reverseMapField.setAccessible(true);
        reverseMapField.set(bidiMap, reverseMap);
    }

    @Test
    public void testRemoveValue_ValueExists() {
        Object key = "key1";
        Object value = "value1";
        normalMap.put(key, value);
        reverseMap.put(value, key);
        assertEquals(key, bidiMap.removeValue(value));
        assertFalse(normalMap.containsKey(key));
        assertFalse(reverseMap.containsKey(value));
    }

    @Test
    public void testRemoveValue_ValueDoesNotExist() {
        Object value = "nonexistent";
        assertNull(bidiMap.removeValue(value));
    }

    @Test
    public void testRemoveValue_EmptyMaps() {
        Object value = "value1";
        assertNull(bidiMap.removeValue(value));
    }
}
