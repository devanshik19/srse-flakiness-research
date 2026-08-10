package org.apache.commons.lang3.mutable;

import org.apache.commons.lang3.mutable.MutableByte;
import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_toByte_25_0_Test {

    @Test
    public void testToByte() throws Exception {
        // Create an instance of MutableByte using the constructor
        MutableByte mutableByte = new MutableByte((byte) 10);
        // Use reflection to access the private method byteValue
        Method byteValueMethod = MutableByte.class.getDeclaredMethod("byteValue");
        byteValueMethod.setAccessible(true);
        // Invoke the private method byteValue to ensure it returns the correct value
        byte byteValue = (byte) byteValueMethod.invoke(mutableByte);
        // Assert that the toByte method returns the correct Byte object
        assertEquals(Byte.valueOf(byteValue), mutableByte.toByte());
    }
}
