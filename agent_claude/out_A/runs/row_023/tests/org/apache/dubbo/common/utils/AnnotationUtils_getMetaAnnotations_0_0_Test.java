package org.apache.dubbo.common.utils;

import org.junit.jupiter.api.Test;

import java.lang.annotation.Annotation;
import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Inherited;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.util.List;
import java.util.function.Predicate;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class AnnotationUtils_getMetaAnnotations_0_0_Test {

    @Retention(RetentionPolicy.RUNTIME)
    @Target({ElementType.TYPE, ElementType.ANNOTATION_TYPE})
    public @interface MetaA {
    }

    @Retention(RetentionPolicy.RUNTIME)
    @Target({ElementType.TYPE, ElementType.ANNOTATION_TYPE})
    public @interface MetaB {
    }

    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.TYPE)
    @Documented
    @Inherited
    @MetaA
    @MetaB
    public @interface Composite {
    }

    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.TYPE)
    @Documented
    public @interface Plain {
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testNoPredicates() {
        List<Annotation> list = AnnotationUtils.getMetaAnnotations(Composite.class);
        assertEquals(3, list.size());
        assertEquals(Inherited.class, list.get(0).annotationType());
        assertEquals(MetaA.class, list.get(1).annotationType());
        assertEquals(MetaB.class, list.get(2).annotationType());
        assertThrows(UnsupportedOperationException.class, () -> list.add(null));
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testWithSinglePredicate() {
        List<Annotation> list = AnnotationUtils.getMetaAnnotations(Composite.class,
                a -> a.annotationType() == MetaA.class);
        assertEquals(1, list.size());
        assertEquals(MetaA.class, list.get(0).annotationType());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testWithMultiplePredicates() {
        Predicate<Annotation> notInherited = a -> a.annotationType() != Inherited.class;
        Predicate<Annotation> notMetaA = a -> a.annotationType() != MetaA.class;
        List<Annotation> list = AnnotationUtils.getMetaAnnotations(Composite.class, notInherited, notMetaA);
        assertEquals(1, list.size());
        assertEquals(MetaB.class, list.get(0).annotationType());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testPredicateRejectsAll() {
        List<Annotation> list = AnnotationUtils.getMetaAnnotations(Composite.class, a -> false);
        assertTrue(list.isEmpty());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testOnlyNativeMetaAnnotations() {
        assertTrue(AnnotationUtils.getMetaAnnotations(Plain.class).isEmpty());
        assertTrue(AnnotationUtils.getMetaAnnotations(Target.class).isEmpty());
        assertTrue(AnnotationUtils.getMetaAnnotations(Retention.class).isEmpty());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testNullType() {
        assertTrue(AnnotationUtils.getMetaAnnotations(null).isEmpty());
    }
}
