package org.bytedeco.javacpp.tools;

import org.bytedeco.javacpp.tools.Info;
import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.bytedeco.javacpp.Pointer;
import org.bytedeco.javacpp.annotation.ByVal;
import org.bytedeco.javacpp.annotation.Cast;
import org.bytedeco.javacpp.annotation.Virtual;

public class Info_purify_30_0_Test {

    @Test
    public void testPurify() throws Exception {
        // Create an instance of the Info class
        Info info = new Info();
        // Use reflection to access the private field 'purify'
        Method purifyMethod = Info.class.getDeclaredMethod("purify", boolean.class);
        purifyMethod.setAccessible(true);
        // Test setting purify to true
        Info result = (Info) purifyMethod.invoke(info, true);
        assertTrue(getPrivatePurifyField(info));
        assertSame(info, result);
        // Test setting purify to false
        result = (Info) purifyMethod.invoke(info, false);
        assertFalse(getPrivatePurifyField(info));
        assertSame(info, result);
    }

    private boolean getPrivatePurifyField(Info info) throws Exception {
        // Use reflection to access the private field 'purify'
        java.lang.reflect.Field purifyField = Info.class.getDeclaredField("purify");
        purifyField.setAccessible(true);
        return purifyField.getBoolean(info);
    }
}
