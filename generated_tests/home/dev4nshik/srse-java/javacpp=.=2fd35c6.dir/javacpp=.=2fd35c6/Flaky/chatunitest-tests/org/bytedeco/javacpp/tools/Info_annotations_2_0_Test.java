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

public class Info_annotations_2_0_Test {

    private Info info;

    @BeforeEach
    public void setUp() {
        info = new Info();
    }

    @Test
    public void testAnnotationsWithEmptyArray() {
        String[] annotationsArray = {};
        Info result = info.annotations(annotationsArray);
        assertNotNull(result);
        assertArrayEquals(annotationsArray, result.annotations);
    }

    @Test
    public void testAnnotationsWithNonEmptyArray() {
        String[] annotationsArray = { "@Override", "@Deprecated" };
        Info result = info.annotations(annotationsArray);
        assertNotNull(result);
        assertArrayEquals(annotationsArray, result.annotations);
    }

    @Test
    public void testAnnotationsWithNull() {
        Info result = info.annotations((String[]) null);
        assertNotNull(result);
        assertNull(result.annotations);
    }

    @Test
    public void testAnnotationsReturnType() {
        Info result = info.annotations("@Test");
        assertSame(info, result);
    }
}
