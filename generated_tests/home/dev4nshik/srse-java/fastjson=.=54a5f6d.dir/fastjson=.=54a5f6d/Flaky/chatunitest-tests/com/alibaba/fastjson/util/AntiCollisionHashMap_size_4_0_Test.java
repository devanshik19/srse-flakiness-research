package com.alibaba.fastjson.util;

import java.lang.reflect.Field;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.IOException;
import java.io.Serializable;
import java.util.*;

public class AntiCollisionHashMap_size_4_0_Test {

    @Test
    public void testSize() throws NoSuchFieldException, IllegalAccessException {
        // Create an instance of the AntiCollisionHashMap
        AntiCollisionHashMap<String, String> map = new AntiCollisionHashMap<>();
        // Use reflection to access the private 'size' field
        Field sizeField = AntiCollisionHashMap.class.getDeclaredField("size");
        sizeField.setAccessible(true);
        // Test when the map is empty
        sizeField.set(map, 0);
        assertEquals(0, map.size(), "Size should be 0 for an empty map");
        // Test when the map has one element
        sizeField.set(map, 1);
        assertEquals(1, map.size(), "Size should be 1 when one element is added");
        // Test when the map has multiple elements
        sizeField.set(map, 5);
        assertEquals(5, map.size(), "Size should be 5 when five elements are added");
    }
}
