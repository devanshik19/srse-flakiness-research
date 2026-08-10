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

public class AntiCollisionHashMap_clear_20_0_Test {

    private AntiCollisionHashMap<String, String> map;

    @BeforeEach
    public void setUp() {
        map = new AntiCollisionHashMap<>();
    }

    @Test
    public void testClear() throws NoSuchFieldException, IllegalAccessException {
        map.put("key1", "value1");
        map.put("key2", "value2");
        // Ensure the map is not empty before clear
        assertEquals(2, map.size());
        // Invoke the clear method
        map.clear();
        // Check if the size is set to 0
        assertEquals(0, map.size());
        // Use reflection to check if the table is cleared
        Field tableField = AntiCollisionHashMap.class.getDeclaredField("table");
        tableField.setAccessible(true);
        Object[] table = (Object[]) tableField.get(map);
        for (Object entry : table) {
            assertEquals(null, entry);
        }
        // Check if the modCount is incremented
        Field modCountField = AntiCollisionHashMap.class.getDeclaredField("modCount");
        modCountField.setAccessible(true);
        int modCount = (int) modCountField.get(map);
        assertEquals(1, modCount);
    }
}
