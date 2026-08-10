package org.bytedeco.javacpp.tools;

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

public class Info_upcast_32_0_Test {

    @Test
    public void testUpcastMethod() throws Exception {
        // Create an instance of the Info class
        Info info = new Info();
        // Use reflection to access the private field 'upcast'
        java.lang.reflect.Field upcastField = Info.class.getDeclaredField("upcast");
        upcastField.setAccessible(true);
        // Assert that the default value of 'upcast' is false
        assertFalse(upcastField.getBoolean(info));
        // Access the upcast method
        Method upcastMethod = Info.class.getDeclaredMethod("upcast", boolean.class);
        // Invoke the method with true
        upcastMethod.invoke(info, true);
        // Assert that the 'upcast' field is now true
        assertTrue(upcastField.getBoolean(info));
        // Invoke the method with false
        upcastMethod.invoke(info, false);
        // Assert that the 'upcast' field is now false
        assertFalse(upcastField.getBoolean(info));
    }
}
