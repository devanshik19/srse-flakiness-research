package org.bytedeco.javacpp.tools;

import java.lang.reflect.Field;
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

public class Info_immutable_17_0_Test {

    @Test
    public void testImmutable() throws NoSuchFieldException, IllegalAccessException {
        // Create an instance of Info
        Info info = new Info();
        // Invoke the immutable method
        Info result = info.immutable();
        // Use reflection to access the private field 'immutable'
        Field immutableField = Info.class.getDeclaredField("immutable");
        immutableField.setAccessible(true);
        // Assert that the immutable field is set to true
        assertTrue(immutableField.getBoolean(info));
        // Assert that the method returns the same instance (this)
        assertSame(info, result);
    }
}
