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

public class AntiCollisionHashMap_keySet_29_0_Test {

    private AntiCollisionHashMap<String, String> map;

    @BeforeEach
    public void setUp() {
        map = new AntiCollisionHashMap<>();
    }

    @Test
    public void testKeySet_WhenKeySetIsNull() throws Exception {
        // Ensure keySet is null initially
        setPrivateField("keySet", null);
        Set<String> keySet = map.keySet();
        assertNotNull(keySet, "The keySet should not be null.");
        // Verify that the keySet field is now initialized
        Set<String> internalKeySet = getPrivateField("keySet");
        assertSame(keySet, internalKeySet, "The cached keySet should be the same as the returned keySet.");
    }

    @Test
    public void testKeySet_WhenKeySetIsNotNull() throws Exception {
        Set<String> existingKeySet = new HashSet<>();
        setPrivateField("keySet", existingKeySet);
        Set<String> keySet = map.keySet();
        assertSame(existingKeySet, keySet, "The returned keySet should be the same as the existing keySet.");
    }

    @SuppressWarnings("unchecked")
    private void setPrivateField(String fieldName, Object value) throws Exception {
        Field field = AntiCollisionHashMap.class.getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(map, value);
    }

    @SuppressWarnings("unchecked")
    private <T> T getPrivateField(String fieldName) throws Exception {
        Field field = AntiCollisionHashMap.class.getDeclaredField(fieldName);
        field.setAccessible(true);
        return (T) field.get(map);
    }
}
