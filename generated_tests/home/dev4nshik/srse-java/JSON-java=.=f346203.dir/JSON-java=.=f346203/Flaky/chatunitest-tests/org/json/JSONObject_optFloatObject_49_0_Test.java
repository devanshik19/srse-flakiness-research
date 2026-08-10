package org.json;

import org.json.JSONObject;
import java.lang.reflect.Field;
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
java.io.Closeable;
import java.io.IOException;
import java.io.StringWriter;
import java.io.Writer;
import java.lang.annotation.Annotation;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Collection;
import java.util.Collections;
import java.util.Enumeration;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.Locale;
import java.util.Map.Entry;
import java.util.ResourceBundle;
import java.util.Set;
import java.util.regex.Pattern;

public class JSONObject_optFloatObject_49_0_Test {

    @Test
    public void testOptFloatObjectWithExistingKey() throws NoSuchFieldException, IllegalAccessException {
        // Set up a JSONObject with a key-value pair
        JSONObject jsonObject = new JSONObject();
        setPrivateMap(jsonObject, "testKey", 10.5);
        // Call the method and assert the expected value
        Float result = jsonObject.optFloatObject("testKey", 0.0f);
        assertEquals(10.5f, result);
    }

    @Test
    public void testOptFloatObjectWithNonExistingKey() throws NoSuchFieldException, IllegalAccessException {
        // Set up a JSONObject without the key
        JSONObject jsonObject = new JSONObject();
        // Call the method and assert the default value
        Float result = jsonObject.optFloatObject("nonExistentKey", 5.0f);
        assertEquals(5.0f, result);
    }

    @Test
    public void testOptFloatObjectWithNullValue() throws NoSuchFieldException, IllegalAccessException {
        // Set up a JSONObject with a key mapped to null
        JSONObject jsonObject = new JSONObject();
        setPrivateMap(jsonObject, "testKey", null);
        // Call the method and assert the default value
        Float result = jsonObject.optFloatObject("testKey", 3.0f);
        assertEquals(3.0f, result);
    }

    private void setPrivateMap(JSONObject jsonObject, String key, Object value) throws NoSuchFieldException, IllegalAccessException {
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        Map<String, Object> map = (Map<String, Object>) mapField.get(jsonObject);
        if (map == null) {
            map = new HashMap<>();
            mapField.set(jsonObject, map);
        }
        map.put(key, value);
    }
}
