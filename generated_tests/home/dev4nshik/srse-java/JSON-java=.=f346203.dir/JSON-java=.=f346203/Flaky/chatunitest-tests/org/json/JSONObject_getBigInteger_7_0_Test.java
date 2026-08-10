package org.json;

import org.json.JSONException;
import org.json.JSONObject;
import java.math.BigDecimal;
import java.math.BigInteger;
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

public class JSONObject_getBigInteger_7_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() {
        Map<String, Object> map = new HashMap<>();
        map.put("bigInteger", new BigInteger("12345678901234567890"));
        map.put("bigDecimal", new BigDecimal("1234567890.123456789"));
        map.put("double", 1234567890.123456789);
        map.put("integer", 123456789);
        map.put("stringInt", "123456789");
        map.put("stringBigInt", "12345678901234567890");
        map.put("nonNumericString", "notANumber");
        map.put("nullValue", JSONObject.NULL);
        jsonObject = new JSONObject(map);
    }

    @Test
    public void testGetBigIntegerWithBigInteger() throws Exception {
        BigInteger result = jsonObject.getBigInteger("bigInteger");
        assertEquals(new BigInteger("12345678901234567890"), result);
    }

    @Test
    public void testGetBigIntegerWithBigDecimal() throws Exception {
        BigInteger result = jsonObject.getBigInteger("bigDecimal");
        assertEquals(new BigInteger("1234567890"), result);
    }

    @Test
    public void testGetBigIntegerWithDouble() throws Exception {
        BigInteger result = jsonObject.getBigInteger("double");
        assertEquals(new BigInteger("1234567890"), result);
    }

    @Test
    public void testGetBigIntegerWithInteger() throws Exception {
        BigInteger result = jsonObject.getBigInteger("integer");
        assertEquals(new BigInteger("123456789"), result);
    }

    @Test
    public void testGetBigIntegerWithStringInt() throws Exception {
        BigInteger result = jsonObject.getBigInteger("stringInt");
        assertEquals(new BigInteger("123456789"), result);
    }

    @Test
    public void testGetBigIntegerWithStringBigInt() throws Exception {
        BigInteger result = jsonObject.getBigInteger("stringBigInt");
        assertEquals(new BigInteger("12345678901234567890"), result);
    }

    @Test
    public void testGetBigIntegerWithNonNumericString() {
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getBigInteger("nonNumericString");
        });
        assertTrue(exception.getMessage().contains("is not a BigInteger"));
    }

    @Test
    public void testGetBigIntegerWithNullValue() {
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getBigInteger("nullValue");
        });
        assertTrue(exception.getMessage().contains("is not a BigInteger"));
    }

    @Test
    public void testGetBigIntegerWithNonExistentKey() {
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getBigInteger("nonExistentKey");
        });
        assertTrue(exception.getMessage().contains("not found"));
    }
}
