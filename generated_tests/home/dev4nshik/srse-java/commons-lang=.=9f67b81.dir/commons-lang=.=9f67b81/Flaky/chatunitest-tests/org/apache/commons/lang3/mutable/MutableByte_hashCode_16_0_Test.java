package org.apache.commons.lang3.mutable;

import java.lang.reflect.Field;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_hashCode_16_0_Test {

    @Test
    public void testHashCode() throws NoSuchFieldException, IllegalAccessException {
        // Create an instance of MutableByte
        MutableByte mutableByte = new MutableByte((byte) 5);
        // Use reflection to access the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        // Set the value of the private field 'value' to 5
        valueField.set(mutableByte, (byte) 5);
        // Verify that hashCode() returns the correct value
        assertEquals(5, mutableByte.hashCode());
        // Change the value of the private field 'value' to -128
        valueField.set(mutableByte, (byte) -128);
        // Verify that hashCode() returns the correct value
        assertEquals(-128, mutableByte.hashCode());
        // Change the value of the private field 'value' to 127
        valueField.set(mutableByte, (byte) 127);
        // Verify that hashCode() returns the correct value
        assertEquals(127, mutableByte.hashCode());
    }
}
