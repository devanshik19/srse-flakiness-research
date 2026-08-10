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

public class MutableByte_decrementAndGet_7_0_Test {

    @Test
    public void testDecrementAndGet() throws NoSuchFieldException, IllegalAccessException {
        // Create an instance of MutableByte
        MutableByte mutableByte = new MutableByte();
        // Use reflection to set the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        valueField.set(mutableByte, (byte) 5);
        // Call the decrementAndGet method
        byte result = mutableByte.decrementAndGet();
        // Assert the result
        assertEquals(4, result);
        // Assert the internal state of the object
        assertEquals(4, valueField.get(mutableByte));
    }
}
