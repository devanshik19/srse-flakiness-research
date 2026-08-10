package org.json;

import org.json.XML;
import org.json.XMLParserConfiguration;
import org.json.JSONException;
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

public class XML_toString_17_0_Test {

    @Test
    public void testToStringWithValidInput() throws Exception {
        // Arrange
        Object object = "SampleText";
        String tagName = "tag";
        // Act
        Method method = XML.class.getDeclaredMethod("toString", Object.class, String.class);
        method.setAccessible(true);
        String result = (String) method.invoke(null, object, tagName);
        // Assert
        String expectedResult = XML.toString(object, tagName, XMLParserConfiguration.ORIGINAL);
        assertEquals(expectedResult, result);
    }

    @Test
    public void testToStringWithNullObject() throws Exception {
        // Arrange
        Object object = null;
        String tagName = "tag";
        // Act
        Method method = XML.class.getDeclaredMethod("toString", Object.class, String.class);
        method.setAccessible(true);
        String result = (String) method.invoke(null, object, tagName);
        // Assert
        String expectedResult = XML.toString(object, tagName, XMLParserConfiguration.ORIGINAL);
        assertEquals(expectedResult, result);
    }

    @Test
    public void testToStringWithEmptyTagName() throws Exception {
        // Arrange
        Object object = "SampleText";
        String tagName = "";
        // Act
        Method method = XML.class.getDeclaredMethod("toString", Object.class, String.class);
        method.setAccessible(true);
        String result = (String) method.invoke(null, object, tagName);
        // Assert
        String expectedResult = XML.toString(object, tagName, XMLParserConfiguration.ORIGINAL);
        assertEquals(expectedResult, result);
    }
}
