package cn.crane4j.core.util;

import org.junit.Assert;
import org.junit.Test;

import java.util.*;

public class ObjectUtils_get_0_0_Test {

    @Test
    public void testNull() {
        Assert.assertNull(ObjectUtils.get(null, 0));
    }

    @Test
    public void testList() {
        List<String> list = Arrays.asList("a", "b");
        Assert.assertEquals("a", ObjectUtils.get(list, 0));
        Assert.assertEquals("b", ObjectUtils.get(list, 1));
        Assert.assertNull(ObjectUtils.get(list, 2));
        Assert.assertNull(ObjectUtils.get(list, -1));
    }

    @Test
    public void testIterator() {
        Assert.assertEquals("b", ObjectUtils.get(Arrays.asList("a", "b").iterator(), 1));
        Assert.assertNull(ObjectUtils.get(Arrays.asList("a", "b").iterator(), 5));
    }

    @Test
    public void testIterable() {
        Set<String> set = new LinkedHashSet<>(Arrays.asList("a", "b"));
        Assert.assertEquals("a", ObjectUtils.get(set, 0));
        Assert.assertEquals("b", ObjectUtils.get(set, 1));
        Assert.assertNull(ObjectUtils.get(set, 2));
    }

    @Test
    public void testMap() {
        Map<String, Integer> map = new LinkedHashMap<>();
        map.put("a", 1);
        map.put("b", 2);
        Assert.assertEquals(Integer.valueOf(1), ObjectUtils.get(map, 0));
        Assert.assertEquals(Integer.valueOf(2), ObjectUtils.get(map, 1));
        Assert.assertNull(ObjectUtils.get(map, 2));
    }

    @Test
    public void testArray() {
        String[] arr = {"a", "b"};
        Assert.assertEquals("a", ObjectUtils.get(arr, 0));
        Assert.assertEquals("b", ObjectUtils.get(arr, 1));
        Assert.assertNull(ObjectUtils.get(arr, 2));
        Assert.assertNull(ObjectUtils.get(arr, -1));
    }

    @Test(expected = ClassCastException.class)
    public void testPrimitiveArray() {
        Object r = ObjectUtils.get(new int[]{1, 2}, 0);
    }

    @Test
    public void testOther() {
        Assert.assertNull(ObjectUtils.get("abc", 0));
        Assert.assertNull(ObjectUtils.get(new Object(), 0));
    }
}
