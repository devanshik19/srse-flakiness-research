package org.apache.commons.collections4.bidimap;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.collections4.BidiMap;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import java.util.Collection;
import java.util.Iterator;
import java.util.Objects;
import java.util.function.Predicate;
import org.apache.commons.collections4.MapIterator;
import org.apache.commons.collections4.ResettableIterator;
import org.apache.commons.collections4.collection.AbstractCollectionDecorator;
import org.apache.commons.collections4.iterators.AbstractIteratorDecorator;
import org.apache.commons.collections4.keyvalue.AbstractMapEntryDecorator;

@ExtendWith(MockitoExtension.class)
class AbstractDualBidiMap_keySet_17_0_Test {

    private AbstractDualBidiMap<String, Integer> bidiMap;

    private Map<String, Integer> normalMap;

    private Map<Integer, String> reverseMap;

    @BeforeEach
    void setUp() throws NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {
        normalMap = new HashMap<>();
        reverseMap = new HashMap<>();
        bidiMap = new AbstractDualBidiMap<String, Integer>(normalMap, reverseMap) {

            @Override
            protected BidiMap<Integer, String> createBidiMap(Map<Integer, String> normalMap, Map<String, Integer> reverseMap, BidiMap<String, Integer> inverseMap) {
                return null;
            }
        };
    }

    @Test
    void testKeySet_EmptyMap() {
        Set<String> keySet = bidiMap.keySet();
        assertNotNull(keySet);
        assertTrue(keySet.isEmpty());
    }

    @Test
    void testKeySet_SingleEntry() {
        normalMap.put("one", 1);
        reverseMap.put(1, "one");
        Set<String> keySet = bidiMap.keySet();
        assertNotNull(keySet);
        assertEquals(1, keySet.size());
        assertTrue(keySet.contains("one"));
    }

    @Test
    void testKeySet_MultipleEntries() {
        normalMap.put("one", 1);
        normalMap.put("two", 2);
        reverseMap.put(1, "one");
        reverseMap.put(2, "two");
        Set<String> keySet = bidiMap.keySet();
        assertNotNull(keySet);
        assertEquals(2, keySet.size());
        assertTrue(keySet.contains("one"));
        assertTrue(keySet.contains("two"));
    }

    @Test
    void testKeySet_NotNull() {
        normalMap.put("one", 1);
        reverseMap.put(1, "one");
        Set<String> keySet = bidiMap.keySet();
        assertNotNull(keySet);
    }

    @Test
    void testKeySet_Cache() {
        Set<String> keySet1 = bidiMap.keySet();
        Set<String> keySet2 = bidiMap.keySet();
        assertSame(keySet1, keySet2);
    }
}
