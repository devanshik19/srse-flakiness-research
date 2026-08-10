package org.json;

import org.json.JSONObject;
import org.json.JSONPointer;
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
java.io.Closeable;
import java.io.IOException;
import java.io.StringWriter;
import java.io.Writer;
import java.lang.annotation.Annotation;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Modifier;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Collection;
import java.util.Collections;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.Locale;
import java.util.Map;
import java.util.Map.Entry;
import java.util.ResourceBundle;
import java.util.Set;
import java.util.regex.Pattern;

public class JSONObject_query_82_0_Test {

    @Test
    public void testQueryWithValidPointer() throws Exception {
        // Create a JSONObject with some test data
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("name", "John Doe");
        jsonObject.put("age", 30);
        jsonObject.put("address", new JSONObject().put("city", "New York"));
        // Use reflection to access the private query method
        Method queryMethod = JSONObject.class.getDeclaredMethod("query", JSONPointer.class);
        queryMethod.setAccessible(true);
        // Test querying a valid JSON pointer
        JSONPointer pointer = new JSONPointer("/name");
        Object result = queryMethod.invoke(jsonObject, pointer);
        assertEquals("John Doe", result);
        pointer = new JSONPointer("/age");
        result = queryMethod.invoke(jsonObject, pointer);
        assertEquals(30, result);
        pointer = new JSONPointer("/address/city");
        result = queryMethod.invoke(jsonObject, pointer);
        assertEquals("New York", result);
    }

    @Test
    public void testQueryWithInvalidPointer() throws Exception {
        // Create a JSONObject with some test data
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("name", "John Doe");
        // Use reflection to access the private query method
        Method queryMethod = JSONObject.class.getDeclaredMethod("query", JSONPointer.class);
        queryMethod.setAccessible(true);
        // Test querying an invalid JSON pointer
        JSONPointer pointer = new JSONPointer("/nonexistent");
        Object result = queryMethod.invoke(jsonObject, pointer);
        assertNull(result);
    }

    @Test
    public void testQueryWithEmptyPointer() throws Exception {
        // Create a JSONObject with some test data
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("name", "John Doe");
        // Use reflection to access the private query method
        Method queryMethod = JSONObject.class.getDeclaredMethod("query", JSONPointer.class);
        queryMethod.setAccessible(true);
        // Test querying with an empty JSON pointer (should return the whole object)
        JSONPointer pointer = new JSONPointer("");
        Object result = queryMethod.invoke(jsonObject, pointer);
        assertEquals(jsonObject, result);
    }
}
