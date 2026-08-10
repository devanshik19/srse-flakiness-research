package org.apache.commons.collections4.bidimap;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import org.apache.commons.collections4.bidimap.AbstractDualBidiMap;
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

class AbstractDualBidiMap_put_8_0_Test {

    private AbstractDualBidiMap<String, String> bidiMap;

    @BeforeEach
    void setUp() throws Exception {
        Map<String, String> normalMap = new HashMap<>();
        Map<String, String> reverseMap = new HashMap<>();
        // Use reflection to instantiate the abstract class with a concrete implementation
        bidiMap = new AbstractDualBidiMap<String, String>(normalMap, reverseMap) {

            @Override
            protected BidiMap<String, String> createBidiMap(Map<String, String> normalMap, Map<String, String> reverseMap, BidiMap<String, String> inverseBidiMap) {
                // Provide a simple implementation or mock if needed
                return null;
            }
        };
    }

    @Test
    void testPutNewEntry() throws Exception {
        String key = "key1";
        String value = "value1";
        // Invoke put method
        String result = bidiMap.put(key, value);
        // Validate the result
        assertNull(result);
        assertEquals(value, getFieldValue(bidiMap, "normalMap").get(key));
        assertEquals(key, getFieldValue(bidiMap, "reverseMap").get(value));
    }

    @Test
    void testPutExistingKey() throws Exception {
        String key = "key1";
        String oldValue = "value1";
        String newValue = "value2";
        bidiMap.put(key, oldValue);
        // Invoke put method with existing key
        String result = bidiMap.put(key, newValue);
        // Validate the result
        assertEquals(oldValue, result);
        assertEquals(newValue, getFieldValue(bidiMap, "normalMap").get(key));
        assertEquals(key, getFieldValue(bidiMap, "reverseMap").get(newValue));
        assertFalse(getFieldValue(bidiMap, "reverseMap").containsKey(oldValue));
    }

    @Test
    void testPutExistingValue() throws Exception {
        String key1 = "key1";
        String key2 = "key2";
        String value = "value1";
        bidiMap.put(key1, value);
        // Invoke put method with existing value
        String result = bidiMap.put(key2, value);
        // Validate the result
        assertNull(result);
        assertEquals(value, getFieldValue(bidiMap, "normalMap").get(key2));
        assertEquals(key2, getFieldValue(bidiMap, "reverseMap").get(value));
        assertFalse(getFieldValue(bidiMap, "normalMap").containsKey(key1));
    }

    @SuppressWarnings("unchecked")
    private <T> Map<T, T> getFieldValue(AbstractDualBidiMap<T, T> bidiMap, String fieldName) throws Exception {
        Field field = AbstractDualBidiMap.class.getDeclaredField(fieldName);
        field.setAccessible(true);
        return (Map<T, T>) field.get(bidiMap);
    }
}
