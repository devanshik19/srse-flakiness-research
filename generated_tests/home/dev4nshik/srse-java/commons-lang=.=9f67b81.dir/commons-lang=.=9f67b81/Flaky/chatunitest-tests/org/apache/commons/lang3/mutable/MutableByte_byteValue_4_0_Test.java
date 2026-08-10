package org.apache.commons.lang3.mutable;

import org.apache.commons.lang3.mutable.MutableByte;
import java.lang.reflect.Field;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_byteValue_4_0_Test {

    @Test
    void testByteValue() throws NoSuchFieldException, IllegalAccessException {
        // Create a MutableByte instance using the default constructor
        MutableByte mutableByte = new MutableByte();
        // Use reflection to set the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        // Test when value is 0
        valueField.set(mutableByte, (byte) 0);
        assertEquals(0, mutableByte.byteValue());
        // Test when value is a positive byte
        valueField.set(mutableByte, (byte) 123);
        assertEquals(123, mutableByte.byteValue());
        // Test when value is a negative byte
        valueField.set(mutableByte, (byte) -45);
        assertEquals(-45, mutableByte.byteValue());
    }
}
