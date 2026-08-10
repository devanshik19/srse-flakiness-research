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

public class Info_translate_24_0_Test {

    @Test
    public void testTranslateTrue() throws Exception {
        // Arrange
        Info info = new Info();
        // Act
        Info result = info.translate(true);
        // Assert
        assertNotNull(result);
        assertEquals(info, result);
        // Using reflection to access the private field 'translate'
        Field translateField = Info.class.getDeclaredField("translate");
        translateField.setAccessible(true);
        boolean translateValue = (boolean) translateField.get(info);
        assertTrue(translateValue);
    }

    @Test
    public void testTranslateFalse() throws Exception {
        // Arrange
        Info info = new Info();
        // Act
        Info result = info.translate(false);
        // Assert
        assertNotNull(result);
        assertEquals(info, result);
        // Using reflection to access the private field 'translate'
        Field translateField = Info.class.getDeclaredField("translate");
        translateField.setAccessible(true);
        boolean translateValue = (boolean) translateField.get(info);
        assertFalse(translateValue);
    }
}
