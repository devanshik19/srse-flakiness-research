package org.apache.commons.collections4.bidimap;

import java.lang.reflect.Constructor;
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

public class AbstractDualBidiMap_hashCode_6_1_Test {

    private AbstractDualBidiMap<String, Integer> bidiMapInstance;

    @BeforeEach
    public void setUp() throws Exception {
        // Use reflection to create an instance of a concrete subclass of AbstractDualBidiMap
        Constructor<?> constructor = DualHashBidiMap.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        bidiMapInstance = (AbstractDualBidiMap<String, Integer>) constructor.newInstance();
        // Use reflection to set the normalMap field
        Field normalMapField = AbstractDualBidiMap.class.getDeclaredField("normalMap");
        normalMapField.setAccessible(true);
        Map<String, Integer> normalMap = new HashMap<>();
        normalMap.put("one", 1);
        normalMap.put("two", 2);
        normalMap.put("three", 3);
        normalMapField.set(bidiMapInstance, normalMap);
    }

    @Test
    public void testHashCode() {
        int expectedHashCode = bidiMapInstance.normalMap.hashCode();
        int actualHashCode = bidiMapInstance.hashCode();
        assertEquals(expectedHashCode, actualHashCode);
    }
}
