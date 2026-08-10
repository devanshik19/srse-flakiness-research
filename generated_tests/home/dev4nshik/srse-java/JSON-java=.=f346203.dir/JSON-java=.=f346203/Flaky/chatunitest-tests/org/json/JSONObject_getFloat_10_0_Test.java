package org.json;

import org.json.JSONObject;
import org.json.JSONException;
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

public class JSONObject_getFloat_10_0_Test {

    private JSONObject jsonObject;

    private Map<String, Object> map;

    @BeforeEach
    public void setUp() throws Exception {
        jsonObject = new JSONObject();
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        map = new HashMap<>();
        mapField.set(jsonObject, map);
    }

    @Test
    public void testGetFloatWithNumber() throws JSONException {
        map.put("key1", 123.45);
        assertEquals(123.45f, jsonObject.getFloat("key1"));
    }

    @Test
    public void testGetFloatWithStringNumber() throws JSONException {
        map.put("key2", "678.90");
        assertEquals(678.90f, jsonObject.getFloat("key2"));
    }

    @Test
    public void testGetFloatWithInvalidString() {
        map.put("key3", "invalid");
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getFloat("key3");
        });
        assertTrue(exception.getMessage().contains("is not a float"));
    }

    @Test
    public void testGetFloatWithNullKey() {
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getFloat(null);
        });
        assertEquals("Null key.", exception.getMessage());
    }

    @Test
    public void testGetFloatWithNonExistentKey() {
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getFloat("nonExistentKey");
        });
        assertTrue(exception.getMessage().contains("not found."));
    }
}
