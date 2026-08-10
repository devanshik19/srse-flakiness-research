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

public class Info_pointerTypes_5_0_Test {

    private Info info;

    @BeforeEach
    public void setUp() {
        info = new Info();
    }

    @Test
    public void testPointerTypesWithNull() {
        info.pointerTypes((String[]) null);
        assertNull(info.pointerTypes, "pointerTypes should be null when null is passed.");
    }

    @Test
    public void testPointerTypesWithEmptyArray() {
        info.pointerTypes();
        assertNotNull(info.pointerTypes, "pointerTypes should not be null when an empty array is passed.");
        assertEquals(0, info.pointerTypes.length, "pointerTypes should be empty.");
    }

    @Test
    public void testPointerTypesWithNonEmptyArray() {
        String[] types = { "int*", "char*" };
        info.pointerTypes(types);
        assertNotNull(info.pointerTypes, "pointerTypes should not be null when a non-empty array is passed.");
        assertArrayEquals(types, info.pointerTypes, "pointerTypes should match the input array.");
    }

    @Test
    public void testPointerTypesReturnsSelf() {
        Info result = info.pointerTypes("int*");
        assertSame(info, result, "pointerTypes method should return the same Info instance.");
    }
}
