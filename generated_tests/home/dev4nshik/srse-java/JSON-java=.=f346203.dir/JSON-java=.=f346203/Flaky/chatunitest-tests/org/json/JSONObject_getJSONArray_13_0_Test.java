package org.json;

import org.json.JSONArray;
import org.json.JSONException;
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

public class JSONObject_getJSONArray_13_0_Test {

    private JSONObject jsonObject;

    private Map<String, Object> map;

    @BeforeEach
    public void setUp() throws Exception {
        jsonObject = new JSONObject();
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        map = (Map<String, Object>) mapField.get(jsonObject);
    }

    @Test
    public void testGetJSONArray_ValidJSONArray() throws Exception {
        JSONArray jsonArray = new JSONArray();
        map.put("arrayKey", jsonArray);
        JSONArray result = jsonObject.getJSONArray("arrayKey");
        assertSame(jsonArray, result);
    }

    @Test
    public void testGetJSONArray_InvalidType() {
        map.put("notArrayKey", "a string");
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getJSONArray("notArrayKey");
        });
        assertTrue(exception.getMessage().contains("is not a JSONArray"));
    }

    @Test
    public void testGetJSONArray_KeyNotFound() {
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getJSONArray("missingKey");
        });
        assertTrue(exception.getMessage().contains("not found"));
    }
}
