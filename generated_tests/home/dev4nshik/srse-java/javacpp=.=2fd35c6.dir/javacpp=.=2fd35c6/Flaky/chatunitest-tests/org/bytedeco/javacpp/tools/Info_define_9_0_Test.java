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

public class Info_define_9_0_Test {

    @Test
    public void testDefine() throws Exception {
        // Create an instance of the Info class
        Info info = new Info();
        // Use reflection to access the private field 'define'
        java.lang.reflect.Field defineField = Info.class.getDeclaredField("define");
        defineField.setAccessible(true);
        // Verify the initial state of the 'define' field
        assertFalse(defineField.getBoolean(info), "Initially, 'define' should be false.");
        // Invoke the define() method
        Info result = info.define();
        // Check that the method returns the same instance
        assertSame(info, result, "The define() method should return the same instance.");
        // Verify that the 'define' field is now true
        assertTrue(defineField.getBoolean(info), "After calling define(), 'define' should be true.");
    }
}
