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

public class MutableByte_subtract_23_0_Test {

    @Test
    public void testSubtract() throws NoSuchFieldException, IllegalAccessException {
        // Create an instance of MutableByte with an initial value
        MutableByte mutableByte = new MutableByte((byte) 10);
        // Use reflection to set the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        valueField.set(mutableByte, (byte) 10);
        // Call the subtract method
        mutableByte.subtract((byte) 3);
        // Assert the expected value
        byte expectedValue = 7;
        byte actualValue = (byte) valueField.get(mutableByte);
        assertEquals(expectedValue, actualValue, "The value after subtraction should be 7");
        // Test with subtraction resulting in negative value
        mutableByte.subtract((byte) 10);
        expectedValue = -3;
        actualValue = (byte) valueField.get(mutableByte);
        assertEquals(expectedValue, actualValue, "The value after subtraction should be -3");
        // Test with subtraction of zero
        mutableByte.subtract((byte) 0);
        expectedValue = -3;
        actualValue = (byte) valueField.get(mutableByte);
        assertEquals(expectedValue, actualValue, "The value after subtraction should remain -3");
    }
}
