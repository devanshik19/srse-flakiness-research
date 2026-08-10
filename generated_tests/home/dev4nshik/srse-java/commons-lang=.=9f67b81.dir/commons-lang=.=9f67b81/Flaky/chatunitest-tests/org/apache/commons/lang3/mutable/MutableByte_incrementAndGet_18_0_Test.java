package org.apache.commons.lang3.mutable;

import java.lang.reflect.Field;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_incrementAndGet_18_0_Test {

    @Test
    public void testIncrementAndGet() throws NoSuchFieldException, IllegalAccessException {
        // Create an instance of MutableByte
        MutableByte mutableByte = new MutableByte((byte) 0);
        // Use reflection to access the private 'value' field
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        // Check the initial value
        assertEquals((byte) 0, valueField.get(mutableByte));
        // Invoke incrementAndGet and check the result
        byte result = mutableByte.incrementAndGet();
        assertEquals((byte) 1, result);
        // Check the updated value using reflection
        assertEquals((byte) 1, valueField.get(mutableByte));
        // Increment again and verify
        result = mutableByte.incrementAndGet();
        assertEquals((byte) 2, result);
        assertEquals((byte) 2, valueField.get(mutableByte));
    }
}
