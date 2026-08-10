package dev.miku.r2dbc.mysql.util;

import dev.miku.r2dbc.mysql.util.InternalArrays;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.List;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.AbstractList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;
import java.util.ListIterator;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.RandomAccess;
import java.util.Spliterator;
import java.util.function.Consumer;
import java.util.function.Predicate;
import java.util.function.UnaryOperator;
import static dev.miku.r2dbc.mysql.util.AssertUtils.requireNonNull;

@ExtendWith(MockitoExtension.class)
class InternalArrays_toImmutableList_1_0_Test {

    @Test
    void testToImmutableListWithEmptyArray() {
        List<Object> result = InternalArrays.toImmutableList();
        assertTrue(result.isEmpty(), "The list should be empty");
    }

    @Test
    void testToImmutableListWithSingleElement() {
        List<String> result = InternalArrays.toImmutableList("single");
        assertEquals(1, result.size(), "The list should contain one element");
        assertEquals("single", result.get(0), "The list should contain the element 'single'");
    }

    @Test
    void testToImmutableListWithMultipleElements() {
        List<Integer> result = InternalArrays.toImmutableList(1, 2, 3);
        assertEquals(3, result.size(), "The list should contain three elements");
        assertEquals(1, result.get(0), "The first element should be 1");
        assertEquals(2, result.get(1), "The second element should be 2");
        assertEquals(3, result.get(2), "The third element should be 3");
    }

    @Test
    void testToImmutableListWithNullArray() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            InternalArrays.toImmutableList((Object[]) null);
        });
        assertEquals("array must not be null", exception.getMessage(), "Exception message should match");
    }
}
