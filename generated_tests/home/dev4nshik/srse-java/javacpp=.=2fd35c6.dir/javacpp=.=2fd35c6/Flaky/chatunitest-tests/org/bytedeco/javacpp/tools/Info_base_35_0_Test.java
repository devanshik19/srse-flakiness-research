package org.bytedeco.javacpp.tools;

import org.bytedeco.javacpp.tools.Info;
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

class Info_base_35_0_Test {

    @Test
    void testBaseMethod() throws Exception {
        // Create an instance of the Info class
        Info info = new Info();
        // Invoke the base method with a sample string
        String testBaseValue = "baseValue";
        Info returnedInfo = info.base(testBaseValue);
        // Use reflection to access the private 'base' field
        java.lang.reflect.Field baseField = Info.class.getDeclaredField("base");
        baseField.setAccessible(true);
        // Assert that the 'base' field is set correctly
        assertEquals(testBaseValue, baseField.get(info));
        // Assert that the returned object is the same instance (method chaining)
        assertSame(info, returnedInfo);
    }
}
