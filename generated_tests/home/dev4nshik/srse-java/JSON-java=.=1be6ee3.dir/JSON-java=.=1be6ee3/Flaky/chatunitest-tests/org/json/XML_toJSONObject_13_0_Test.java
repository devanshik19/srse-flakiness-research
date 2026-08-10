package org.json;

import org.json.JSONObject;
import org.json.XML;
import org.json.XMLParserConfiguration;
import org.json.XMLTokener;
import org.json.JSONException;
import java.io.StringReader;
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

public class XML_toJSONObject_13_0_Test {

    @Test
    public void testToJSONObjectWithValidXML() throws Exception {
        String xml = "<root><child>value</child></root>";
        StringReader reader = new StringReader(xml);
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        JSONObject result = XML.toJSONObject(reader, config);
        assertNotNull(result);
        assertTrue(result.has("root"));
        assertTrue(result.getJSONObject("root").has("child"));
        assertEquals("value", result.getJSONObject("root").getString("child"));
    }

    @Test
    public void testToJSONObjectWithEmptyXML() throws Exception {
        String xml = "";
        StringReader reader = new StringReader(xml);
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        JSONObject result = XML.toJSONObject(reader, config);
        assertNotNull(result);
        assertEquals(0, result.length());
    }

    @Test
    public void testToJSONObjectWithComplexXML() throws Exception {
        String xml = "<root><child attr=\"value\">text</child><empty /></root>";
        StringReader reader = new StringReader(xml);
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        JSONObject result = XML.toJSONObject(reader, config);
        assertNotNull(result);
        assertTrue(result.has("root"));
        JSONObject root = result.getJSONObject("root");
        assertTrue(root.has("child"));
        assertEquals("text", root.getJSONObject("child").getString("content"));
        assertEquals("value", root.getJSONObject("child").getString("attr"));
        assertTrue(root.has("empty"));
    }

    @Test
    public void testToJSONObjectWithInvalidXML() {
        String xml = "<root><child></root>";
        StringReader reader = new StringReader(xml);
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        assertThrows(JSONException.class, () -> {
            XML.toJSONObject(reader, config);
        });
    }
}
