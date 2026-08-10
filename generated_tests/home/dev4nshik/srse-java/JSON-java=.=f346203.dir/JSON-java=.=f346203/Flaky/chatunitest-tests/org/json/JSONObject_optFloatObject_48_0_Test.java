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

public class JSONObject_optFloatObject_48_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() {
        jsonObject = new JSONObject();
    }

    @Test
    public void testOptFloatObject_KeyExists_ReturnsFloatValue() throws Exception {
        setInternalMap("key1", 123.45f);
        Float result = jsonObject.optFloatObject("key1");
        assertEquals(123.45f, result);
    }

    @Test
    public void testOptFloatObject_KeyDoesNotExist_ReturnsNaN() {
        Float result = jsonObject.optFloatObject("nonExistentKey");
        assertTrue(Float.isNaN(result));
    }

    @Test
    public void testOptFloatObject_KeyExistsWithNonNumberValue_ReturnsNaN() throws Exception {
        setInternalMap("key2", "notANumber");
        Float result = jsonObject.optFloatObject("key2");
        assertTrue(Float.isNaN(result));
    }

    @Test
    public void testOptFloatObject_KeyExistsWithNullValue_ReturnsNaN() throws Exception {
        setInternalMap("key3", null);
        Float result = jsonObject.optFloatObject("key3");
        assertTrue(Float.isNaN(result));
    }

    private void setInternalMap(String key, Object value) throws Exception {
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
