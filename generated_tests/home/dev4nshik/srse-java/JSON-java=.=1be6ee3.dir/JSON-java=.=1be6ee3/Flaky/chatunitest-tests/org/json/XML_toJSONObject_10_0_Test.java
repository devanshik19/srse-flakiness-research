package org.json;

import org.json.JSONObject;
import org.json.XML;
import org.json.XMLParserConfiguration;
import org.json.JSONException;
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

class XML_toJSONObject_10_0_Test {

    @Test
    void testToJSONObjectWithValidXML() {
        String xmlString = "<root><child>value</child></root>";
        try {
            JSONObject jsonObject = XML.toJSONObject(xmlString);
            assertNotNull(jsonObject);
            assertTrue(jsonObject.has("root"));
            assertTrue(jsonObject.getJSONObject("root").has("child"));
            assertEquals("value", jsonObject.getJSONObject("root").getString("child"));
        } catch (JSONException e) {
            fail("JSONException was thrown: " + e.getMessage());
        }
    }

    @Test
    void testToJSONObjectWithEmptyString() {
        String xmlString = "";
        try {
            JSONObject jsonObject = XML.toJSONObject(xmlString);
            assertNotNull(jsonObject);
            assertTrue(jsonObject.isEmpty());
        } catch (JSONException e) {
            fail("JSONException was thrown: " + e.getMessage());
        }
    }

    @Test
    void testToJSONObjectWithInvalidXML() {
        String xmlString = "<root><child>value</root>";
        assertThrows(JSONException.class, () -> {
            XML.toJSONObject(xmlString);
        });
    }

    @Test
    void testToJSONObjectWithNullString() {
        String xmlString = null;
        assertThrows(NullPointerException.class, () -> {
            XML.toJSONObject(xmlString);
        });
    }
}
