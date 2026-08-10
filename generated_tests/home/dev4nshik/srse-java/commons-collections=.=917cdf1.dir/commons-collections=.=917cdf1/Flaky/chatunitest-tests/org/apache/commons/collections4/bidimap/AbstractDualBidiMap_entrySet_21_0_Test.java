package org.apache.commons.collections4.bidimap;

import org.apache.commons.collections4.bidimap.AbstractDualBidiMap;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.Collection;
import java.util.Iterator;
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

class AbstractDualBidiMap_entrySet_21_0_Test {

    private AbstractDualBidiMap<String, String> bidiMap;

    @BeforeEach
    void setUp() {
        bidiMap = new AbstractDualBidiMap<String, String>() {

            @Override
            protected BidiMap<String, String> createBidiMap(Map<String, String> normalMap, Map<String, String> reverseMap, BidiMap<String, String> inverseMap) {
                return null;
            }
        };
    }

    @Test
    void testEntrySet_whenEntrySetIsNotNull_shouldReturnExistingEntrySet() throws NoSuchFieldException, IllegalAccessException {
        Field entrySetField = AbstractDualBidiMap.class.getDeclaredField("entrySet");
        entrySetField.setAccessible(true);
        Set<Map.Entry<String, String>> mockEntrySet = new HashMap<String, String>() {

            {
                put("key", "value");
            }
        }.entrySet();
        entrySetField.set(bidiMap, mockEntrySet);
        Set<Map.Entry<String, String>> entrySet = bidiMap.entrySet();
        assertNotNull(entrySet);
        assertSame(mockEntrySet, entrySet);
    }
}
