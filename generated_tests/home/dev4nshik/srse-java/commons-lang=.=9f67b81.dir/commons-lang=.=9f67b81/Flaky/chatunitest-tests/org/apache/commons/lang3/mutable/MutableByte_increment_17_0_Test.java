package org.apache.commons.lang3.mutable;

import java.lang.reflect.Field;
import org.apache.commons.lang3.mutable.MutableByte;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_increment_17_0_Test {

    private MutableByte mutableByte;

    @BeforeEach
    public void setUp() {
        mutableByte = new MutableByte((byte) 0);
    }

    @Test
    public void testIncrement() throws NoSuchFieldException, IllegalAccessException {
        // Using reflection to access the private 'value' field
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        // Initial value check
        byte initialValue = (byte) valueField.get(mutableByte);
        assertEquals(0, initialValue);
        // Increment the value
        mutableByte.increment();
        // Verify the incremented value
        byte incrementedValue = (byte) valueField.get(mutableByte);
        assertEquals(1, incrementedValue);
    }
}
