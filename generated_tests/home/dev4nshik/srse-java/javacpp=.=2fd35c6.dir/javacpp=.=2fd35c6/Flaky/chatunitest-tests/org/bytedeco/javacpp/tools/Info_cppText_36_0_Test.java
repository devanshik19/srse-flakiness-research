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

public class Info_cppText_36_0_Test {

    @Test
    public void testCppText() throws NoSuchFieldException, IllegalAccessException {
        // Arrange
        Info info = new Info();
        String expectedCppText = "sampleCppText";
        // Act
        Info result = info.cppText(expectedCppText);
        // Assert
        assertNotNull(result);
        assertEquals(info, result);
        // Use reflection to access the private field
        java.lang.reflect.Field cppTextField = Info.class.getDeclaredField("cppText");
        cppTextField.setAccessible(true);
        String actualCppText = (String) cppTextField.get(info);
        assertEquals(expectedCppText, actualCppText);
    }
}
