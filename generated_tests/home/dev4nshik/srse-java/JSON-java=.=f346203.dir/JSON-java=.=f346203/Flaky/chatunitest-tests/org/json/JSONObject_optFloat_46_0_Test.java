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

public class JSONObject_optFloat_46_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() throws Exception {
        jsonObject = new JSONObject();
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        Map<String, Object> map = new HashMap<>();
        map.put("validFloat", 10.5f);
        map.put("invalidFloat", "notANumber");
        map.put("nullValue", null);
        mapField.set(jsonObject, map);
    }

    @Test
    public void testOptFloatWithValidKey() {
        float result = jsonObject.optFloat("validFloat");
        assertEquals(10.5f, result, 0.0f);
    }

    @Test
    public void testOptFloatWithInvalidKey() {
        float result = jsonObject.optFloat("invalidFloat");
        assertEquals(Float.NaN, result, 0.0f);
    }

    @Test
    public void testOptFloatWithNonExistentKey() {
        float result = jsonObject.optFloat("nonExistentKey");
        assertEquals(Float.NaN, result, 0.0f);
    }

    @Test
    public void testOptFloatWithNullValue() {
        float result = jsonObject.optFloat("nullValue");
        assertEquals(Float.NaN, result, 0.0f);
    }
}
