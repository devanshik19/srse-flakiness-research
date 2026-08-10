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

public class Info_cast_8_0_Test {

    @Test
    public void testCastMethod() throws Exception {
        // Create an instance of Info
        Info info = new Info();
        // Use reflection to access the private field 'cast'
        Method setCastMethod = Info.class.getDeclaredMethod("cast", boolean.class);
        setCastMethod.setAccessible(true);
        // Set the cast field to true
        Info returnedInfo = (Info) setCastMethod.invoke(info, true);
        // Verify that the cast field is set to true
        assertTrue(info.cast);
        assertSame(info, returnedInfo);
        // Set the cast field to false
        returnedInfo = (Info) setCastMethod.invoke(info, false);
        // Verify that the cast field is set to false
        assertFalse(info.cast);
        assertSame(info, returnedInfo);
    }
}
