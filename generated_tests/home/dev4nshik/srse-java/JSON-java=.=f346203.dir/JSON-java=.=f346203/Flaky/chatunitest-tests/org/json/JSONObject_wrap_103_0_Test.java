package org.json;

import org.json.JSONObject;
import org.json.JSONArray;
import java.lang.reflect.Method;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.Closeable;
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
import java.util.Arrays;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import /*
Public Domain.
*/
java.io.Closeable;

class JSONObject_wrap_103_0_Test {

    @Test
    void testWrapWithNull() throws Exception {
        // Using reflection to access the private wrap(Object, Set<Object>) method
        Method wrapMethod = JSONObject.class.getDeclaredMethod("wrap", Object.class, Set.class);
        wrapMethod.setAccessible(true);
        // Test with null input
        Object result = wrapMethod.invoke(null, null, null);
        assertEquals(JSONObject.NULL, result);
    }

    @Test
    void testWrapWithPrimitive() throws Exception {
        Method wrapMethod = JSONObject.class.getDeclaredMethod("wrap", Object.class, Set.class);
        wrapMethod.setAccessible(true);
        // Test with Integer
        Object result = wrapMethod.invoke(null, 123, null);
        assertEquals(123, result);
        // Test with Double
        result = wrapMethod.invoke(null, 123.45, null);
        assertEquals(123.45, result);
    }

    @Test
    void testWrapWithString() throws Exception {
        Method wrapMethod = JSONObject.class.getDeclaredMethod("wrap", Object.class, Set.class);
        wrapMethod.setAccessible(true);
        // Test with String
        Object result = wrapMethod.invoke(null, "test", null);
        assertEquals("test", result);
    }

    @Test
    void testWrapWithJSONObject() throws Exception {
        Method wrapMethod = JSONObject.class.getDeclaredMethod("wrap", Object.class, Set.class);
        wrapMethod.setAccessible(true);
        // Test with JSONObject
        JSONObject jsonObject = new JSONObject();
        Object result = wrapMethod.invoke(null, jsonObject, null);
        assertEquals(jsonObject, result);
    }

    @Test
    void testWrapWithMap() throws Exception {
        Method wrapMethod = JSONObject.class.getDeclaredMethod("wrap", Object.class, Set.class);
        wrapMethod.setAccessible(true);
        // Test with Map
        Map<String, Object> map = new HashMap<>();
        map.put("key", "value");
        Object result = wrapMethod.invoke(null, map, null);
        assertTrue(result instanceof JSONObject);
        assertEquals("value", ((JSONObject) result).get("key"));
    }

    @Test
    void testWrapWithCollection() throws Exception {
        Method wrapMethod = JSONObject.class.getDeclaredMethod("wrap", Object.class, Set.class);
        wrapMethod.setAccessible(true);
        // Test with Collection
        Collection<Object> collection = Arrays.asList("value1", "value2");
        Object result = wrapMethod.invoke(null, collection, null);
        assertTrue(result instanceof JSONArray);
        assertEquals("value1", ((JSONArray) result).get(0));
        assertEquals("value2", ((JSONArray) result).get(1));
    }
}
