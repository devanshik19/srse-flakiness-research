package org.json;

import org.json.JSONObject;
import org.json.JSONException;
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
java.io.Closeable;
import java.io.IOException;
import java.io.StringWriter;
import java.io.Writer;
import java.lang.annotation.Annotation;
import java.lang.reflect.Field;
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

public class JSONObject_getJSONObject_14_0_Test {

    @Test
    public void testGetJSONObjectSuccess() throws Exception {
        // Create a JSONObject with nested JSONObject
        JSONObject innerObject = new JSONObject();
        innerObject.put("innerKey", "innerValue");
        JSONObject outerObject = new JSONObject();
        outerObject.put("outerKey", innerObject);
        // Test getJSONObject for existing key
        JSONObject result = outerObject.getJSONObject("outerKey");
        assertNotNull(result);
        assertEquals("innerValue", result.get("innerKey"));
    }

    @Test
    public void testGetJSONObjectThrowsException() {
        // Create a JSONObject with a non-JSONObject value
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("key", "value");
        // Test getJSONObject for a key with non-JSONObject value
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getJSONObject("key");
        });
        assertTrue(exception.getMessage().contains("is not a JSONObject"));
    }

    @Test
    public void testGetJSONObjectKeyNotFound() {
        // Create an empty JSONObject
        JSONObject jsonObject = new JSONObject();
        // Test getJSONObject for a non-existing key
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getJSONObject("nonExistentKey");
        });
        assertTrue(exception.getMessage().contains("not found"));
    }

    @Test
    public void testWrongValueFormatException() throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        // Use reflection to test private method wrongValueFormatException
        Method method = JSONObject.class.getDeclaredMethod("wrongValueFormatException", String.class, String.class, Object.class, Throwable.class);
        method.setAccessible(true);
        JSONException exception = (JSONException) method.invoke(null, "key", "JSONObject", "value", null);
        assertTrue(exception.getMessage().contains("is not a JSONObject"));
    }
}
