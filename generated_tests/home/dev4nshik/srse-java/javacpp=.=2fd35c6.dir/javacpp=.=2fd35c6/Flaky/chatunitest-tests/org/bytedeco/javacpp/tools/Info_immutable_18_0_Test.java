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

public class Info_immutable_18_0_Test {

    @Test
    public void testImmutableTrue() throws NoSuchFieldException, IllegalAccessException {
        Info info = new Info();
        info.immutable(true);
        Field immutableField = Info.class.getDeclaredField("immutable");
        immutableField.setAccessible(true);
        boolean immutableValue = (boolean) immutableField.get(info);
        assertTrue(immutableValue, "The immutable field should be true.");
    }

    @Test
    public void testImmutableFalse() throws NoSuchFieldException, IllegalAccessException {
        Info info = new Info();
        info.immutable(false);
        Field immutableField = Info.class.getDeclaredField("immutable");
        immutableField.setAccessible(true);
        boolean immutableValue = (boolean) immutableField.get(info);
        assertFalse(immutableValue, "The immutable field should be false.");
    }
}
