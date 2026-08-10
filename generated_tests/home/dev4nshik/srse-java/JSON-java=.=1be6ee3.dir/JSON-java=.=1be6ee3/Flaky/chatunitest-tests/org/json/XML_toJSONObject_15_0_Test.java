package org.json;

import org.json.XML;
import org.json.XMLParserConfiguration;
import org.json.JSONObject;
import org.json.JSONException;
import java.lang.reflect.Method;
import java.io.StringReader;
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

public class XML_toJSONObject_15_0_Test {

    @Test
    public void testToJSONObject() throws Exception {
        // Prepare test data
        String xmlString = "<root><element>value</element></root>";
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        // Invoke the focal method
        JSONObject result = XML.toJSONObject(xmlString, config);
        // Verify the result
        assertNotNull(result);
        assertTrue(result.has("root"));
        JSONObject root = result.getJSONObject("root");
        assertTrue(root.has("element"));
        assertEquals("value", root.getString("element"));
    }

    @Test
    public void testToJSONObjectWithEmptyString() throws Exception {
        // Prepare test data
        String xmlString = "";
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        // Invoke the focal method
        JSONObject result = XML.toJSONObject(xmlString, config);
        // Verify the result
        assertNotNull(result);
        assertTrue(result.isEmpty());
    }

    @Test
    public void testToJSONObjectWithInvalidXML() {
        // Prepare test data
        String xmlString = "<root><element>value</element>";
        XMLParserConfiguration config = XMLParserConfiguration.ORIGINAL;
        // Expect JSONException to be thrown
        assertThrows(JSONException.class, () -> {
            XML.toJSONObject(xmlString, config);
        });
    }
}
