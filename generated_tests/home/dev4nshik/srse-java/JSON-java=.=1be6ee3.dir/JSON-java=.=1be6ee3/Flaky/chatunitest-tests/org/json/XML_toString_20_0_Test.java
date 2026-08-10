package org.json;

import org.json.XML;
import org.json.JSONException;
import org.json.XMLParserConfiguration;
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

public class XML_toString_20_0_Test {

    @Test
    void testToStringWithNullObject() {
        try {
            Method toStringMethod = XML.class.getDeclaredMethod("toString", Object.class, int.class);
            toStringMethod.setAccessible(true);
            Object result = toStringMethod.invoke(null, null, 2);
            assertNotNull(result);
            assertTrue(result instanceof String);
            assertEquals("", result);
        } catch (Exception e) {
            fail("Exception occurred: " + e.getMessage());
        }
    }

    @Test
    void testToStringWithNonNullObject() {
        try {
            Method toStringMethod = XML.class.getDeclaredMethod("toString", Object.class, int.class);
            toStringMethod.setAccessible(true);
            String testString = "test";
            Object result = toStringMethod.invoke(null, testString, 2);
            assertNotNull(result);
            assertTrue(result instanceof String);
            assertTrue(((String) result).contains(testString));
        } catch (Exception e) {
            fail("Exception occurred: " + e.getMessage());
        }
    }

    @Test
    void testToStringWithNegativeIndent() {
        try {
            Method toStringMethod = XML.class.getDeclaredMethod("toString", Object.class, int.class);
            toStringMethod.setAccessible(true);
            String testString = "test";
            Object result = toStringMethod.invoke(null, testString, -1);
            assertNotNull(result);
            assertTrue(result instanceof String);
            assertTrue(((String) result).contains(testString));
        } catch (Exception e) {
            fail("Exception occurred: " + e.getMessage());
        }
    }
}
