package org.json;

import org.json.XML;
import org.json.JSONObject;
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

public class XML_stringToValue_7_0_Test {

    @Test
    public void testStringToValueEmptyString() {
        assertEquals("", XML.stringToValue(""));
    }

    @Test
    public void testStringToValueTrue() {
        assertEquals(Boolean.TRUE, XML.stringToValue("true"));
        assertEquals(Boolean.TRUE, XML.stringToValue("TRUE"));
    }

    @Test
    public void testStringToValueFalse() {
        assertEquals(Boolean.FALSE, XML.stringToValue("false"));
        assertEquals(Boolean.FALSE, XML.stringToValue("FALSE"));
    }

    @Test
    public void testStringToValueNull() {
        assertEquals(JSONObject.NULL, XML.stringToValue("null"));
        assertEquals(JSONObject.NULL, XML.stringToValue("NULL"));
    }

    @Test
    public void testStringToValueNumber() {
        assertEquals(123, XML.stringToValue("123"));
        assertEquals(-123, XML.stringToValue("-123"));
        assertEquals(new BigDecimal("123.45"), XML.stringToValue("123.45"));
        assertEquals(Double.valueOf(-0.0), XML.stringToValue("-0.0"));
    }

    @Test
    public void testStringToValueInvalidNumber() {
        assertEquals("0123", XML.stringToValue("0123"));
        assertEquals("-0123", XML.stringToValue("-0123"));
    }

    @Test
    public void testStringToValueString() {
        assertEquals("abc", XML.stringToValue("abc"));
    }

    @Test
    public void testStringToNumberReflection() throws Exception {
        Method method = XML.class.getDeclaredMethod("stringToNumber", String.class);
        method.setAccessible(true);
        assertEquals(123, method.invoke(null, "123"));
        assertEquals(new BigDecimal("123.45"), method.invoke(null, "123.45"));
        assertEquals(Double.valueOf(-0.0), method.invoke(null, "-0.0"));
        assertThrows(NumberFormatException.class, () -> method.invoke(null, "0123"));
        assertThrows(NumberFormatException.class, () -> method.invoke(null, "-0123"));
    }
}
