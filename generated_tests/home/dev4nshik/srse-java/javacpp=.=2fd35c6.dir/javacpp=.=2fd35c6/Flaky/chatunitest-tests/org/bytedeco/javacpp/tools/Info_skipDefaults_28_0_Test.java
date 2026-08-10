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

public class Info_skipDefaults_28_0_Test {

    @Test
    public void testSkipDefaults() throws Exception {
        // Create an instance of Info
        Info info = new Info();
        // Use reflection to access the private field 'skipDefaults'
        Method skipDefaultsMethod = Info.class.getDeclaredMethod("skipDefaults", boolean.class);
        // Test setting skipDefaults to true
        skipDefaultsMethod.invoke(info, true);
        assertEquals(true, getSkipDefaults(info), "The skipDefaults should be set to true");
        // Test setting skipDefaults to false
        skipDefaultsMethod.invoke(info, false);
        assertEquals(false, getSkipDefaults(info), "The skipDefaults should be set to false");
    }

    // Helper method to access the private field 'skipDefaults' using reflection
    private boolean getSkipDefaults(Info info) throws Exception {
        java.lang.reflect.Field skipDefaultsField = Info.class.getDeclaredField("skipDefaults");
        skipDefaultsField.setAccessible(true);
        return skipDefaultsField.getBoolean(info);
    }
}
