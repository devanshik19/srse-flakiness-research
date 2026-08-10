package org.json;

import org.json.JSONObject;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
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
import java.util.regex.Pattern;

public class JSONObject_keySet_23_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() throws Exception {
        jsonObject = new JSONObject();
        // Use reflection to set the private map field
        Field mapField = JSONObject.class.getDeclaredField("map");
        mapField.setAccessible(true);
        Map<String, Object> map = new HashMap<>();
        map.put("key1", "value1");
        map.put("key2", "value2");
        mapField.set(jsonObject, map);
    }

    @Test
    public void testKeySet() {
        Set<String> keys = jsonObject.keySet();
        assertEquals(2, keys.size());
        assertEquals(Set.of("key1", "key2"), keys);
    }
}
