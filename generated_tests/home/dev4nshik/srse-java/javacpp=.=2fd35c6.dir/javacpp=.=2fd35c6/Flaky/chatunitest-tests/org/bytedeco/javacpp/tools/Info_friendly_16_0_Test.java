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

public class Info_friendly_16_0_Test {

    @Test
    public void testFriendly() throws Exception {
        // Create an instance of Info
        Info info = new Info();
        // Use reflection to get the private field 'friendly'
        Method setFriendlyMethod = Info.class.getDeclaredMethod("friendly", boolean.class);
        setFriendlyMethod.setAccessible(true);
        // Test when friendly is set to true
        setFriendlyMethod.invoke(info, true);
        assertTrue(getFriendlyField(info));
        // Test when friendly is set to false
        setFriendlyMethod.invoke(info, false);
        assertFalse(getFriendlyField(info));
    }

    private boolean getFriendlyField(Info info) throws Exception {
        // Use reflection to access the private field 'friendly'
        java.lang.reflect.Field friendlyField = Info.class.getDeclaredField("friendly");
        friendlyField.setAccessible(true);
        return friendlyField.getBoolean(info);
    }
}
