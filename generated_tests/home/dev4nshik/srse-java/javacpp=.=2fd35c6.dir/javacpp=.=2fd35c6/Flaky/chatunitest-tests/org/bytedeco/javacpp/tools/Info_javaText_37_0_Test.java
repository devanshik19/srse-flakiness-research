package org.bytedeco.javacpp.tools;

import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;
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

public class Info_javaText_37_0_Test {

    @Test
    public void testJavaText() {
        // Create an instance of Info
        Info info = new Info();
        // Test setting a javaText value
        String testJavaText = "Sample Java Text";
        Info result = info.javaText(testJavaText);
        // Assert that the method returns the same Info instance
        assertSame(info, result);
        // Use reflection to access the private javaText field
        try {
            Method javaTextMethod = Info.class.getDeclaredMethod("javaText", String.class);
            javaTextMethod.setAccessible(true);
            // Invoke the method and check the field value
            javaTextMethod.invoke(info, testJavaText);
            assertEquals(testJavaText, info.javaText);
        } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
            fail("Reflection failed: " + e.getMessage());
        }
    }
}
