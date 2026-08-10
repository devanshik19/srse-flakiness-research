package org.json;

import org.json.XML;
import org.json.XMLXsiTypeConverter;
import java.lang.reflect.Method;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.Reader;
import java.io.StringReader;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Iterator;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import /*
Public Domain.
*/
java.io.Reader;

public class XML_stringToValue_6_0_Test {

    private XML xmlInstance;

    @BeforeEach
    public void setUp() {
        xmlInstance = new XML();
    }

    @Test
    public void testStringToValueWithTypeConverter() {
        XMLXsiTypeConverter<Integer> converter = new XMLXsiTypeConverter<Integer>() {

            @Override
            public Integer convert(String value) {
                return Integer.parseInt(value);
            }
        };
        Object result = XML.stringToValue("123", converter);
        assertEquals(123, result);
    }

    @Test
    public void testStringToValueWithoutTypeConverter_EmptyString() throws Exception {
        Method stringToValueMethod = XML.class.getDeclaredMethod("stringToValue", String.class);
        stringToValueMethod.setAccessible(true);
        Object result = stringToValueMethod.invoke(null, "");
        assertEquals("", result);
    }

    @Test
    public void testStringToValueWithoutTypeConverter_TrueString() throws Exception {
        Method stringToValueMethod = XML.class.getDeclaredMethod("stringToValue", String.class);
        stringToValueMethod.setAccessible(true);
        Object result = stringToValueMethod.invoke(null, "true");
        assertEquals(Boolean.TRUE, result);
    }

    @Test
    public void testStringToValueWithoutTypeConverter_FalseString() throws Exception {
        Method stringToValueMethod = XML.class.getDeclaredMethod("stringToValue", String.class);
        stringToValueMethod.setAccessible(true);
        Object result = stringToValueMethod.invoke(null, "false");
        assertEquals(Boolean.FALSE, result);
    }

    @Test
    public void testStringToValueWithoutTypeConverter_NullString() throws Exception {
        Method stringToValueMethod = XML.class.getDeclaredMethod("stringToValue", String.class);
        stringToValueMethod.setAccessible(true);
        Object result = stringToValueMethod.invoke(null, "null");
        assertNull(result);
    }

    @Test
    public void testStringToValueWithoutTypeConverter_NumberString() throws Exception {
        Method stringToValueMethod = XML.class.getDeclaredMethod("stringToValue", String.class);
        stringToValueMethod.setAccessible(true);
        Object result = stringToValueMethod.invoke(null, "123");
        assertEquals(123, result);
    }

    @Test
    public void testStringToValueWithoutTypeConverter_NonNumberString() throws Exception {
        Method stringToValueMethod = XML.class.getDeclaredMethod("stringToValue", String.class);
        stringToValueMethod.setAccessible(true);
        Object result = stringToValueMethod.invoke(null, "Hello");
        assertEquals("Hello", result);
    }
}
