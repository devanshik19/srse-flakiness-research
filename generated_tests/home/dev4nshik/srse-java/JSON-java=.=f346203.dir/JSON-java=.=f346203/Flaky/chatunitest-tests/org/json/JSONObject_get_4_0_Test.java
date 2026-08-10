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

public class JSONObject_get_4_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() {
        jsonObject = new JSONObject();
    }

    @Test
    public void testGetExistingKey() throws JSONException {
        // Set up the map using reflection to bypass private access
        setPrivateField(jsonObject, "map", new HashMap<>(Map.of("key1", "value1")));
        // Test the get method
        assertEquals("value1", jsonObject.get("key1"));
    }

    @Test
    public void testGetNonExistingKey() {
        // Test that a JSONException is thrown for a non-existing key
        JSONException exception = assertThrows(JSONException.class, () -> jsonObject.get("nonExistingKey"));
        assertEquals("JSONObject[\"nonExistingKey\"] not found.", exception.getMessage());
    }

    @Test
    public void testGetNullKey() {
        // Test that a JSONException is thrown for a null key
        JSONException exception = assertThrows(JSONException.class, () -> jsonObject.get(null));
        assertEquals("Null key.", exception.getMessage());
    }

    private void setPrivateField(Object object, String fieldName, Object value) {
        try {
            Field field = object.getClass().getDeclaredField(fieldName);
            field.setAccessible(true);
            field.set(object, value);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new RuntimeException(e);
        }
    }
}
