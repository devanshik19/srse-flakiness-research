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

public class Info_cppTypes_3_0_Test {

    @Test
    public void testCppTypes() throws Exception {
        // Create an instance of the Info class
        Info info = new Info();
        // Define the input for the cppTypes method
        String[] inputCppTypes = { "int", "float", "double" };
        // Invoke the cppTypes method
        Info result = info.cppTypes(inputCppTypes);
        // Use reflection to access the private field 'cppTypes'
        java.lang.reflect.Field cppTypesField = Info.class.getDeclaredField("cppTypes");
        cppTypesField.setAccessible(true);
        String[] cppTypesValue = (String[]) cppTypesField.get(info);
        // Assert that the cppTypes field is set correctly
        assertArrayEquals(inputCppTypes, cppTypesValue);
        // Assert that the method returns the same instance (this)
        assertSame(info, result);
    }
}
