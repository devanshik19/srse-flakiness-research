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

public class Info_javaNames_1_0_Test {

    @Test
    public void testJavaNames() {
        // Create an instance of the Info class
        Info info = new Info();
        // Test with a single java name
        String[] singleJavaName = { "com.example.MyClass" };
        Info result = info.javaNames(singleJavaName);
        // Assert that the returned object is the same instance
        assertSame(info, result);
        // Access the private field javaNames using reflection
        try {
            java.lang.reflect.Field javaNamesField = Info.class.getDeclaredField("javaNames");
            javaNamesField.setAccessible(true);
            String[] javaNames = (String[]) javaNamesField.get(info);
            // Assert that the javaNames field is correctly set
            assertArrayEquals(singleJavaName, javaNames);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            fail("Reflection failed: " + e.getMessage());
        }
        // Test with multiple java names
        String[] multipleJavaNames = { "com.example.MyClass", "com.example.AnotherClass" };
        result = info.javaNames(multipleJavaNames);
        // Assert that the returned object is the same instance
        assertSame(info, result);
        // Access the private field javaNames using reflection again
        try {
            java.lang.reflect.Field javaNamesField = Info.class.getDeclaredField("javaNames");
            javaNamesField.setAccessible(true);
            String[] javaNames = (String[]) javaNamesField.get(info);
            // Assert that the javaNames field is correctly set
            assertArrayEquals(multipleJavaNames, javaNames);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            fail("Reflection failed: " + e.getMessage());
        }
        // Test with no java names (empty array)
        String[] emptyJavaNames = {};
        result = info.javaNames(emptyJavaNames);
        // Assert that the returned object is the same instance
        assertSame(info, result);
        // Access the private field javaNames using reflection again
        try {
            java.lang.reflect.Field javaNamesField = Info.class.getDeclaredField("javaNames");
            javaNamesField.setAccessible(true);
            String[] javaNames = (String[]) javaNamesField.get(info);
            // Assert that the javaNames field is correctly set
            assertArrayEquals(emptyJavaNames, javaNames);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            fail("Reflection failed: " + e.getMessage());
        }
    }
}
