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

public class Info_virtualize_34_0_Test {

    @Test
    public void testVirtualize() throws Exception {
        // Create an instance of Info
        Info info = new Info();
        // Use reflection to access the private field 'virtualize'
        Method virtualizeMethod = Info.class.getDeclaredMethod("virtualize", boolean.class);
        virtualizeMethod.setAccessible(true);
        // Test setting virtualize to true
        Info returnedInfo = (Info) virtualizeMethod.invoke(info, true);
        assertTrue(getVirtualizeField(info));
        assertSame(info, returnedInfo);
        // Test setting virtualize to false
        returnedInfo = (Info) virtualizeMethod.invoke(info, false);
        assertFalse(getVirtualizeField(info));
        assertSame(info, returnedInfo);
    }

    private boolean getVirtualizeField(Info info) throws Exception {
        // Use reflection to access the private field 'virtualize'
        java.lang.reflect.Field virtualizeField = Info.class.getDeclaredField("virtualize");
        virtualizeField.setAccessible(true);
        return virtualizeField.getBoolean(info);
    }
}
