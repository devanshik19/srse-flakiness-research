package org.apache.commons.collections4.bidimap;

import org.apache.commons.collections4.BidiMap;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
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

class AbstractDualBidiMap_values_19_0_Test {

    private AbstractDualBidiMap<String, Integer> bidiMap;

    private Map<String, Integer> normalMap;

    private Map<Integer, String> reverseMap;

    @BeforeEach
    void setUp() throws Exception {
        normalMap = new HashMap<>();
        reverseMap = new HashMap<>();
        // Use a subclass to instantiate the abstract class
        bidiMap = new AbstractDualBidiMap<String, Integer>(normalMap, reverseMap) {

            @Override
            protected BidiMap<Integer, String> createBidiMap(Map<Integer, String> normalMap, Map<String, Integer> reverseMap, BidiMap<String, Integer> inverseMap) {
                return null;
            }
        };
    }

    @Test
    void testValues() {
        Set<Integer> values = bidiMap.values();
        assertNotNull(values);
        assertTrue(values.isEmpty());
        normalMap.put("One", 1);
        normalMap.put("Two", 2);
        reverseMap.put(1, "One");
        reverseMap.put(2, "Two");
        values = bidiMap.values();
        assertEquals(2, values.size());
        assertTrue(values.contains(1));
        assertTrue(values.contains(2));
    }
}
