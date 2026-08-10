package org.apache.commons.lang3.mutable;

import org.apache.commons.lang3.mutable.MutableByte;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_add_1_0_Test {

    private MutableByte mutableByte;

    @BeforeEach
    public void setUp() {
        mutableByte = new MutableByte((byte) 10);
    }

    @Test
    public void testAddPositiveNumber() throws Exception {
        Number operand = 5;
        invokeAddMethod(operand);
        assertEquals((byte) 15, getValueField());
    }

    @Test
    public void testAddNegativeNumber() throws Exception {
        Number operand = -3;
        invokeAddMethod(operand);
        assertEquals((byte) 7, getValueField());
    }

    @Test
    public void testAddZero() throws Exception {
        Number operand = 0;
        invokeAddMethod(operand);
        assertEquals((byte) 10, getValueField());
    }

    @Test
    public void testAddNumberCausingOverflow() throws Exception {
        mutableByte = new MutableByte(Byte.MAX_VALUE);
        Number operand = 1;
        invokeAddMethod(operand);
        assertEquals(Byte.MIN_VALUE, getValueField());
    }

    private void invokeAddMethod(Number operand) throws Exception {
        Method addMethod = MutableByte.class.getDeclaredMethod("add", Number.class);
        addMethod.setAccessible(true);
        addMethod.invoke(mutableByte, operand);
    }

    private byte getValueField() throws Exception {
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        return valueField.getByte(mutableByte);
    }
}
