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

class Info_skip_25_0_Test {

    @Test
    void testSkipMethod() throws Exception {
        // Create an instance of Info
        Info info = new Info();
        // Use reflection to access the skip() method
        Method skipMethod = Info.class.getDeclaredMethod("skip");
        skipMethod.setAccessible(true);
        // Invoke the skip() method
        Info result = (Info) skipMethod.invoke(info);
        // Check that the returned object is the same instance
        assertSame(info, result);
        // Use reflection to access the private field 'skip'
        java.lang.reflect.Field skipField = Info.class.getDeclaredField("skip");
        skipField.setAccessible(true);
        // Verify that the 'skip' field is set to true
        assertTrue(skipField.getBoolean(info));
    }
}
