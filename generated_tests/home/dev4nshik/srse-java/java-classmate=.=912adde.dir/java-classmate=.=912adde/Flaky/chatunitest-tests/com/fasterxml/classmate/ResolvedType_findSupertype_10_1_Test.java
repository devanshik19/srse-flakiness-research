package com.fasterxml.classmate;

import com.fasterxml.classmate.ResolvedType;
import com.fasterxml.classmate.TypeBindings;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.lang.reflect.Type;
import java.util.*;
import com.fasterxml.classmate.members.*;

class ResolvedType_findSupertype_10_1_Test {

    private ResolvedType resolvedType;

    private Class<?> testClass;

    private TypeBindings typeBindings;

    @BeforeEach
    void setUp() throws NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException {
        testClass = TestClass.class;
        typeBindings = TypeBindings.emptyBindings();
        // Use a mock for the abstract class
        resolvedType = mock(ResolvedType.class, withSettings().useConstructor(testClass, typeBindings).defaultAnswer(CALLS_REAL_METHODS));
    }

    @Test
    void testFindSupertype_SameType() {
        assertEquals(resolvedType, resolvedType.findSupertype(testClass));
    }

    @Test
    void testFindSupertype_NotFound() {
        assertNull(resolvedType.findSupertype(AnotherClass.class));
    }

    @Test
    void testFindSupertype_InterfaceType() {
        Class<?> interfaceType = InterfaceClass.class;
        ResolvedType interfaceResolvedType = mock(ResolvedType.class);
        when(resolvedType.getImplementedInterfaces()).thenReturn(List.of(interfaceResolvedType));
        when(interfaceResolvedType.findSupertype(interfaceType)).thenReturn(interfaceResolvedType);
        assertEquals(interfaceResolvedType, resolvedType.findSupertype(interfaceType));
    }

    @Test
    void testFindSupertype_ParentClassType() {
        Class<?> parentType = ParentClass.class;
        ResolvedType parentResolvedType = mock(ResolvedType.class);
        when(resolvedType.getParentClass()).thenReturn(parentResolvedType);
        when(parentResolvedType.findSupertype(parentType)).thenReturn(parentResolvedType);
        assertEquals(parentResolvedType, resolvedType.findSupertype(parentType));
    }

    // Mock class to use as a test class
    private static class TestClass {
    }

    // Additional mock classes
    private static class AnotherClass {
    }

    private interface InterfaceClass {
    }

    private static class ParentClass {
    }
}
