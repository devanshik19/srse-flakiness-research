package com.alibaba.fastjson.util;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.IOException;
import java.io.Serializable;
import java.util.*;

public class AntiCollisionHashMap_entrySet_31_0_Test {

    private AntiCollisionHashMap<String, String> map;

    @BeforeEach
    public void setUp() {
        map = new AntiCollisionHashMap<>();
    }

    @Test
    public void testEntrySet() throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        // Use reflection to access the private entrySet0 method
        Method entrySet0Method = AntiCollisionHashMap.class.getDeclaredMethod("entrySet0");
        entrySet0Method.setAccessible(true);
        // Invoke entrySet0 and ensure it returns a non-null set
        Set<Map.Entry<String, String>> entrySet0Result = (Set<Map.Entry<String, String>>) entrySet0Method.invoke(map);
        assertNotNull(entrySet0Result);
        // Call the public entrySet method and ensure it returns the same set as entrySet0
        Set<Map.Entry<String, String>> entrySetResult = map.entrySet();
        assertSame(entrySet0Result, entrySetResult);
    }
}
