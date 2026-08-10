package org.json;

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

public class JSONObject_getInt_12_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() {
        jsonObject = new JSONObject();
    }

    @Test
    public void testGetIntWithNumber() throws Exception {
        setField(jsonObject, "map", new HashMap<>(Map.of("key1", 42)));
        assertEquals(42, jsonObject.getInt("key1"));
    }

    @Test
    public void testGetIntWithStringNumber() throws Exception {
        setField(jsonObject, "map", new HashMap<>(Map.of("key1", "42")));
        assertEquals(42, jsonObject.getInt("key1"));
    }

    @Test
    public void testGetIntWithInvalidString() throws Exception {
        setField(jsonObject, "map", new HashMap<>(Map.of("key1", "invalid")));
        JSONException exception = assertThrows(JSONException.class, () -> jsonObject.getInt("key1"));
        assertTrue(exception.getMessage().contains("is not a int"));
    }

    @Test
    public void testGetIntWithMissingKey() {
        JSONException exception = assertThrows(JSONException.class, () -> jsonObject.getInt("missingKey"));
        assertTrue(exception.getMessage().contains("not found"));
    }

    private void setField(JSONObject jsonObject, String fieldName, Object value) throws Exception {
        Field field = JSONObject.class.getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(jsonObject, value);
    }
}
