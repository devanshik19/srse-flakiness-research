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

class Info_cppNames_0_0_Test {

    @Test
    void testCppNames() {
        // Create an instance of Info
        Info info = new Info();
        // Test with empty array
        String[] emptyArray = {};
        Info result = info.cppNames(emptyArray);
        assertArrayEquals(emptyArray, info.cppNames);
        assertSame(info, result);
        // Test with a single element
        String[] singleElement = { "name1" };
        result = info.cppNames(singleElement);
        assertArrayEquals(singleElement, info.cppNames);
        assertSame(info, result);
        // Test with multiple elements
        String[] multipleElements = { "name1", "name2", "name3" };
        result = info.cppNames(multipleElements);
        assertArrayEquals(multipleElements, info.cppNames);
        assertSame(info, result);
        // Test with null
        result = info.cppNames((String[]) null);
        assertNull(info.cppNames);
        assertSame(info, result);
    }
}
