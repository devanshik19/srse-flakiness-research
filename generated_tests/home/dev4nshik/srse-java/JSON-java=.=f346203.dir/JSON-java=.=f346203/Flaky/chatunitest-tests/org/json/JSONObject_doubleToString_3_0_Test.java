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

class JSONObject_doubleToString_3_0_Test {

    @Test
    void testDoubleToString() throws Exception {
        // Access the private method using reflection
        Method doubleToStringMethod = JSONObject.class.getDeclaredMethod("doubleToString", double.class);
        doubleToStringMethod.setAccessible(true);
        // Test cases
        assertEquals("null", doubleToStringMethod.invoke(null, Double.POSITIVE_INFINITY));
        assertEquals("null", doubleToStringMethod.invoke(null, Double.NEGATIVE_INFINITY));
        assertEquals("null", doubleToStringMethod.invoke(null, Double.NaN));
        assertEquals("123.45", doubleToStringMethod.invoke(null, 123.45000));
        assertEquals("123", doubleToStringMethod.invoke(null, 123.00000));
        assertEquals("0", doubleToStringMethod.invoke(null, 0.0));
        assertEquals("-123.45", doubleToStringMethod.invoke(null, -123.45000));
        assertEquals("-123", doubleToStringMethod.invoke(null, -123.00000));
    }
}
