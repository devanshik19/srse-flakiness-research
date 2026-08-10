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

public class JSONObject_optString_64_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() throws Exception {
        jsonObject = new JSONObject();
        // Use reflection to set the private map field
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        Map<String, Object> map = new HashMap<>();
        map.put("key1", "value1");
        map.put("key2", JSONObject.NULL);
        mapField.set(jsonObject, map);
    }

    @Test
    public void testOptStringWithExistingKey() {
        assertEquals("value1", jsonObject.optString("key1"));
    }

    @Test
    public void testOptStringWithNonExistingKey() {
        assertEquals("", jsonObject.optString("nonExistingKey"));
    }

    @Test
    public void testOptStringWithNullValue() {
        assertEquals("", jsonObject.optString("key2"));
    }
}
