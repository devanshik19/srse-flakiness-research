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

public class AbstractDualBidiMap_getKey_14_0_Test {

    private AbstractDualBidiMap<String, Integer> bidiMap;

    @BeforeEach
    public void setUp() throws Exception {
        bidiMap = new AbstractDualBidiMap<String, Integer>(new HashMap<>(), new HashMap<>()) {

            @Override
            protected BidiMap<Integer, String> createBidiMap(Map<Integer, String> normalMap, Map<String, Integer> reverseMap, BidiMap<String, Integer> inverseBidiMap) {
                return null;
            }
        };
        Map<Integer, String> reverseMap = new HashMap<>();
        reverseMap.put(1, "one");
        reverseMap.put(2, "two");
        reverseMap.put(3, "three");
        Field reverseMapField = AbstractDualBidiMap.class.getDeclaredField("reverseMap");
        reverseMapField.setAccessible(true);
        reverseMapField.set(bidiMap, reverseMap);
    }

    @Test
    public void testGetKeyExistingValue() {
        assertEquals("one", bidiMap.getKey(1));
        assertEquals("two", bidiMap.getKey(2));
        assertEquals("three", bidiMap.getKey(3));
    }

    @Test
    public void testGetKeyNonExistingValue() {
        assertNull(bidiMap.getKey(4));
        assertNull(bidiMap.getKey(null));
    }
}
