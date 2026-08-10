package org.apache.commons.lang3.mutable;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_longValue_20_0_Test {

    @Test
    public void testLongValue() throws Exception {
        // Use reflection to create an instance of MutableByte
        Constructor<MutableByte> constructor = MutableByte.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        MutableByte mutableByte = constructor.newInstance();
        // Use reflection to set the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        // Test with a range of byte values
        for (byte b = Byte.MIN_VALUE; b < Byte.MAX_VALUE; b++) {
            valueField.setByte(mutableByte, b);
            assertEquals((long) b, mutableByte.longValue(), "Failed for byte value: " + b);
        }
        // Test the maximum byte value
        valueField.setByte(mutableByte, Byte.MAX_VALUE);
        assertEquals((long) Byte.MAX_VALUE, mutableByte.longValue(), "Failed for byte value: " + Byte.MAX_VALUE);
    }
}
