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

public class MutableByte_subtract_24_0_Test {

    @Test
    public void testSubtract() throws Exception {
        // Create an instance of MutableByte with initial value 10
        MutableByte mutableByte = new MutableByte((byte) 10);
        // Use reflection to access the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        // Subtract 3 from the current value
        mutableByte.subtract((byte) 3);
        // Verify the value is now 7
        assertEquals((byte) 7, valueField.get(mutableByte));
        // Subtract 10 from the current value
        mutableByte.subtract((byte) 10);
        // Verify the value is now -3
        assertEquals((byte) -3, valueField.get(mutableByte));
    }
}
