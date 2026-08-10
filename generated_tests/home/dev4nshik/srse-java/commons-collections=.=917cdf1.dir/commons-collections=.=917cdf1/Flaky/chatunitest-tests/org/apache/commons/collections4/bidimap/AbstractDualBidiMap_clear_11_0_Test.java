package org.apache.commons.collections4.bidimap;

import org.apache.commons.collections4.bidimap.AbstractDualBidiMap;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.Collection;
import java.util.Iterator;
import java.util.Set;
import java.util.Objects;
import java.util.function.Predicate;
import org.apache.commons.collections4.BidiMap;
import org.apache.commons.collections4.MapIterator;
import org.apache.commons.collections4.ResettableIterator;
import org.apache.commons.collections4.collection.AbstractCollectionDecorator;
import org.apache.commons.collections4.iterators.AbstractIteratorDecorator;
import org.apache.commons.collections4.keyvalue.AbstractMapEntryDecorator;

class AbstractDualBidiMap_clear_11_0_Test {

    private AbstractDualBidiMap<String, Integer> bidiMap;

    @BeforeEach
    void setUp() throws Exception {
        Map<String, Integer> normalMap = new HashMap<>();
        Map<Integer, String> reverseMap = new HashMap<>();
        normalMap.put("one", 1);
        normalMap.put("two", 2);
        reverseMap.put(1, "one");
        reverseMap.put(2, "two");
        bidiMap = new AbstractDualBidiMap<String, Integer>(normalMap, reverseMap) {

            @Override
            protected AbstractDualBidiMap<Integer, String> createBidiMap(Map<Integer, String> normalMap, Map<String, Integer> reverseMap, BidiMap<String, Integer> inverseBidiMap) {
                // Provide a mock or a simple implementation if needed
                return null;
            }
        };
    }

    @Test
    void testClear() throws Exception {
        // Using reflection to access private fields
        Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
        Field reverseMapField = AbstractDualBidiMap.class.getDeclaredField("reverseMap");
        normalMapField.setAccessible(true);
        reverseMapField.setAccessible(true);
        // Assert that maps are initially populated
        Map<String, Integer> normalMap = (Map<String, Integer>) normalMapField.get(bidiMap);
        Map<Integer, String> reverseMap = (Map<Integer, String>) reverseMapField.get(bidiMap);
        assertEquals(2, normalMap.size());
        assertEquals(2, reverseMap.size());
        // Invoke clear method
        bidiMap.clear();
        // Assert that maps are cleared
        assertTrue(normalMap.isEmpty());
        assertTrue(reverseMap.isEmpty());
    }
}
