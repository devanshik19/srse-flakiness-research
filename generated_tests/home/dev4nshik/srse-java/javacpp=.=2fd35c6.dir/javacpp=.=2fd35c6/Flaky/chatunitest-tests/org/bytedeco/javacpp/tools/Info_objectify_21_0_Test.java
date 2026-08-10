package org.bytedeco.javacpp.tools;

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

public class Info_objectify_21_0_Test {

    @Test
    public void testObjectify() throws Exception {
        // Create an instance of Info
        Info info = new Info();
        // Use reflection to invoke the private method objectify()
        Method objectifyMethod = Info.class.getDeclaredMethod("objectify");
        objectifyMethod.setAccessible(true);
        // Invoke the method and get the result
        Info result = (Info) objectifyMethod.invoke(info);
        // Check if the result is the same instance
        assertSame(info, result);
        // Verify that the objectify field is set to true
        assertTrue(info.objectify);
    }
}
