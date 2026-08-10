package org.apache.commons.lang3.mutable;

import org.apache.commons.lang3.mutable.MutableByte;
import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_addAndGet_3_0_Test {

    @Test
    public void testAddAndGet() throws Exception {
        // Create an instance of MutableByte
        MutableByte mutableByte = new MutableByte((byte) 5);
        // Use reflection to access the private field 'value'
        Method addAndGetMethod = MutableByte.class.getDeclaredMethod("addAndGet", Number.class);
        addAndGetMethod.setAccessible(true);
        // Test adding a positive number
        byte result = (byte) addAndGetMethod.invoke(mutableByte, 3);
        assertEquals(8, result);
        // Test adding a negative number
        result = (byte) addAndGetMethod.invoke(mutableByte, -2);
        assertEquals(6, result);
        // Test adding zero
        result = (byte) addAndGetMethod.invoke(mutableByte, 0);
        assertEquals(6, result);
        // Test adding a large number that causes overflow
        result = (byte) addAndGetMethod.invoke(mutableByte, 250);
        // 6 + 250 = 256, which overflows to 0
        assertEquals(-4, result);
    }
}
