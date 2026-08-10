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

public class MutableByte_add_0_0_Test {

    private MutableByte mutableByte;

    @BeforeEach
    public void setUp() {
        mutableByte = new MutableByte();
    }

    @Test
    public void testAdd() throws NoSuchFieldException, IllegalAccessException {
        // Use reflection to access the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        // Set initial value
        valueField.set(mutableByte, (byte) 5);
        // Call the add method
        mutableByte.add((byte) 3);
        // Assert the value after addition
        assertEquals((byte) 8, valueField.get(mutableByte));
    }

    @Test
    public void testAddNegativeValue() throws NoSuchFieldException, IllegalAccessException {
        // Use reflection to access the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        // Set initial value
        valueField.set(mutableByte, (byte) 5);
        // Call the add method with a negative operand
        mutableByte.add((byte) -2);
        // Assert the value after addition
        assertEquals((byte) 3, valueField.get(mutableByte));
    }

    @Test
    public void testAddWithOverflow() throws NoSuchFieldException, IllegalAccessException {
        // Use reflection to access the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        // Set initial value
        valueField.set(mutableByte, Byte.MAX_VALUE);
        // Call the add method with an operand that causes overflow
        mutableByte.add((byte) 1);
        // Assert the value after addition, should wrap around
        assertEquals(Byte.MIN_VALUE, valueField.get(mutableByte));
    }
}
