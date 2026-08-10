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

public class MutableByte_getAndAdd_11_0_Test {

    private MutableByte mutableByte;

    @BeforeEach
    public void setUp() {
        mutableByte = new MutableByte();
    }

    @Test
    public void testGetAndAdd() throws NoSuchFieldException, IllegalAccessException {
        // Set initial value using reflection
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        valueField.set(mutableByte, (byte) 10);
        // Test getAndAdd
        byte result = mutableByte.getAndAdd((byte) 5);
        // Check that the method returns the original value
        assertEquals(10, result);
        // Check that the internal value has been updated correctly
        assertEquals(15, valueField.get(mutableByte));
    }

    @Test
    public void testGetAndAddWithNegative() throws NoSuchFieldException, IllegalAccessException {
        // Set initial value using reflection
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        valueField.set(mutableByte, (byte) 10);
        // Test getAndAdd with a negative operand
        byte result = mutableByte.getAndAdd((byte) -3);
        // Check that the method returns the original value
        assertEquals(10, result);
        // Check that the internal value has been updated correctly
        assertEquals(7, valueField.get(mutableByte));
    }

    @Test
    public void testGetAndAddWithZero() throws NoSuchFieldException, IllegalAccessException {
        // Set initial value using reflection
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        valueField.set(mutableByte, (byte) 10);
        // Test getAndAdd with a zero operand
        byte result = mutableByte.getAndAdd((byte) 0);
        // Check that the method returns the original value
        assertEquals(10, result);
        // Check that the internal value remains unchanged
        assertEquals(10, valueField.get(mutableByte));
    }
}
