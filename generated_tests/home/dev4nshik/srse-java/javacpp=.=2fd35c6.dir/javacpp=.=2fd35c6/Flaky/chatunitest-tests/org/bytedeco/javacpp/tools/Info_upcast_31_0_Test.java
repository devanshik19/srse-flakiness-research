package org.bytedeco.javacpp.tools;

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

class Info_upcast_31_0_Test {

    @Test
    void testUpcast() throws Exception {
        // Create an instance of the Info class
        Info info = new Info();
        // Use reflection to access the private field 'upcast'
        java.lang.reflect.Field upcastField = Info.class.getDeclaredField("upcast");
        upcastField.setAccessible(true);
        // Assert that the initial value of 'upcast' is false
        assertFalse(upcastField.getBoolean(info));
        // Call the upcast method
        Info result = info.upcast();
        // Assert that the upcast method returns the same instance
        assertSame(info, result);
        // Assert that the 'upcast' field is now true
        assertTrue(upcastField.getBoolean(info));
    }
}
