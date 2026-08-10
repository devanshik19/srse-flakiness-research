package org.json;

import org.json.XML;
import org.json.XMLParserConfiguration;
import org.json.JSONException;
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

public class XML_toString_18_0_Test {

    @Test
    public void testToStringWithJSONObject() throws Exception {
        // Create a JSONObject with sample data
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("name", "John");
        jsonObject.put("age", 30);
        // Use reflection to access the private method
        Method toStringMethod = XML.class.getDeclaredMethod("toString", Object.class, String.class, XMLParserConfiguration.class, int.class, int.class);
        toStringMethod.setAccessible(true);
        // Call the method with the created JSONObject
        String result = (String) toStringMethod.invoke(null, jsonObject, "person", XMLParserConfiguration.ORIGINAL, 0, 0);
        // Expected XML output
        String expected = "<person><name>John</name><age>30</age></person>";
        // Assert the result
        assertEquals(expected, result);
    }

    @Test
    public void testToStringWithJSONArray() throws Exception {
        // Create a JSONArray with sample data
        JSONArray jsonArray = new JSONArray();
        jsonArray.put("apple");
        jsonArray.put("banana");
        // Use reflection to access the private method
        Method toStringMethod = XML.class.getDeclaredMethod("toString", Object.class, String.class, XMLParserConfiguration.class, int.class, int.class);
        toStringMethod.setAccessible(true);
        // Call the method with the created JSONArray
        String result = (String) toStringMethod.invoke(null, jsonArray, "fruits", XMLParserConfiguration.ORIGINAL, 0, 0);
        // Expected XML output
        String expected = "<fruits>apple</fruits><fruits>banana</fruits>";
        // Assert the result
        assertEquals(expected, result);
    }

    @Test
    public void testToStringWithNullObject() throws Exception {
        // Use reflection to access the private method
        Method toStringMethod = XML.class.getDeclaredMethod("toString", Object.class, String.class, XMLParserConfiguration.class, int.class, int.class);
        toStringMethod.setAccessible(true);
        // Call the method with null object
        String result = (String) toStringMethod.invoke(null, null, "nullTag", XMLParserConfiguration.ORIGINAL, 0, 0);
        // Expected XML output
        String expected = "<nullTag>null</nullTag>";
        // Assert the result
        assertEquals(expected, result);
    }

    @Test
    public void testToStringWithPrimitiveObject() throws Exception {
        // Use reflection to access the private method
        Method toStringMethod = XML.class.getDeclaredMethod("toString", Object.class, String.class, XMLParserConfiguration.class, int.class, int.class);
        toStringMethod.setAccessible(true);
        // Call the method with a primitive object
        String result = (String) toStringMethod.invoke(null, 42, "number", XMLParserConfiguration.ORIGINAL, 0, 0);
        // Expected XML output
        String expected = "<number>42</number>";
        // Assert the result
        assertEquals(expected, result);
    }

    @Test
    public void testToStringThrowsJSONException() {
        assertThrows(JSONException.class, () -> {
            // Use reflection to access the private method
            Method toStringMethod = XML.class.getDeclaredMethod("toString", Object.class, String.class, XMLParserConfiguration.class, int.class, int.class);
            toStringMethod.setAccessible(true);
            // Call the method with an invalid object
            toStringMethod.invoke(null, new Object(), "invalid", XMLParserConfiguration.ORIGINAL, 0, 0);
        });
    }
}
