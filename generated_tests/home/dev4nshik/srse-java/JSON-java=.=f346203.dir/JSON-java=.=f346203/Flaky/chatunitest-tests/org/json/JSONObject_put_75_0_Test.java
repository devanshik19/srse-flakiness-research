package org.json;

import org.json.JSONObject;
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

public class JSONObject_put_75_0_Test {

    @Test
    public void testPutWithFloat() throws Exception {
        // Create an instance of JSONObject
        JSONObject jsonObject = new JSONObject();
        // Define test data
        String key = "testKey";
        float value = 3.14f;
        // Use reflection to access the private 'put' method with Object parameter
        Method putMethod = JSONObject.class.getDeclaredMethod("put", String.class, Object.class);
        putMethod.setAccessible(true);
        // Invoke the method with test data
        JSONObject result = (JSONObject) putMethod.invoke(jsonObject, key, Float.valueOf(value));
        // Verify that the returned JSONObject is the same instance
        assertSame(jsonObject, result);
        // Verify that the value has been correctly added to the JSONObject
        assertEquals(value, jsonObject.get(key));
    }

    @Test
    public void testPutWithNullKey() {
        // Create an instance of JSONObject
        JSONObject jsonObject = new JSONObject();
        // Define test data
        String key = null;
        float value = 3.14f;
        // Verify that a NullPointerException is thrown when the key is null
        assertThrows(NullPointerException.class, () -> {
            jsonObject.put(key, value);
        });
    }
}
