package org.json;

import org.json.JSONObject;
import org.json.JSONTokener;
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

public class JSONObject_optFloat_47_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() {
        jsonObject = new JSONObject();
    }

    @Test
    public void testOptFloatWithExistingKey() throws Exception {
        // Set up the map field using reflection
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        Map<String, Object> map = new HashMap<>();
        map.put("key1", 123.45f);
        mapField.set(jsonObject, map);
        // Test optFloat with a key that exists
        float defaultValue = 0.0f;
        float result = jsonObject.optFloat("key1", defaultValue);
        assertEquals(123.45f, result);
    }

    @Test
    public void testOptFloatWithNonExistingKey() {
        // Test optFloat with a key that does not exist
        float defaultValue = 0.0f;
        float result = jsonObject.optFloat("nonExistingKey", defaultValue);
        assertEquals(defaultValue, result);
    }

    @Test
    public void testOptFloatWithNullValue() throws Exception {
        // Set up the map field using reflection
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        Map<String, Object> map = new HashMap<>();
        map.put("key1", null);
        mapField.set(jsonObject, map);
        // Test optFloat with a key that has a null value
        float defaultValue = 0.0f;
        float result = jsonObject.optFloat("key1", defaultValue);
        assertEquals(defaultValue, result);
    }

    @Test
    public void testOptFloatWithNonNumberValue() throws Exception {
        // Set up the map field using reflection
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        Map<String, Object> map = new HashMap<>();
        map.put("key1", "not a number");
        mapField.set(jsonObject, map);
        // Test optFloat with a key that has a non-number value
        float defaultValue = 0.0f;
        float result = jsonObject.optFloat("key1", defaultValue);
        assertEquals(defaultValue, result);
    }
}
