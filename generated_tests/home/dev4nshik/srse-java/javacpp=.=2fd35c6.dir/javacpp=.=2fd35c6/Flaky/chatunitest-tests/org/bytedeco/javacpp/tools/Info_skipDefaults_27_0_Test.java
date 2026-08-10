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

public class Info_skipDefaults_27_0_Test {

    @Test
    public void testSkipDefaults() throws Exception {
        // Create an instance of the Info class
        Info info = new Info();
        // Use reflection to access the private field 'skipDefaults'
        Method skipDefaultsMethod = Info.class.getDeclaredMethod("skipDefaults");
        skipDefaultsMethod.setAccessible(true);
        // Invoke the skipDefaults method
        Object result = skipDefaultsMethod.invoke(info);
        // Assert that the returned object is the same instance
        assertSame(info, result);
        // Use reflection to access the private field 'skipDefaults'
        java.lang.reflect.Field skipDefaultsField = Info.class.getDeclaredField("skipDefaults");
        skipDefaultsField.setAccessible(true);
        // Assert that the skipDefaults field is set to true
        assertTrue(skipDefaultsField.getBoolean(info));
    }
}
