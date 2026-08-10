package org.bytedeco.javacpp.tools;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.bytedeco.javacpp.Pointer;
import org.bytedeco.javacpp.annotation.ByVal;
import org.bytedeco.javacpp.annotation.Cast;
import org.bytedeco.javacpp.annotation.Virtual;

public class Info_define_10_0_Test {

    @Test
    public void testDefineWithTrue() throws Exception {
        // Create an instance of Info
        Info info = new Info();
        // Use reflection to access the private method 'define'
        Method defineMethod = Info.class.getDeclaredMethod("define", boolean.class);
        defineMethod.setAccessible(true);
        // Invoke the method with 'true'
        Info result = (Info) defineMethod.invoke(info, true);
        // Use reflection to access the private field 'define'
        Field defineField = Info.class.getDeclaredField("define");
        defineField.setAccessible(true);
        // Check if the 'define' field is set to true
        assertEquals(true, defineField.getBoolean(info));
        // Check if the method returns the same instance
        assertEquals(info, result);
    }

    @Test
    public void testDefineWithFalse() throws Exception {
        // Create an instance of Info
        Info info = new Info();
        // Use reflection to access the private method 'define'
        Method defineMethod = Info.class.getDeclaredMethod("define", boolean.class);
        defineMethod.setAccessible(true);
        // Invoke the method with 'false'
        Info result = (Info) defineMethod.invoke(info, false);
        // Use reflection to access the private field 'define'
        Field defineField = Info.class.getDeclaredField("define");
        defineField.setAccessible(true);
        // Check if the 'define' field is set to false
        assertEquals(false, defineField.getBoolean(info));
        // Check if the method returns the same instance
        assertEquals(info, result);
    }
}
