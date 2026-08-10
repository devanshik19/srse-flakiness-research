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

public class Info_virtualize_33_0_Test {

    @Test
    public void testVirtualize() throws Exception {
        // Create an instance of the Info class
        Info info = new Info();
        // Use reflection to access the private field 'virtualize'
        Method virtualizeMethod = Info.class.getDeclaredMethod("virtualize");
        virtualizeMethod.setAccessible(true);
        // Call the virtualize method
        Info returnedInfo = (Info) virtualizeMethod.invoke(info);
        // Validate that the virtualize field is set to true
        assertTrue(info.virtualize, "The virtualize field should be true after calling virtualize()");
        // Validate that the method returns the same instance
        assertSame(info, returnedInfo, "The virtualize() method should return the same instance");
    }
}
