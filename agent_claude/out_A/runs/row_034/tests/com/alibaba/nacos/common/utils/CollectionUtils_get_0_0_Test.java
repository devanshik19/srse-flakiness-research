package com.alibaba.nacos.common.utils;

import org.junit.Test;

import java.util.*;

import static org.junit.Assert.*;

public class CollectionUtils_get_0_0_Test {

    @Test(expected = IndexOutOfBoundsException.class)
    public void testNegativeIndex() {
        CollectionUtils.get(new ArrayList<>(), -1);
    }

    @Test
    public void testMap() {
        Map<String, String> map = new LinkedHashMap<>();
        map.put("a", "1");
        map.put("b", "2");
        Map.Entry<?, ?> e = (Map.Entry<?, ?>) CollectionUtils.get(map, 1);
        assertEquals("b", e.getKey());
        assertEquals("2", e.getValue());
    }

    @Test(expected = IndexOutOfBoundsException.class)
    public void testMapOutOfBounds() {
        Map<String, String> map = new HashMap<>();
        map.put("a", "1");
        CollectionUtils.get(map, 3);
    }

    @Test
    public void testList() {
        assertEquals("b", CollectionUtils.get(Arrays.asList("a", "b"), 1));
    }

    @Test(expected = IndexOutOfBoundsException.class)
    public void testListOutOfBounds() {
        CollectionUtils.get(new ArrayList<>(), 0);
    }

    @Test
    public void testObjectArray() {
        assertEquals("a", CollectionUtils.get(new String[] {"a", "b"}, 0));
    }

    @Test(expected = IndexOutOfBoundsException.class)
    public void testObjectArrayOutOfBounds() {
        CollectionUtils.get(new Object[0], 0);
    }

    @Test
    public void testIterator() {
        assertEquals("c", CollectionUtils.get(Arrays.asList("a", "b", "c").iterator(), 2));
        assertEquals("a", CollectionUtils.get(Arrays.asList("a").iterator(), 0));
    }

    @Test(expected = IndexOutOfBoundsException.class)
    public void testIteratorOutOfBounds() {
        CollectionUtils.get(Arrays.asList("a").iterator(), 1);
    }

    @Test
    public void testCollection() {
        Set<String> set = new LinkedHashSet<>(Arrays.asList("x", "y"));
        assertEquals("y", CollectionUtils.get(set, 1));
    }

    @Test(expected = IndexOutOfBoundsException.class)
    public void testCollectionOutOfBounds() {
        CollectionUtils.get(new HashSet<>(), 0);
    }

    @Test
    public void testEnumeration() {
        Vector<String> v = new Vector<>(Arrays.asList("a", "b", "c"));
        assertEquals("b", CollectionUtils.get(v.elements(), 1));
        assertEquals("a", CollectionUtils.get(v.elements(), 0));
    }

    @Test(expected = IndexOutOfBoundsException.class)
    public void testEnumerationOutOfBounds() {
        CollectionUtils.get(new Vector<String>(Arrays.asList("a")).elements(), 2);
    }

    @Test
    public void testNull() {
        try {
            CollectionUtils.get(null, 0);
            fail();
        } catch (IllegalArgumentException e) {
            assertEquals("Unsupported object type: null", e.getMessage());
        }
    }

    @Test
    public void testPrimitiveArray() {
        assertEquals(2, CollectionUtils.get(new int[] {1, 2}, 1));
    }

    @Test(expected = ArrayIndexOutOfBoundsException.class)
    public void testPrimitiveArrayOutOfBounds() {
        CollectionUtils.get(new int[0], 0);
    }

    @Test
    public void testUnsupported() {
        try {
            CollectionUtils.get("str", 0);
            fail();
        } catch (IllegalArgumentException e) {
            assertEquals("Unsupported object type: java.lang.String", e.getMessage());
        }
    }
}
