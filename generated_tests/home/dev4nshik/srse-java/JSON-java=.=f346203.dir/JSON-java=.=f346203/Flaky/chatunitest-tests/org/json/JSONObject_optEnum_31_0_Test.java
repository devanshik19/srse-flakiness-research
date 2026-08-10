package org.json;

import org.json.JSONObject;
import java.lang.reflect.Method;
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
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.Locale;
import java.util.Map;
import java.util.Map.Entry;
import java.util.ResourceBundle;
import java.util.Set;
import java.util.regex.Pattern;

public class JSONObject_optEnum_31_0_Test {

    @Test
    public void testOptEnum() throws Exception {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("key1", "VALUE1");
        jsonObject.put("key2", "INVALID");
        // Using reflection to access the private method optEnum
        Method optEnumMethod = JSONObject.class.getDeclaredMethod("optEnum", Class.class, String.class, Enum.class);
        optEnumMethod.setAccessible(true);
        // Test case 1: Valid enum value
        TestEnum result1 = (TestEnum) optEnumMethod.invoke(jsonObject, TestEnum.class, "key1", TestEnum.DEFAULT);
        assertEquals(TestEnum.VALUE1, result1);
        // Test case 2: Invalid enum value, should return default
        TestEnum result2 = (TestEnum) optEnumMethod.invoke(jsonObject, TestEnum.class, "key2", TestEnum.DEFAULT);
        assertEquals(TestEnum.DEFAULT, result2);
        // Test case 3: Non-existent key, should return default
        TestEnum result3 = (TestEnum) optEnumMethod.invoke(jsonObject, TestEnum.class, "nonExistentKey", TestEnum.DEFAULT);
        assertEquals(TestEnum.DEFAULT, result3);
        // Test case 4: Null default value
        TestEnum result4 = (TestEnum) optEnumMethod.invoke(jsonObject, TestEnum.class, "nonExistentKey", null);
        assertNull(result4);
    }

    private enum TestEnum {

        VALUE1, DEFAULT
    }
}
