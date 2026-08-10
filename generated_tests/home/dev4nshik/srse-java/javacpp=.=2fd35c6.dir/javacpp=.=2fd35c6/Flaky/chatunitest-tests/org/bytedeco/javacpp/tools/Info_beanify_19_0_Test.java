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

public class Info_beanify_19_0_Test {

    @Test
    public void testBeanify() throws Exception {
        // Create an instance of the Info class
        Info info = new Info();
        // Use reflection to invoke the private method beanify
        Method beanifyMethod = Info.class.getDeclaredMethod("beanify");
        beanifyMethod.setAccessible(true);
        // Invoke the method and get the result
        Info result = (Info) beanifyMethod.invoke(info);
        // Assert that the result is the same instance
        assertSame(info, result, "The beanify method should return the same instance");
        // Assert that the beanify field is set to true
        assertTrue(info.beanify, "The beanify field should be set to true");
    }
}
