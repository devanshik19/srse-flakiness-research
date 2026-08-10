package org.apache.commons.lang3.mutable;

import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_compareTo_5_0_Test {

    @Test
    public void testCompareToEqual() {
        MutableByte byte1 = new MutableByte((byte) 5);
        MutableByte byte2 = new MutableByte((byte) 5);
        assertEquals(0, byte1.compareTo(byte2), "Expected comparison result to be 0 when both bytes are equal.");
    }

    @Test
    public void testCompareToGreater() {
        MutableByte byte1 = new MutableByte((byte) 10);
        MutableByte byte2 = new MutableByte((byte) 5);
        assertEquals(1, byte1.compareTo(byte2), "Expected comparison result to be positive when first byte is greater.");
    }

    @Test
    public void testCompareToLess() {
        MutableByte byte1 = new MutableByte((byte) 5);
        MutableByte byte2 = new MutableByte((byte) 10);
        assertEquals(-1, byte1.compareTo(byte2), "Expected comparison result to be negative when first byte is less.");
    }
}
