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

public class MutableByte_intValue_19_0_Test {

    @Test
    public void testIntValue() throws NoSuchFieldException, IllegalAccessException {
        MutableByte mutableByte = new MutableByte();
        // Using reflection to set the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        // Test with default constructor
        valueField.set(mutableByte, (byte) 0);
        assertEquals(0, mutableByte.intValue(), "intValue should return 0 when value is 0");
        // Test with specific byte value
        valueField.set(mutableByte, (byte) 10);
        assertEquals(10, mutableByte.intValue(), "intValue should return 10 when value is 10");
        // Test with negative byte value
        valueField.set(mutableByte, (byte) -5);
        assertEquals(-5, mutableByte.intValue(), "intValue should return -5 when value is -5");
    }
}
