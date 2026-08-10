package org.apache.commons.lang3.mutable;

import org.apache.commons.lang3.mutable.MutableByte;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_floatValue_10_0_Test {

    @Test
    public void testFloatValue() throws Exception {
        // Test default constructor
        MutableByte defaultMutableByte = new MutableByte();
        assertEquals(0.0f, defaultMutableByte.floatValue(), "Default constructor should initialize value to 0");
        // Test byte constructor
        MutableByte byteConstructorMutableByte = new MutableByte((byte) 5);
        assertEquals(5.0f, byteConstructorMutableByte.floatValue(), "Byte constructor should initialize value to 5");
        // Test Number constructor
        MutableByte numberConstructorMutableByte = new MutableByte((Number) 10);
        assertEquals(10.0f, numberConstructorMutableByte.floatValue(), "Number constructor should initialize value to 10");
        // Test String constructor
        MutableByte stringConstructorMutableByte = new MutableByte("15");
        assertEquals(15.0f, stringConstructorMutableByte.floatValue(), "String constructor should initialize value to 15");
    }
}
