package org.json;

import org.json.JSONObject;
import java.util.Iterator;
import java.util.Map;
import java.util.HashMap;
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
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Collection;
import java.util.Collections;
import java.util.Enumeration;
import java.util.IdentityHashMap;
import java.util.Locale;
import java.util.Map.Entry;
import java.util.ResourceBundle;
import java.util.Set;
import java.util.regex.Pattern;

public class JSONObject_keys_22_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() {
        Map<String, Object> map = new HashMap<>();
        map.put("key1", "value1");
        map.put("key2", "value2");
        jsonObject = new JSONObject(map);
    }

    @Test
    public void testKeys() {
        Iterator<String> keysIterator = jsonObject.keys();
        assertNotNull(keysIterator);
        assertTrue(keysIterator.hasNext());
        String key1 = keysIterator.next();
        assertNotNull(key1);
        assertTrue(key1.equals("key1") || key1.equals("key2"));
        assertTrue(keysIterator.hasNext());
        String key2 = keysIterator.next();
        assertNotNull(key2);
        assertTrue(key2.equals("key1") || key2.equals("key2"));
        assertNotEquals(key1, key2);
        assertFalse(keysIterator.hasNext());
    }
}
