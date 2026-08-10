package org.apache.commons.lang3.mutable;

import java.lang.reflect.Field;
import org.apache.commons.lang3.mutable.MutableByte;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_toString_26_0_Test {

    @Test
    public void testToString() throws Exception {
        // Create an instance of MutableByte using the default constructor
        MutableByte mutableByte = new MutableByte();
        // Use reflection to set the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        // Test with different byte values
        byte[] testValues = { 0, 1, -1, 127, -128 };
        for (byte testValue : testValues) {
            valueField.set(mutableByte, testValue);
            assertEquals(String.valueOf(testValue), mutableByte.toString());
        }
    }
}
