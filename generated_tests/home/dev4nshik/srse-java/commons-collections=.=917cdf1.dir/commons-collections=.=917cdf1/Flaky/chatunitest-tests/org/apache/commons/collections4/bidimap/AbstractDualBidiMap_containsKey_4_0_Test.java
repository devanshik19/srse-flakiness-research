package org.apache.commons.collections4.bidimap;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import org.apache.commons.collections4.BidiMap;
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
import org.apache.commons.collections4.MapIterator;
import org.apache.commons.collections4.ResettableIterator;
import org.apache.commons.collections4.collection.AbstractCollectionDecorator;
import org.apache.commons.collections4.iterators.AbstractIteratorDecorator;
import org.apache.commons.collections4.keyvalue.AbstractMapEntryDecorator;

public class AbstractDualBidiMap_containsKey_4_0_Test {

    private AbstractDualBidiMap<String, Integer> bidiMap;

    @BeforeEach
    public void setUp() throws Exception {
        // Create a subclass of AbstractDualBidiMap to instantiate
        bidiMap = new AbstractDualBidiMap<String, Integer>(new HashMap<>(), new HashMap<>()) {

            @Override
            protected BidiMap<Integer, String> createBidiMap(Map<Integer, String> normalMap, Map<String, Integer> reverseMap, BidiMap<String, Integer> inverseBidiMap) {
                // Implement this method as per requirement
                return null;
            }
        };
    }

    @Test
    public void testContainsKeyWhenKeyExists() {
        try {
            Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
            normalMapField.setAccessible(true);
            Map<String, Integer> normalMap = new HashMap<>();
            normalMap.put("key1", 1);
            normalMapField.set(bidiMap, normalMap);
        } catch (Exception e) {
            fail("Failed to set up normalMap field: " + e.getMessage());
        }
        assertTrue(bidiMap.containsKey("key1"));
    }

    @Test
    public void testContainsKeyWhenKeyDoesNotExist() {
        try {
            Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
            normalMapField.setAccessible(true);
            Map<String, Integer> normalMap = new HashMap<>();
            normalMapField.set(bidiMap, normalMap);
        } catch (Exception e) {
            fail("Failed to set up normalMap field: " + e.getMessage());
        }
        assertFalse(bidiMap.containsKey("key2"));
    }

    @Test
    public void testContainsKeyWithNullKey() {
        try {
            Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
            normalMapField.setAccessible(true);
            Map<String, Integer> normalMap = new HashMap<>();
            normalMap.put("key1", 1);
            normalMapField.set(bidiMap, normalMap);
        } catch (Exception e) {
            fail("Failed to set up normalMap field: " + e.getMessage());
        }
        assertFalse(bidiMap.containsKey(null));
    }
}
