package org.json;

import org.json.JSONObject;
import org.json.XML;
import org.json.XMLParserConfiguration;
import org.json.XMLTokener;
import org.json.JSONException;
import java.io.StringReader;
import java.io.Reader;
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

public class XML_toJSONObject_11_0_Test {

    @Test
    public void testToJSONObjectWithValidXML() throws Exception {
        String xml = "<root><element>value</element></root>";
        Reader reader = new StringReader(xml);
        JSONObject result = XML.toJSONObject(reader);
        assertNotNull(result);
        assertTrue(result.has("root"));
        assertTrue(result.getJSONObject("root").has("element"));
        assertEquals("value", result.getJSONObject("root").getString("element"));
    }

    @Test
    public void testToJSONObjectWithEmptyXML() throws Exception {
        String xml = "";
        Reader reader = new StringReader(xml);
        JSONObject result = XML.toJSONObject(reader);
        assertNotNull(result);
        assertTrue(result.isEmpty());
    }

    @Test
    public void testToJSONObjectWithInvalidXML() {
        String xml = "<root><element>value</element>";
        Reader reader = new StringReader(xml);
        assertThrows(JSONException.class, () -> {
            XML.toJSONObject(reader);
        });
    }

    @Test
    public void testToJSONObjectWithNullReader() {
        assertThrows(NullPointerException.class, () -> {
            XML.toJSONObject((Reader) null);
        });
    }

    @Test
    public void testToJSONObjectWithReflection() throws Exception {
        String xml = "<root><element>value</element></root>";
        Reader reader = new StringReader(xml);
        Method toJSONObjectMethod = XML.class.getDeclaredMethod("toJSONObject", Reader.class, XMLParserConfiguration.class);
        toJSONObjectMethod.setAccessible(true);
        JSONObject result = (JSONObject) toJSONObjectMethod.invoke(null, reader, XMLParserConfiguration.ORIGINAL);
        assertNotNull(result);
        assertTrue(result.has("root"));
        assertTrue(result.getJSONObject("root").has("element"));
        assertEquals("value", result.getJSONObject("root").getString("element"));
    }
}
