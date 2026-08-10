package org.json;

import org.junit.jupiter.api.function.Executable;
import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import /*
Public Domain.
*/
java.io.Reader;
import java.io.StringReader;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Iterator;

public class XML_noSpace_4_0_Test {

    @Test
    public void testNoSpaceWithValidString() throws Exception {
        // Arrange
        String validString = "NoSpaceHere";
        // Act & Assert
        assertDoesNotThrow(() -> {
            Method method = XML.class.getDeclaredMethod("noSpace", String.class);
            method.setAccessible(true);
            method.invoke(null, validString);
        });
    }

    @Test
    public void testNoSpaceWithEmptyString() throws Exception {
        // Arrange
        String emptyString = "";
        // Act
        Executable executable = () -> {
            Method method = XML.class.getDeclaredMethod("noSpace", String.class);
            method.setAccessible(true);
            method.invoke(null, emptyString);
        };
        // Assert
        Exception exception = assertThrows(Exception.class, executable);
        assertTrue(exception.getCause() instanceof JSONException);
        assertEquals("Empty string.", exception.getCause().getMessage());
    }

    @Test
    public void testNoSpaceWithWhitespaceString() throws Exception {
        // Arrange
        String whitespaceString = "Contains Space";
        // Act
        Executable executable = () -> {
            Method method = XML.class.getDeclaredMethod("noSpace", String.class);
            method.setAccessible(true);
            method.invoke(null, whitespaceString);
        };
        // Assert
        Exception exception = assertThrows(Exception.class, executable);
        assertTrue(exception.getCause() instanceof JSONException);
        assertEquals("'Contains Space' contains a space character.", exception.getCause().getMessage());
    }
}
