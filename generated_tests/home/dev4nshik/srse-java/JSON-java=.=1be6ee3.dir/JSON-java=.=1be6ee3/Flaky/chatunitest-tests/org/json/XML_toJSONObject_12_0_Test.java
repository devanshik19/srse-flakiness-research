package org.json;

import org.json.JSONException;
import org.json.JSONObject;
import org.json.XML;
import org.json.XMLParserConfiguration;
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

public class XML_toJSONObject_12_0_Test {

    @Test
    public void testToJSONObjectKeepStringsTrue() throws Exception {
        String xmlData = "<root><element>value</element></root>";
        StringReader reader = new StringReader(xmlData);
        JSONObject result = invokeToJSONObject(reader, true);
        assertNotNull(result);
        assertTrue(result.has("root"));
        assertEquals("value", result.getJSONObject("root").getString("element"));
    }

    @Test
    public void testToJSONObjectKeepStringsFalse() throws Exception {
        String xmlData = "<root><element>value</element></root>";
        StringReader reader = new StringReader(xmlData);
        JSONObject result = invokeToJSONObject(reader, false);
        assertNotNull(result);
        assertTrue(result.has("root"));
        assertEquals("value", result.getJSONObject("root").getString("element"));
    }

    @Test
    public void testToJSONObjectEmptyReader() throws Exception {
        StringReader reader = new StringReader("");
        JSONObject result = invokeToJSONObject(reader, true);
        assertNotNull(result);
        assertTrue(result.isEmpty());
    }

    @Test
    public void testToJSONObjectNullReader() {
        assertThrows(NullPointerException.class, () -> {
            invokeToJSONObject(null, true);
        });
    }

    @Test
    public void testToJSONObjectPrivateMethod() throws Exception {
        String xmlData = "<root><element>value</element></root>";
        StringReader reader = new StringReader(xmlData);
        Method method = XML.class.getDeclaredMethod("toJSONObject", Reader.class, XMLParserConfiguration.class);
        method.setAccessible(true);
        JSONObject result = (JSONObject) method.invoke(null, reader, XMLParserConfiguration.KEEP_STRINGS);
        assertNotNull(result);
        assertTrue(result.has("root"));
        assertEquals("value", result.getJSONObject("root").getString("element"));
    }

    private JSONObject invokeToJSONObject(Reader reader, boolean keepStrings) throws Exception {
        Method method = XML.class.getDeclaredMethod("toJSONObject", Reader.class, boolean.class);
        method.setAccessible(true);
        return (JSONObject) method.invoke(null, reader, keepStrings);
    }
}
