package org.apache.commons.lang3.mutable;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.commons.lang3.math.NumberUtils;

public class MutableByte_doubleValue_8_0_Test {

    @Test
    public void testDoubleValueDefaultConstructor() throws Exception {
        // Use reflection to create an instance of MutableByte
        Constructor<?> constructor = MutableByte.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        Object mutableByte = constructor.newInstance();
        // Use reflection to invoke the doubleValue method
        Method doubleValueMethod = MutableByte.class.getDeclaredMethod("doubleValue");
        doubleValueMethod.setAccessible(true);
        double result = (double) doubleValueMethod.invoke(mutableByte);
        // Assert that the double value is 0.0 by default
        assertEquals(0.0, result);
    }

    @Test
    public void testDoubleValueParameterizedConstructor() throws Exception {
        // Use reflection to create an instance of MutableByte with a specific value
        Constructor<?> constructor = MutableByte.class.getDeclaredConstructor(byte.class);
        constructor.setAccessible(true);
        byte testValue = 5;
        Object mutableByte = constructor.newInstance(testValue);
        // Use reflection to invoke the doubleValue method
        Method doubleValueMethod = MutableByte.class.getDeclaredMethod("doubleValue");
        doubleValueMethod.setAccessible(true);
        double result = (double) doubleValueMethod.invoke(mutableByte);
        // Assert that the double value matches the set byte value
        assertEquals(5.0, result);
    }

    @Test
    public void testDoubleValueWithReflection() throws Exception {
        // Use reflection to create an instance of MutableByte
        Constructor<?> constructor = MutableByte.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        Object mutableByte = constructor.newInstance();
        // Use reflection to set the private field 'value'
        Field valueField = MutableByte.class.getDeclaredField("value");
        valueField.setAccessible(true);
        byte testValue = 10;
        valueField.set(mutableByte, testValue);
        // Use reflection to invoke the doubleValue method
        Method doubleValueMethod = MutableByte.class.getDeclaredMethod("doubleValue");
        doubleValueMethod.setAccessible(true);
        double result = (double) doubleValueMethod.invoke(mutableByte);
        // Assert that the double value matches the set byte value
        assertEquals(10.0, result);
    }
}
