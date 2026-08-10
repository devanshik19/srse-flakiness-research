package org.json;

import org.json.JSONObject;
import org.json.XML;
import org.json.JSONException;
import org.json.XMLParserConfiguration;
import java.io.Reader;
import java.io.StringReader;
import java.lang.reflect.InvocationTargetException;
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
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Iterator;

public class XML_toJSONObject_14_0_Test {

    @Test
    public void testToJSONObjectWithKeepStringsTrue() {
        String xmlString = "<root><child>value</child></root>";
        try {
            JSONObject jsonObject = XML.toJSONObject(xmlString, true);
            assertNotNull(jsonObject);
            assertEquals("value", jsonObject.getJSONObject("root").get("child"));
        } catch (JSONException e) {
            fail("JSONException was thrown: " + e.getMessage());
        }
    }

    @Test
    public void testToJSONObjectWithKeepStringsFalse() {
        String xmlString = "<root><child>value</child></root>";
        try {
            JSONObject jsonObject = XML.toJSONObject(xmlString, false);
            assertNotNull(jsonObject);
            assertEquals("value", jsonObject.getJSONObject("root").get("child"));
        } catch (JSONException e) {
            fail("JSONException was thrown: " + e.getMessage());
        }
    }

    @Test
    public void testToJSONObjectWithEmptyString() {
        String xmlString = "";
        try {
            JSONObject jsonObject = XML.toJSONObject(xmlString, false);
            assertNotNull(jsonObject);
            assertTrue(jsonObject.isEmpty());
        } catch (JSONException e) {
            fail("JSONException was thrown: " + e.getMessage());
        }
    }

    @Test
    public void testToJSONObjectWithInvalidXML() {
        String xmlString = "<root><child>value</child>";
        assertThrows(JSONException.class, () -> {
            XML.toJSONObject(xmlString, false);
        });
    }

    @Test
    public void testPrivateToJSONObjectMethod() {
        String xmlString = "<root><child>value</child></root>";
        try {
            Method method = XML.class.getDeclaredMethod("toJSONObject", Reader.class, boolean.class);
            method.setAccessible(true);
            JSONObject jsonObject = (JSONObject) method.invoke(null, new StringReader(xmlString), true);
            assertNotNull(jsonObject);
            assertEquals("value", jsonObject.getJSONObject("root").get("child"));
        } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
            fail("Exception was thrown: " + e.getMessage());
        }
    }
}
