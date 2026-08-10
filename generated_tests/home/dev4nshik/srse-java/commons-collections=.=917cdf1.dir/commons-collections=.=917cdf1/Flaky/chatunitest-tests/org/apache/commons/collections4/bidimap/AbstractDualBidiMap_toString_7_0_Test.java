package org.apache.commons.collections4.bidimap;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import org.apache.commons.collections4.bidimap.AbstractDualBidiMap;
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
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
public class AbstractDualBidiMap_toString_7_0_Test {

    private AbstractDualBidiMap<String, Integer> dualBidiMap;

    @BeforeEach
    public void setUp() throws Exception {
        // Use reflection to access the protected constructor
        Constructor<AbstractDualBidiMap> constructor = AbstractDualBidiMap.class.getDeclaredConstructor(Map.class, Map.class);
        constructor.setAccessible(true);
        // Create sample data for testing
        Map<String, Integer> normalMap = new HashMap<>();
        normalMap.put("One", 1);
        normalMap.put("Two", 2);
        normalMap.put("Three", 3);
        Map<Integer, String> reverseMap = new HashMap<>();
        reverseMap.put(1, "One");
        reverseMap.put(2, "Two");
        reverseMap.put(3, "Three");
        // Initialize the focal class instance using an anonymous subclass
        dualBidiMap = new AbstractDualBidiMap<String, Integer>(normalMap, reverseMap) {

            @Override
            protected BidiMap<Integer, String> createBidiMap(Map<Integer, String> normalMap, Map<String, Integer> reverseMap, BidiMap<String, Integer> inverseBidiMap) {
                return null;
            }
        };
    }

    @Test
    public void testToString() throws Exception {
        // Access the private field 'normalMap' using reflection
        Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
        normalMapField.setAccessible(true);
        // Set the field value
        @SuppressWarnings("unchecked")
        Map<String, Integer> normalMap = (Map<String, Integer>) normalMapField.get(dualBidiMap);
        // Ensure normalMap is not null
        assertNotNull(normalMap);
        // Test the toString method
        String expected = normalMap.toString();
        String actual = dualBidiMap.toString();
        assertEquals(expected, actual);
    }
}
