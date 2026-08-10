package org.bytedeco.javacpp.tools;

import org.bytedeco.javacpp.tools.Info;
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

public class Info_enumerate_11_0_Test {

    @Test
    public void testEnumerate() throws NoSuchFieldException, IllegalAccessException {
        // Create an instance of the Info class
        Info info = new Info();
        // Invoke the enumerate() method
        info.enumerate();
        // Use reflection to access the private field 'enumerate'
        Field enumerateField = Info.class.getDeclaredField("enumerate");
        enumerateField.setAccessible(true);
        // Assert that the 'enumerate' field is set to true
        assertTrue(enumerateField.getBoolean(info), "The enumerate field should be set to true.");
    }
}
