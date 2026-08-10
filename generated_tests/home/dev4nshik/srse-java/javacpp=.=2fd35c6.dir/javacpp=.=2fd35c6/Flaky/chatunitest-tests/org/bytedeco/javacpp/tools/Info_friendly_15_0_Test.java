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

public class Info_friendly_15_0_Test {

    private Info info;

    @BeforeEach
    public void setUp() {
        info = new Info();
    }

    @Test
    public void testFriendly() throws Exception {
        // Use reflection to invoke the private method friendly()
        java.lang.reflect.Method friendlyMethod = Info.class.getDeclaredMethod("friendly");
        friendlyMethod.setAccessible(true);
        Info result = (Info) friendlyMethod.invoke(info);
        // Assert that the returned object is not null
        assertNotNull(result);
        // Assert that the friendly field is set to true
        java.lang.reflect.Field friendlyField = Info.class.getDeclaredField("friendly");
        friendlyField.setAccessible(true);
        assertTrue((boolean) friendlyField.get(info));
    }
}
