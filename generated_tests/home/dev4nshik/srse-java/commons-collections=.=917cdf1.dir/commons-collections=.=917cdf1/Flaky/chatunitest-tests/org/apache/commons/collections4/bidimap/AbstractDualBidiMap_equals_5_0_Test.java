package org.apache.commons.collections4.bidimap;

import java.util.HashMap;
import java.util.Map;
import java.lang.reflect.Field;
import org.apache.commons.collections4.bidimap.AbstractDualBidiMap;
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

class AbstractDualBidiMap_equals_5_0_Test {

    private AbstractDualBidiMap<String, Integer> bidiMap;

    @BeforeEach
    void setUp() throws Exception {
        bidiMap = new TestDualBidiMap<>();
        Map<String, Integer> normalMap = new HashMap<>();
        normalMap.put("one", 1);
        normalMap.put("two", 2);
        Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
        normalMapField.setAccessible(true);
        normalMapField.set(bidiMap, normalMap);
    }

    @Test
    void testEquals_sameObject() {
        assertTrue(bidiMap.equals(bidiMap));
    }

    @Test
    void testEquals_nullObject() {
        assertFalse(bidiMap.equals(null));
    }

    @Test
    void testEquals_differentClass() {
        assertFalse(bidiMap.equals("string"));
    }

    @Test
    void testEquals_equalMap() throws Exception {
        AbstractDualBidiMap<String, Integer> otherBidiMap = new TestDualBidiMap<>();
        Map<String, Integer> otherMap = new HashMap<>();
        otherMap.put("one", 1);
        otherMap.put("two", 2);
        Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
        normalMapField.setAccessible(true);
        normalMapField.set(otherBidiMap, otherMap);
        assertTrue(bidiMap.equals(otherBidiMap));
    }

    @Test
    void testEquals_nonEqualMap() throws Exception {
        AbstractDualBidiMap<String, Integer> otherBidiMap = new TestDualBidiMap<>();
        Map<String, Integer> otherMap = new HashMap<>();
        otherMap.put("three", 3);
        Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
        normalMapField.setAccessible(true);
        normalMapField.set(otherBidiMap, otherMap);
        assertFalse(bidiMap.equals(otherBidiMap));
    }

    // Concrete implementation for testing
    private static class TestDualBidiMap<K, V> extends AbstractDualBidiMap<K, V> {

        @Override
        protected BidiMap<V, K> createBidiMap(Map<V, K> reverseMap, Map<K, V> normalMap, BidiMap<K, V> inverseBidiMap) {
            // Not needed for equals test
            return null;
        }
    }
}
