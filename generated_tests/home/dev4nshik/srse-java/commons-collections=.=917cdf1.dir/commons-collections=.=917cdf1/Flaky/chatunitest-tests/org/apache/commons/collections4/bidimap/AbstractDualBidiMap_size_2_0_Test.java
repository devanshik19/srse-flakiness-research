package org.apache.commons.collections4.bidimap;

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

public class AbstractDualBidiMap_size_2_0_Test {

    private AbstractDualBidiMap<String, Integer> bidiMap;

    @BeforeEach
    public void setUp() throws Exception {
        bidiMap = new AbstractDualBidiMap<String, Integer>() {

            @Override
            protected AbstractDualBidiMap<Integer, String> createBidiMap(Map<Integer, String> reverseMap, Map<String, Integer> normalMap, BidiMap<String, Integer> inverseBidiMap) {
                return null;
            }
        };
        // Using reflection to set the private fields
        Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
        normalMapField.setAccessible(true);
        normalMapField.set(bidiMap, new HashMap<String, Integer>());
        Field reverseMapField = AbstractDualBidiMap.class.getDeclaredField("reverseMap");
        reverseMapField.setAccessible(true);
        reverseMapField.set(bidiMap, new HashMap<Integer, String>());
    }

    @Test
    public void testSizeEmpty() {
        assertEquals(0, bidiMap.size(), "Size should be 0 for an empty map");
    }

    @Test
    public void testSizeNonEmpty() throws Exception {
        Map<String, Integer> normalMap = new HashMap<>();
        normalMap.put("one", 1);
        normalMap.put("two", 2);
        // Set the normalMap field using reflection
        Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
        normalMapField.setAccessible(true);
        normalMapField.set(bidiMap, normalMap);
        assertEquals(2, bidiMap.size(), "Size should be 2 after adding two elements");
    }

    @Test
    public void testSizeAfterModification() throws Exception {
        Map<String, Integer> normalMap = new HashMap<>();
        normalMap.put("one", 1);
        // Set the normalMap field using reflection
        Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
        normalMapField.setAccessible(true);
        normalMapField.set(bidiMap, normalMap);
        assertEquals(1, bidiMap.size(), "Size should be 1 after adding one element");
        normalMap.put("two", 2);
        assertEquals(2, bidiMap.size(), "Size should be 2 after adding another element");
        normalMap.remove("one");
        assertEquals(1, bidiMap.size(), "Size should be 1 after removing one element");
    }
}
