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

public class JSONObject_remove_88_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() {
        jsonObject = new JSONObject();
    }

    @Test
    public void testRemoveExistingKey() throws NoSuchFieldException, IllegalAccessException {
        // Arrange
        String key = "testKey";
        String value = "testValue";
        setMapField(jsonObject, key, value);
        // Act
        Object removedValue = jsonObject.remove(key);
        // Assert
        assertEquals(value, removedValue);
        assertNull(getMapField(jsonObject).get(key));
    }

    @Test
    public void testRemoveNonExistingKey() {
        // Arrange
        String key = "nonExistingKey";
        // Act
        Object removedValue = jsonObject.remove(key);
        // Assert
        assertNull(removedValue);
    }

    @Test
    public void testRemoveNullKey() {
        // Arrange
        String key = null;
        // Act
        Object removedValue = jsonObject.remove(key);
        // Assert
        assertNull(removedValue);
    }

    private void setMapField(JSONObject jsonObject, String key, Object value) throws NoSuchFieldException, IllegalAccessException {
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        @SuppressWarnings("unchecked")
        Map<String, Object> map = (Map<String, Object>) mapField.get(jsonObject);
        map.put(key, value);
    }

    private Map<String, Object> getMapField(JSONObject jsonObject) throws NoSuchFieldException, IllegalAccessException {
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        @SuppressWarnings("unchecked")
        Map<String, Object> map = (Map<String, Object>) mapField.get(jsonObject);
        return map;
    }
}
