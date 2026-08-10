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

public class Info_flatten_14_0_Test {

    @Test
    public void testFlattenWithTrue() throws Exception {
        Info info = new Info();
        // Use reflection to invoke the private method
        Method flattenMethod = Info.class.getDeclaredMethod("flatten", boolean.class);
        flattenMethod.setAccessible(true);
        // Invoke the method with true
        Info returnedInfo = (Info) flattenMethod.invoke(info, true);
        // Assert the flatten field is set to true
        assertTrue(info.flatten);
        // Assert the method returns the same instance
        assertSame(info, returnedInfo);
    }

    @Test
    public void testFlattenWithFalse() throws Exception {
        Info info = new Info();
        // Use reflection to invoke the private method
        Method flattenMethod = Info.class.getDeclaredMethod("flatten", boolean.class);
        flattenMethod.setAccessible(true);
        // Invoke the method with false
        Info returnedInfo = (Info) flattenMethod.invoke(info, false);
        // Assert the flatten field is set to false
        assertFalse(info.flatten);
        // Assert the method returns the same instance
        assertSame(info, returnedInfo);
    }
}
