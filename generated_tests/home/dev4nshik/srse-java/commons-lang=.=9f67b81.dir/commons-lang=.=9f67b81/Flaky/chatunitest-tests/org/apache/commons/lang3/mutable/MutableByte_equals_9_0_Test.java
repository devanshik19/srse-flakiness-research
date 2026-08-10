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

public class MutableByte_equals_9_0_Test {

    @Test
    public void testEquals_SameObject() throws Exception {
        MutableByte mutableByte = new MutableByte((byte) 5);
        Method equalsMethod = MutableByte.class.getDeclaredMethod("equals", Object.class);
        equalsMethod.setAccessible(true);
        assertTrue((boolean) equalsMethod.invoke(mutableByte, mutableByte));
    }

    @Test
    public void testEquals_EqualValues() throws Exception {
        MutableByte mutableByte1 = new MutableByte((byte) 5);
        MutableByte mutableByte2 = new MutableByte((byte) 5);
        Method equalsMethod = MutableByte.class.getDeclaredMethod("equals", Object.class);
        equalsMethod.setAccessible(true);
        assertTrue((boolean) equalsMethod.invoke(mutableByte1, mutableByte2));
    }

    @Test
    public void testEquals_DifferentValues() throws Exception {
        MutableByte mutableByte1 = new MutableByte((byte) 5);
        MutableByte mutableByte2 = new MutableByte((byte) 10);
        Method equalsMethod = MutableByte.class.getDeclaredMethod("equals", Object.class);
        equalsMethod.setAccessible(true);
        assertFalse((boolean) equalsMethod.invoke(mutableByte1, mutableByte2));
    }

    @Test
    public void testEquals_DifferentClass() throws Exception {
        MutableByte mutableByte = new MutableByte((byte) 5);
        Object otherObject = new Object();
        Method equalsMethod = MutableByte.class.getDeclaredMethod("equals", Object.class);
        equalsMethod.setAccessible(true);
        assertFalse((boolean) equalsMethod.invoke(mutableByte, otherObject));
    }
}
