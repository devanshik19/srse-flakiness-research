package org.bytedeco.javacpp.tools;

import org.bytedeco.javacpp.tools.Info;
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

public class Info_linePatterns_6_0_Test {

    @Test
    public void testLinePatterns() {
        // Create an instance of the Info class
        Info info = new Info();
        // Define test data
        String[] testPatterns = { "pattern1", "pattern2", "pattern3" };
        // Invoke the linePatterns method
        Info result = info.linePatterns(testPatterns);
        // Use reflection to access the private field linePatterns
        try {
            java.lang.reflect.Field field = Info.class.getDeclaredField("linePatterns");
            field.setAccessible(true);
            String[] linePatternsField = (String[]) field.get(info);
            // Verify that the linePatterns field is correctly set
            assertArrayEquals(testPatterns, linePatternsField);
            // Verify that the method returns the same instance
            assertSame(info, result);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            fail("Reflection failed: " + e.getMessage());
        }
    }
}
