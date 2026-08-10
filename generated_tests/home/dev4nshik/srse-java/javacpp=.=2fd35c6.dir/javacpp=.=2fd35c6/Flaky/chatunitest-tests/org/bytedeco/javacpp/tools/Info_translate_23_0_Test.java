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

public class Info_translate_23_0_Test {

    @Test
    public void testTranslate() throws Exception {
        // Create an instance of the Info class
        Info info = new Info();
        // Use reflection to access the private field 'translate'
        Method translateMethod = Info.class.getDeclaredMethod("translate");
        translateMethod.setAccessible(true);
        // Invoke the translate method
        Info result = (Info) translateMethod.invoke(info);
        // Check if the method returns the same instance
        assertSame(info, result, "The translate method should return the same instance.");
        // Use reflection to access the private field 'translate'
        java.lang.reflect.Field translateField = Info.class.getDeclaredField("translate");
        translateField.setAccessible(true);
        // Check if the translate field is set to true
        assertTrue((boolean) translateField.get(info), "The translate field should be set to true.");
    }
}
