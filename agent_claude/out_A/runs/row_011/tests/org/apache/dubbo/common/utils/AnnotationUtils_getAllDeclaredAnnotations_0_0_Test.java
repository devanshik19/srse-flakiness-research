package org.apache.dubbo.common.utils;

import org.junit.jupiter.api.Test;

import java.lang.annotation.Annotation;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.lang.reflect.AnnotatedElement;
import java.lang.reflect.Method;
import java.util.List;
import java.util.function.Predicate;

import static org.junit.jupiter.api.Assertions.*;

public class AnnotationUtils_getAllDeclaredAnnotations_0_0_Test {

    @Retention(RetentionPolicy.RUNTIME)
    @Target({ElementType.TYPE, ElementType.METHOD})
    @interface A1 {}

    @Retention(RetentionPolicy.RUNTIME)
    @Target({ElementType.TYPE, ElementType.METHOD})
    @interface A2 {}

    @A1
    interface Iface {}

    @A2
    static class Parent {}

    @A1
    static class Child extends Parent implements Iface {
        @A1 @A2
        public void m() {}
        public void n() {}
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testClassElement() {
        AnnotatedElement e = Child.class;
        List<Annotation> list = AnnotationUtils.getAllDeclaredAnnotations(e);
        assertTrue(list.size() >= 3);
        List<Annotation> filtered = AnnotationUtils.getAllDeclaredAnnotations(e,
                (Predicate<Annotation>) a -> a.annotationType() == A2.class);
        assertEquals(1, filtered.size());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testMethodElement() throws Exception {
        Method m = Child.class.getMethod("m");
        AnnotatedElement e = m;
        assertEquals(2, AnnotationUtils.getAllDeclaredAnnotations(e).size());
        List<Annotation> filtered = AnnotationUtils.getAllDeclaredAnnotations(e,
                (Predicate<Annotation>) a -> a.annotationType() == A1.class);
        assertEquals(1, filtered.size());
        AnnotatedElement n = Child.class.getMethod("n");
        assertTrue(AnnotationUtils.getAllDeclaredAnnotations(n).isEmpty());
    }

    @Test
    public void testNull() {
        assertTrue(AnnotationUtils.getAllDeclaredAnnotations((AnnotatedElement) null).isEmpty());
    }
}
