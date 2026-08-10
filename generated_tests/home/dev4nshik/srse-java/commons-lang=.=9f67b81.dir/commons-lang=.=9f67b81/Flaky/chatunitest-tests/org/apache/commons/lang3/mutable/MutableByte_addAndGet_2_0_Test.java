package org.apache.commons.lang3.mutable;

import java.lang.reflect.Field;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_addAndGet_2_0_Test {

    private MutableByte mutableByte;

    @BeforeEach
    public void setUp() {
        mutableByte = new MutableByte();
    }

    @Test
    public void testAddAndGet() throws NoSuchFieldException, IllegalAccessException {
        // Set initial value using reflection
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        valueField.set(mutableByte, (byte) 5);
        // Test addAndGet method
        byte result = mutableByte.addAndGet((byte) 3);
        // Assert the result
        assertEquals(8, result);
        // Verify the internal state
        assertEquals(8, valueField.get(mutableByte));
    }

    @Test
    public void testAddAndGetWithNegative() throws NoSuchFieldException, IllegalAccessException {
        // Set initial value using reflection
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        valueField.set(mutableByte, (byte) 5);
        // Test addAndGet method with a negative operand
        byte result = mutableByte.addAndGet((byte) -2);
        // Assert the result
        assertEquals(3, result);
        // Verify the internal state
        assertEquals(3, valueField.get(mutableByte));
    }

    @Test
    public void testAddAndGetWithZero() throws NoSuchFieldException, IllegalAccessException {
        // Set initial value using reflection
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        valueField.set(mutableByte, (byte) 5);
        // Test addAndGet method with zero
        byte result = mutableByte.addAndGet((byte) 0);
        // Assert the result
        assertEquals(5, result);
        // Verify the internal state
        assertEquals(5, valueField.get(mutableByte));
    }
}
