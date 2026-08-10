package org.apache.commons.lang3.mutable;

import java.lang.reflect.Field;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_decrement_6_0_Test {

    private MutableByte mutableByte;

    @BeforeEach
    public void setUp() {
        // Initialize with a specific value
        mutableByte = new MutableByte((byte) 10);
    }

    @Test
    public void testDecrement() throws NoSuchFieldException, IllegalAccessException {
        // Use reflection to access the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        // Call the decrement method
        mutableByte.decrement();
        // Assert the value has been decremented
        byte expectedValue = 9;
        byte actualValue = (byte) valueField.get(mutableByte);
        assertEquals(expectedValue, actualValue);
    }
}
