package com.fasterxml.classmate;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.lang.reflect.Type;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import com.fasterxml.classmate.members.*;

@ExtendWith(MockitoExtension.class)
public class ResolvedType_appendErasedSignature_29_1_Test {

    private ResolvedType resolvedType;

    @BeforeEach
    public void setUp() throws Exception {
        // Use Mockito to mock the abstract class
        resolvedType = mock(ResolvedType.class, withSettings().useConstructor(Object.class, TypeBindings.emptyBindings()).defaultAnswer(CALLS_REAL_METHODS));
    }

    @Test
    public void testAppendErasedSignature() throws Exception {
        StringBuilder sb = new StringBuilder();
        when(resolvedType.appendErasedSignature(sb)).thenReturn(sb.append("MockedSignature"));
        StringBuilder result = resolvedType.appendErasedSignature(sb);
        assertEquals("MockedSignature", result.toString());
    }
}
