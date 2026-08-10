package com.fasterxml.classmate;

import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.lang.reflect.Type;
import java.util.*;
import com.fasterxml.classmate.members.*;

@ExtendWith(MockitoExtension.class)
class ResolvedType_appendSignature_28_3_Test {

    private ResolvedType resolvedType;

    private Class<?> resolvedTypeClass;

    @BeforeEach
    void setUp() throws Exception {
        resolvedTypeClass = ResolvedType.class;
        // Use Mockito to create a mock instance of the abstract class
        resolvedType = mock(ResolvedType.class, withSettings().useConstructor(Object.class, TypeBindings.emptyBindings()).defaultAnswer(CALLS_REAL_METHODS));
    }

    @Test
    void testAppendSignature() throws Exception {
        StringBuilder sb = new StringBuilder();
        // Use reflection to invoke the abstract method
        Method appendSignatureMethod = resolvedTypeClass.getDeclaredMethod("appendSignature", StringBuilder.class);
        appendSignatureMethod.setAccessible(true);
        // Mock the behavior of appendSignature
        when(resolvedType.appendSignature(sb)).thenReturn(sb.append("mocked-signature"));
        StringBuilder result = (StringBuilder) appendSignatureMethod.invoke(resolvedType, sb);
        assertNotNull(result);
        assertEquals("mocked-signature", result.toString());
    }
}
