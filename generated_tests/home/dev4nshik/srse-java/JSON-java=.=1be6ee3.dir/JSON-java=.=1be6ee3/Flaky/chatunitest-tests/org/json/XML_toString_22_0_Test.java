package org.json;

import org.json.XML;
import org.json.XMLParserConfiguration;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONArray;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Map;
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

public class XML_toString_22_0_Test {

    @Test
    public void testToStringWithJSONObject() throws Exception {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("name", "John Doe");
        jsonObject.put("age", 30);
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        String result = XML.toString(jsonObject, "person", config, 2);
        String expected = "<person>\n" + "  <name>John Doe</name>\n" + "  <age>30</age>\n" + "</person>\n";
        assertEquals(expected, result);
    }

    @Test
    public void testToStringWithJSONArray() throws Exception {
        JSONArray jsonArray = new JSONArray();
        jsonArray.put("item1");
        jsonArray.put("item2");
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        String result = XML.toString(jsonArray, "items", config, 2);
        String expected = "<items>item1</items>\n" + "<items>item2</items>\n";
        assertEquals(expected, result);
    }

    @Test
    public void testToStringWithPrimitive() throws Exception {
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        String result = XML.toString(123, "number", config, 2);
        String expected = "<number>123</number>\n";
        assertEquals(expected, result);
    }

    @Test
    public void testToStringWithNullTag() throws Exception {
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        String result = XML.toString("Hello", null, config, 2);
        String expected = "\"Hello\"\n";
        assertEquals(expected, result);
    }

    @Test
    public void testToStringWithEmptyString() throws Exception {
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        String result = XML.toString("", "empty", config, 2);
        String expected = "<empty/>\n";
        assertEquals(expected, result);
    }

    @Test
    public void testToStringWithNullObject() throws Exception {
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        String result = XML.toString(null, "nullTag", config, 2);
        String expected = "<nullTag>null</nullTag>\n";
        assertEquals(expected, result);
    }

    @Test
    public void testPrivateToStringMethod() throws Exception {
        Method privateToString = XML.class.getDeclaredMethod("toString", Object.class, String.class, XMLParserConfiguration.class, int.class, int.class);
        privateToString.setAccessible(true);
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("key", "value");
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        String result = (String) privateToString.invoke(null, jsonObject, "root", config, 2, 0);
        String expected = "<root>\n" + "  <key>value</key>\n" + "</root>\n";
        assertEquals(expected, result);
    }
}
