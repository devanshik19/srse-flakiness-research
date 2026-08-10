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

public class Info_skip_26_0_Test {

    @Test
    public void testSkipTrue() throws Exception {
        Info info = new Info();
        Method skipMethod = Info.class.getDeclaredMethod("skip", boolean.class);
        skipMethod.setAccessible(true);
        Info result = (Info) skipMethod.invoke(info, true);
        assertNotNull(result);
        assertTrue(getSkipField(info));
    }

    @Test
    public void testSkipFalse() throws Exception {
        Info info = new Info();
        Method skipMethod = Info.class.getDeclaredMethod("skip", boolean.class);
        skipMethod.setAccessible(true);
        Info result = (Info) skipMethod.invoke(info, false);
        assertNotNull(result);
        assertFalse(getSkipField(info));
    }

    private boolean getSkipField(Info info) throws Exception {
        java.lang.reflect.Field skipField = Info.class.getDeclaredField("skip");
        skipField.setAccessible(true);
        return (boolean) skipField.get(info);
    }
}
