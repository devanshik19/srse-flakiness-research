package org.bytedeco.javacpp.tools;

import org.bytedeco.javacpp.tools.Info;
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

public class Info_objectify_22_0_Test {

    @Test
    public void testObjectifyTrue() throws Exception {
        Info info = new Info();
        Method objectifyMethod = Info.class.getDeclaredMethod("objectify", boolean.class);
        objectifyMethod.setAccessible(true);
        Info result = (Info) objectifyMethod.invoke(info, true);
        assertEquals(true, info.objectify);
        assertEquals(info, result);
    }

    @Test
    public void testObjectifyFalse() throws Exception {
        Info info = new Info();
        Method objectifyMethod = Info.class.getDeclaredMethod("objectify", boolean.class);
        objectifyMethod.setAccessible(true);
        Info result = (Info) objectifyMethod.invoke(info, false);
        assertEquals(false, info.objectify);
        assertEquals(info, result);
    }
}
