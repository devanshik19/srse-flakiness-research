package org.json;

import org.json.JSONObject;
import org.json.JSONException;
import java.lang.reflect.Method;
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

public class JSONObject_getEnum_5_0_Test {

    private JSONObject jsonObject;

    @BeforeEach
    public void setUp() {
        Map<String, Object> map = new HashMap<>();
        map.put("enumKey", TestEnum.VALUE1);
        jsonObject = new JSONObject(map);
    }

    @Test
    public void testGetEnumSuccess() throws Exception {
        TestEnum result = jsonObject.getEnum(TestEnum.class, "enumKey");
        assertEquals(TestEnum.VALUE1, result);
    }

    @Test
    public void testGetEnumKeyNotFound() {
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getEnum(TestEnum.class, "nonExistentKey");
        });
        assertTrue(exception.getMessage().contains("is not a enum of type"));
    }

    @Test
    public void testGetEnumWrongType() {
        jsonObject = new JSONObject();
        jsonObject.put("enumKey", "notAnEnum");
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getEnum(TestEnum.class, "enumKey");
        });
        assertTrue(exception.getMessage().contains("is not a enum of type"));
    }

    @Test
    public void testGetEnumNullValue() {
        jsonObject = new JSONObject();
        jsonObject.put("enumKey", JSONObject.NULL);
        JSONException exception = assertThrows(JSONException.class, () -> {
            jsonObject.getEnum(TestEnum.class, "enumKey");
        });
        assertTrue(exception.getMessage().contains("is not a enum of type"));
    }

    // Enum for testing purposes
    private enum TestEnum {

        VALUE1, VALUE2
    }
}
