package org.bytedeco.javacpp.tools;

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

public class Info_enumerate_12_0_Test {

    private Info info;

    @BeforeEach
    public void setUp() {
        info = new Info();
    }

    @Test
    public void testEnumerateTrue() throws Exception {
        Info result = info.enumerate(true);
        assertTrue(getPrivateBooleanField(info, "enumerate"));
        assertSame(info, result);
    }

    @Test
    public void testEnumerateFalse() throws Exception {
        Info result = info.enumerate(false);
        assertFalse(getPrivateBooleanField(info, "enumerate"));
        assertSame(info, result);
    }

    private boolean getPrivateBooleanField(Info info, String fieldName) throws Exception {
        java.lang.reflect.Field field = Info.class.getDeclaredField(fieldName);
        field.setAccessible(true);
        return field.getBoolean(info);
    }
}
