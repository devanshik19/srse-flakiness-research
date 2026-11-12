package com.hellokaton.blade.options;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.util.HashSet;
import java.util.Set;

import static org.junit.Assert.*;

public class StaticOptions_addStatic_0_0_Test {

    private Set<String> snapshot;

    @Before
    public void setUp() {
        snapshot = new HashSet<>(StaticOptions.DEFAULT_STATICS);
    }

    @After
    public void tearDown() {
        StaticOptions.DEFAULT_STATICS.clear();
        StaticOptions.DEFAULT_STATICS.addAll(snapshot);
    }

    @Test
    public void testAddStaticReturnsSameInstanceAndAdds() {
        StaticOptions options = new StaticOptions();
        options.setPaths(new HashSet<>());
        StaticOptions result = options.addStatic("/assets");
        assertSame(options, result);
        assertTrue(options.getPaths().contains("/assets"));
        assertEquals(1, options.getPaths().size());
    }

    @Test
    public void testAddStaticDuplicate() {
        StaticOptions options = new StaticOptions();
        options.setPaths(new HashSet<>());
        options.addStatic("/a").addStatic("/a").addStatic("/b");
        assertEquals(2, options.getPaths().size());
        assertTrue(options.getPaths().contains("/b"));
    }

    @Test
    public void testAddStaticNull() {
        StaticOptions options = new StaticOptions();
        options.setPaths(new HashSet<>());
        options.addStatic(null);
        assertTrue(options.getPaths().contains(null));
    }

    @Test
    public void testAddStaticOnDefaultPaths() {
        StaticOptions options = new StaticOptions();
        options.addStatic("/upload");
        assertTrue(options.getPaths().contains("/upload"));
        assertTrue(options.getPaths().contains("/static"));
        assertTrue(options.getPaths().contains("/favicon.ico"));
    }

    @Test(expected = UnsupportedOperationException.class)
    public void testAddStaticImmutableSet() {
        StaticOptions options = new StaticOptions();
        options.setPaths(java.util.Collections.<String>emptySet());
        options.addStatic("/x");
    }
}
