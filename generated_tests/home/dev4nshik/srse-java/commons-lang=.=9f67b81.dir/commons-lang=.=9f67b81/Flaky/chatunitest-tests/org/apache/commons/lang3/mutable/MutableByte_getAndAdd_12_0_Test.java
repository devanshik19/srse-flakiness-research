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

public class MutableByte_getAndAdd_12_0_Test {

    @Test
    public void testGetAndAdd() throws Exception {
        // Testing default constructor
        MutableByte mutableByte = new MutableByte();
        setPrivateField(mutableByte, "value", (byte) 5);
        byte result = mutableByte.getAndAdd((byte) 3);
        assertEquals(5, result);
        assertEquals(8, getPrivateField(mutableByte, "value"));
        // Testing constructor with initial value
        MutableByte mutableByteWithValue = new MutableByte((byte) 10);
        result = mutableByteWithValue.getAndAdd((byte) -4);
        assertEquals(10, result);
        assertEquals(6, getPrivateField(mutableByteWithValue, "value"));
    }

    private byte getPrivateField(MutableByte mutableByte, String fieldName) throws Exception {
        Field field = MutableByte.class.getDeclaredField(fieldName);
        field.setAccessible(true);
        return field.getByte(mutableByte);
    }

    private void setPrivateField(MutableByte mutableByte, String fieldName, byte value) throws Exception {
        Field field = MutableByte.class.getDeclaredField(fieldName);
        field.setAccessible(true);
        field.setByte(mutableByte, value);
    }
}
