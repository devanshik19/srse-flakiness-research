package org.json;

import org.json.JSONObject;
import org.json.JSONException;
import java.math.BigDecimal;
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
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
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

public class JSONObject_getBigDecimal_8_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() {
        jsonObject = new JSONObject();
    }

    @Test
    public void testGetBigDecimal_InvalidFormat() {
        jsonObject = new JSONObject();
        Map<String, Object> map = new HashMap<>();
        map.put("key", "not a number");
        setField(jsonObject, "map", map);
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getBigDecimal("key");
        });
        assertTrue(exception.getMessage().contains("is not a BigDecimal"));
    }

    @Test
    public void testGetBigDecimal_KeyNotFound() {
        jsonObject = new JSONObject();
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getBigDecimal("nonexistentKey");
        });
        assertTrue(exception.getMessage().contains("not found"));
    }

    private void setField(Object target, String fieldName, Object value) {
        try {
            java.lang.reflect.Field field = target.getClass().getDeclaredField(fieldName);
            field.setAccessible(true);
            field.set(target, value);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
