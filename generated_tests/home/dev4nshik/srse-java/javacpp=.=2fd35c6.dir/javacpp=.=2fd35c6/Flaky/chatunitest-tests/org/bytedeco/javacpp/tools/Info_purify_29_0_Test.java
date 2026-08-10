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

public class Info_purify_29_0_Test {

    @Test
    public void testPurify() throws Exception {
        // Creating an instance of the Info class
        Info info = new Info();
        // Using reflection to access the private method 'purify'
        Method purifyMethod = Info.class.getDeclaredMethod("purify");
        purifyMethod.setAccessible(true);
        // Invoke the purify method
        Info result = (Info) purifyMethod.invoke(info);
        // Assert that the purify method returns the same instance (this)
        assertEquals(info, result);
        // Using reflection to access the private field 'purify'
        Field purifyField = Info.class.getDeclaredField("purify");
        purifyField.setAccessible(true);
        // Check if the purify field is set to true
        boolean purifyValue = (boolean) purifyField.get(info);
        assertTrue(purifyValue);
    }
}
