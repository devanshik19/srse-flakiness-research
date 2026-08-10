package org.bytedeco.javacpp.tools;

import java.lang.reflect.Field;
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

public class Info_valueTypes_4_0_Test {

    private Info info;

    @BeforeEach
    public void setUp() {
        info = new Info();
    }

    @Test
    public void testValueTypes() throws NoSuchFieldException, IllegalAccessException {
        // Prepare test data
        String[] testValueTypes = { "int", "float", "double" };
        // Invoke the focal method
        Info result = info.valueTypes(testValueTypes);
        // Use reflection to access the private field 'valueTypes'
        Field valueTypesField = Info.class.getDeclaredField("valueTypes");
        valueTypesField.setAccessible(true);
        String[] actualValueTypes = (String[]) valueTypesField.get(info);
        // Assert the field was set correctly
        assertArrayEquals(testValueTypes, actualValueTypes);
        // Assert that the method returns the same instance
        assertSame(info, result);
    }
}
