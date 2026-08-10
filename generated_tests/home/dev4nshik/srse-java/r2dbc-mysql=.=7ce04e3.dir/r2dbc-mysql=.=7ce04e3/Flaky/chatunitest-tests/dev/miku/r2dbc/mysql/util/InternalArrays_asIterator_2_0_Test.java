package dev.miku.r2dbc.mysql.util;

import java.util.Collections;
import java.util.Iterator;
import java.util.NoSuchElementException;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.AbstractList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Comparator;
import java.util.List;
import java.util.ListIterator;
import java.util.Objects;
import java.util.RandomAccess;
import java.util.Spliterator;
import java.util.function.Consumer;
import java.util.function.Predicate;
import java.util.function.UnaryOperator;
import static dev.miku.r2dbc.mysql.util.AssertUtils.requireNonNull;

class InternalArrays_asIterator_2_0_Test {

    @Test
    void testAsIteratorWithNonNullArray() {
        Integer[] array = { 1, 2, 3 };
        Iterator<Integer> iterator = InternalArrays.asIterator(array);
        assertNotNull(iterator);
        assertTrue(iterator.hasNext());
        assertEquals(1, iterator.next());
        assertTrue(iterator.hasNext());
        assertEquals(2, iterator.next());
        assertTrue(iterator.hasNext());
        assertEquals(3, iterator.next());
        assertFalse(iterator.hasNext());
    }

    @Test
    void testAsIteratorWithEmptyArray() {
        Integer[] array = {};
        Iterator<Integer> iterator = InternalArrays.asIterator(array);
        assertNotNull(iterator);
        assertFalse(iterator.hasNext());
    }

    @Test
    void testAsIteratorWithNullArray() {
        assertThrows(IllegalArgumentException.class, () -> {
            InternalArrays.asIterator(null);
        });
    }

    @Test
    void testAsIteratorWithEmptyArrayNoSuchElementException() {
        Integer[] array = {};
        Iterator<Integer> iterator = InternalArrays.asIterator(array);
        assertThrows(NoSuchElementException.class, iterator::next);
    }

    @Test
    void testAsIteratorWithNonNullArrayNoSuchElementException() {
        Integer[] array = { 1 };
        Iterator<Integer> iterator = InternalArrays.asIterator(array);
        assertNotNull(iterator);
        assertTrue(iterator.hasNext());
        assertEquals(1, iterator.next());
        assertFalse(iterator.hasNext());
        assertThrows(NoSuchElementException.class, iterator::next);
    }
}
