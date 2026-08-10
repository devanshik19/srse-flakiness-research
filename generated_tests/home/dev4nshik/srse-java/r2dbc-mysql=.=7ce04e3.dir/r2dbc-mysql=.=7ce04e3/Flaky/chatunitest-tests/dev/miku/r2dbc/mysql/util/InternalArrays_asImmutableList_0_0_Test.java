package dev.miku.r2dbc.mysql.util;

import java.util.List;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
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

public class InternalArrays_asImmutableList_0_0_Test {

    @Test
    public void testAsImmutableListWithEmptyArray() {
        List<Object> result = InternalArrays.asImmutableList();
        assertTrue(result.isEmpty(), "The list should be empty");
    }

    @Test
    public void testAsImmutableListWithSingleElement() {
        String element = "test";
        List<String> result = InternalArrays.asImmutableList(element);
        assertEquals(1, result.size(), "The list should contain one element");
        assertEquals(element, result.get(0), "The list element should be the same as the input element");
    }

    @Test
    public void testAsImmutableListWithMultipleElements() {
        String[] elements = { "one", "two", "three" };
        List<String> result = InternalArrays.asImmutableList(elements);
        assertEquals(elements.length, result.size(), "The list should contain all input elements");
        for (int i = 0; i < elements.length; i++) {
            assertEquals(elements[i], result.get(i), "The list elements should be the same as the input elements");
        }
    }

    @Test
    public void testAsImmutableListWithNullArray() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            InternalArrays.asImmutableList((Object[]) null);
        });
        assertEquals("array must not be null", exception.getMessage(), "Exception message should match");
    }
}
