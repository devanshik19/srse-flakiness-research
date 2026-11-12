package org.apache.commons.lang3.builder;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

public class HashCodeBuilder_reflectionHashCode_0_0_Test {

    static class Base {
        int b = 3;
    }

    static class Sub extends Base {
        int a = 5;
        String s = "x";
        transient int t = 9;
        static int st = 11;
        @HashCodeExclude
        int ex = 13;
    }

    static class SelfRef {
        int v = 2;
        SelfRef self;
    }

    @Test
    public void testNullObjectThrows() {
        assertThrows(IllegalArgumentException.class, () -> HashCodeBuilder.reflectionHashCode(null, (String[]) null));
    }

    @Test
    public void testNoExcludes() {
        Sub o = new Sub();
        int expected = new HashCodeBuilder(17, 37).append(5).append("x").append(3).toHashCode();
        assertEquals(expected, HashCodeBuilder.reflectionHashCode(o));
        assertEquals(expected, HashCodeBuilder.reflectionHashCode(o, (String[]) null));
    }

    @Test
    public void testWithExcludes() {
        Sub o = new Sub();
        int expected = new HashCodeBuilder(17, 37).append("x").toHashCode();
        assertEquals(expected, HashCodeBuilder.reflectionHashCode(o, "a", "b"));
        int expected2 = new HashCodeBuilder(17, 37).append(5).append("x").append(3).toHashCode();
        assertEquals(expected2, HashCodeBuilder.reflectionHashCode(o, "nonexistent"));
    }

    @Test
    public void testPlainObject() {
        assertEquals(17, HashCodeBuilder.reflectionHashCode(new Object()));
    }

    @Test
    public void testSelfReference() {
        SelfRef r = new SelfRef();
        r.self = r;
        int h = HashCodeBuilder.reflectionHashCode(r);
        assertEquals(h, HashCodeBuilder.reflectionHashCode(r));
        assertNull(HashCodeBuilder.getRegistry());
    }
}
