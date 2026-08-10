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

public class Info_flatten_13_0_Test {

    @Test
    public void testFlatten() throws Exception {
        // Create an instance of the Info class
        Info info = new Info();
        // Use reflection to access the private field 'flatten' before calling flatten()
        java.lang.reflect.Field flattenField = Info.class.getDeclaredField("flatten");
        flattenField.setAccessible(true);
        assertFalse(flattenField.getBoolean(info), "Initially, 'flatten' should be false.");
        // Call the flatten() method
        Info result = info.flatten();
        // Verify that the returned object is the same instance
        assertSame(info, result, "The returned object should be the same instance.");
        // Use reflection to check that the 'flatten' field is set to true
        assertTrue(flattenField.getBoolean(info), "After calling flatten(), 'flatten' should be true.");
    }
}
