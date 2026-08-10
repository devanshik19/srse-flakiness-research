package org.apache.commons.collections4.bidimap;

import org.apache.commons.collections4.bidimap.AbstractDualBidiMap;
import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.collections4.BidiMap;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Collection;
import java.util.Iterator;
import java.util.Set;
import java.util.Objects;
import java.util.function.Predicate;
import org.apache.commons.collections4.MapIterator;
import org.apache.commons.collections4.ResettableIterator;
import org.apache.commons.collections4.collection.AbstractCollectionDecorator;
import org.apache.commons.collections4.iterators.AbstractIteratorDecorator;
import org.apache.commons.collections4.keyvalue.AbstractMapEntryDecorator;

@ExtendWith(MockitoExtension.class)
class AbstractDualBidiMap_remove_10_0_Test {

    private AbstractDualBidiMap<String, Integer> bidiMap;

    @BeforeEach
    void setUp() {
        Map<String, Integer> normalMap = new HashMap<>();
        Map<Integer, String> reverseMap = new HashMap<>();
        bidiMap = new AbstractDualBidiMap<String, Integer>(normalMap, reverseMap) {

            @Override
            protected BidiMap<Integer, String> createBidiMap(Map<Integer, String> normalMap, Map<String, Integer> reverseMap, BidiMap<String, Integer> inverseBidiMap) {
                return null;
            }
        };
    }

    @Test
    void testRemoveExistingKey() throws Exception {
        // Use reflection to access the private fields
        Map<String, Integer> normalMap = (Map<String, Integer>) getField(bidiMap, "normalMap");
        Map<Integer, String> reverseMap = (Map<Integer, String>) getField(bidiMap, "reverseMap");
        // Add initial data
        normalMap.put("one", 1);
        reverseMap.put(1, "one");
        // Test removing an existing key
        Integer removedValue = bidiMap.remove("one");
        assertEquals(1, removedValue);
        assertFalse(normalMap.containsKey("one"));
        assertFalse(reverseMap.containsKey(1));
    }

    @Test
    void testRemoveNonExistingKey() throws Exception {
        // Use reflection to access the private fields
        Map<String, Integer> normalMap = (Map<String, Integer>) getField(bidiMap, "normalMap");
        Map<Integer, String> reverseMap = (Map<Integer, String>) getField(bidiMap, "reverseMap");
        // Add initial data
        normalMap.put("one", 1);
        reverseMap.put(1, "one");
        // Test removing a non-existing key
        Integer removedValue = bidiMap.remove("two");
        assertNull(removedValue);
        assertTrue(normalMap.containsKey("one"));
        assertTrue(reverseMap.containsKey(1));
    }

    // Helper method to access private fields using reflection
    private Object getField(Object obj, String fieldName) throws Exception {
        java.lang.reflect.Field field = obj.getClass().getSuperclass().getDeclaredField(fieldName);
        field.setAccessible(true);
        return field.get(obj);
    }
}
