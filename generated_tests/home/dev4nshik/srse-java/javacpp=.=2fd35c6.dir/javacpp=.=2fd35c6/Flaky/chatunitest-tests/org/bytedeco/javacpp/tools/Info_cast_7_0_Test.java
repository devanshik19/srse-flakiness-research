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

public class Info_cast_7_0_Test {

    @Test
    public void testCast() throws Exception {
        // Create an instance of Info
        Info info = new Info();
        // Use reflection to access the private field 'cast'
        java.lang.reflect.Field castField = Info.class.getDeclaredField("cast");
        castField.setAccessible(true);
        // Ensure the initial value of 'cast' is false
        assertFalse(castField.getBoolean(info));
        // Call the cast() method
        Info result = info.cast();
        // Verify that the method returns the same instance
        assertSame(info, result);
        // Verify that the 'cast' field is now true
        assertTrue(castField.getBoolean(info));
    }
}
