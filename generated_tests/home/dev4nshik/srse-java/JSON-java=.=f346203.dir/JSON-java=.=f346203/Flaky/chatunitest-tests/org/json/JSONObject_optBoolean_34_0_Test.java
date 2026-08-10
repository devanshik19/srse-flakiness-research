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

public class JSONObject_optBoolean_34_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() {
        jsonObject = new JSONObject();
    }

    @Test
    public void testOptBooleanKeyExistsAndIsBoolean() {
        setField(jsonObject, "map", Map.of("key1", true, "key2", false));
        assertTrue(jsonObject.optBoolean("key1", false));
        assertFalse(jsonObject.optBoolean("key2", true));
    }

    @Test
    public void testOptBooleanKeyExistsAndIsNull() {
        setField(jsonObject, "map", Map.of("key1", JSONObject.NULL));
        assertTrue(jsonObject.optBoolean("key1", true));
    }

    @Test
    public void testOptBooleanKeyExistsAndIsStringTrue() {
        setField(jsonObject, "map", Map.of("key1", "true"));
        assertTrue(jsonObject.optBoolean("key1", false));
    }

    @Test
    public void testOptBooleanKeyExistsAndIsStringFalse() {
        setField(jsonObject, "map", Map.of("key1", "false"));
        assertFalse(jsonObject.optBoolean("key1", true));
    }

    @Test
    public void testOptBooleanKeyDoesNotExist() {
        assertTrue(jsonObject.optBoolean("nonexistent", true));
        assertFalse(jsonObject.optBoolean("nonexistent", false));
    }

    @Test
    public void testOptBooleanKeyExistsAndIsInvalidString() {
        setField(jsonObject, "map", Map.of("key1", "invalid"));
        assertTrue(jsonObject.optBoolean("key1", true));
    }

    @Test
    public void testOptBooleanKeyExistsAndIsOtherObject() {
        setField(jsonObject, "map", Map.of("key1", 123));
        assertFalse(jsonObject.optBoolean("key1", false));
    }

    private void setField(Object object, String fieldName, Object value) {
        try {
            Field field = JSONObject.class.getDeclaredField(fieldName);
            field.setAccessible(true);
            field.set(object, value);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException(e);
        }
    }
}
