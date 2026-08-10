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

public class Info_beanify_20_0_Test {

    private Info info;

    @BeforeEach
    public void setUp() {
        info = new Info();
    }

    @Test
    public void testBeanifyTrue() {
        Info returnedInfo = info.beanify(true);
        assertNotNull(returnedInfo);
        assertSame(info, returnedInfo);
        assertTrue(getBeanifyFieldValue());
    }

    @Test
    public void testBeanifyFalse() {
        Info returnedInfo = info.beanify(false);
        assertNotNull(returnedInfo);
        assertSame(info, returnedInfo);
        assertFalse(getBeanifyFieldValue());
    }

    private boolean getBeanifyFieldValue() {
        try {
            Method method = Info.class.getDeclaredMethod("beanify");
            method.setAccessible(true);
            return (boolean) method.invoke(info);
        } catch (Exception e) {
            fail("Reflection failed: " + e.getMessage());
            return false;
        }
    }
}
