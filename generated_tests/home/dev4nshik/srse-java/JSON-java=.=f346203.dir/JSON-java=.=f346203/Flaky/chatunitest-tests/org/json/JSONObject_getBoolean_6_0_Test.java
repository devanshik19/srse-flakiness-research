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

public class JSONObject_getBoolean_6_0_Test {

    @Test
    public void testGetBooleanTrue() throws Exception {
        JSONObject jsonObject = new JSONObject();
        setPrivateField(jsonObject, "map", Map.of("key1", true, "key2", "true"));
        assertTrue(jsonObject.getBoolean("key1"));
        assertTrue(jsonObject.getBoolean("key2"));
    }

    @Test
    public void testGetBooleanFalse() throws Exception {
        JSONObject jsonObject = new JSONObject();
        setPrivateField(jsonObject, "map", Map.of("key1", false, "key2", "false"));
        assertFalse(jsonObject.getBoolean("key1"));
        assertFalse(jsonObject.getBoolean("key2"));
    }

    @Test
    public void testGetBooleanThrowsException() {
        JSONObject jsonObject = new JSONObject();
        setPrivateField(jsonObject, "map", Map.of("key1", "notABoolean"));
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getBoolean("key1");
        });
        assertTrue(exception.getMessage().contains("JSONObject[\"key1\"] is not a Boolean"));
    }

    @Test
    public void testGetBooleanKeyNotFound() {
        JSONObject jsonObject = new JSONObject();
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getBoolean("nonExistentKey");
        });
        assertTrue(exception.getMessage().contains("JSONObject[\"nonExistentKey\"] not found."));
    }

    private void setPrivateField(JSONObject jsonObject, String fieldName, Object value) {
        try {
            Field field = JSONObject.class.getDeclaredField(fieldName);
            field.setAccessible(true);
            field.set(jsonObject, value);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
