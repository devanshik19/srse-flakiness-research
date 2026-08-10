package org.apache.commons.collections4.bidimap;

import org.apache.commons.collections4.bidimap.AbstractDualBidiMap;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Map;
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
public class AbstractDualBidiMap_putAll_9_1_Test {

    private AbstractDualBidiMap<String, Integer> bidiMap;

    private Map<String, Integer> normalMap;

    private Map<Integer, String> reverseMap;

    @BeforeEach
    public void setUp() throws Exception {
        normalMap = new HashMap<>();
        reverseMap = new HashMap<>();
        // Using a mock subclass to instantiate the abstract class
        bidiMap = mock(AbstractDualBidiMap.class, withSettings().useConstructor(normalMap, reverseMap).defaultAnswer(CALLS_REAL_METHODS));
    }

    @Test
    public void testPutAll() {
        Map<String, Integer> testMap = new HashMap<>();
        testMap.put("one", 1);
        testMap.put("two", 2);
        bidiMap.putAll(testMap);
        assertEquals(2, normalMap.size());
        assertEquals(1, normalMap.get("one"));
        assertEquals(2, normalMap.get("two"));
    }

    @Test
    public void testPutAllWithExistingKeys() {
        normalMap.put("one", 1);
        reverseMap.put(1, "one");
        Map<String, Integer> testMap = new HashMap<>();
        testMap.put("one", 1);
        testMap.put("two", 2);
        bidiMap.putAll(testMap);
        assertEquals(2, normalMap.size());
        assertEquals(1, normalMap.get("one"));
        assertEquals(2, normalMap.get("two"));
    }
}
