package org.json;

import org.json.JSONObject;
import org.json.JSONException;
import java.lang.reflect.Field;
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
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.Locale;
import java.util.Map.Entry;
import java.util.ResourceBundle;
import java.util.Set;
import java.util.regex.Pattern;

public class JSONObject_put_74_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() {
        jsonObject = new JSONObject();
    }

    @Test
    public void testPutValidKeyAndValue() throws JSONException, NoSuchFieldException, IllegalAccessException {
        String key = "validKey";
        double value = 123.456;
        jsonObject.put(key, value);
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        Map<String, Object> map = (Map<String, Object>) mapField.get(jsonObject);
        assertTrue(map.containsKey(key));
        assertEquals(Double.valueOf(value), map.get(key));
    }

    @Test
    public void testPutNullKey() {
        double value = 123.456;
        assertThrows(NullPointerException.class, () -> {
            jsonObject.put(null, value);
        });
    }

    @Test
    public void testPutNegativeValue() throws JSONException, NoSuchFieldException, IllegalAccessException {
        String key = "negativeValue";
        double value = -987.654;
        jsonObject.put(key, value);
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        Map<String, Object> map = (Map<String, Object>) mapField.get(jsonObject);
        assertTrue(map.containsKey(key));
        assertEquals(Double.valueOf(value), map.get(key));
    }

    @Test
    public void testPutZeroValue() throws JSONException, NoSuchFieldException, IllegalAccessException {
        String key = "zeroValue";
        double value = 0.0;
        jsonObject.put(key, value);
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        Map<String, Object> map = (Map<String, Object>) mapField.get(jsonObject);
        assertTrue(map.containsKey(key));
        assertEquals(Double.valueOf(value), map.get(key));
    }
}
