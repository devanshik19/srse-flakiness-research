package org.jboss.as.naming;

import static org.junit.Assert.*;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.util.HashMap;
import java.util.Map;

import javax.naming.CannotProceedException;
import javax.naming.CompositeName;
import javax.naming.NameNotFoundException;
import javax.naming.NamingException;
import javax.naming.Reference;
import javax.naming.StringRefAddr;
import javax.naming.spi.ResolveResult;

import org.jboss.msc.service.ServiceController;
import org.jboss.msc.service.ServiceName;
import org.jboss.msc.service.ServiceRegistry;
import org.junit.Before;
import org.junit.Test;

public class ServiceBasedNamingStore_lookup_0_0_Test {

    private final Map<ServiceName, Object> values = new HashMap<ServiceName, Object>();
    private final Map<ServiceName, Throwable> errors = new HashMap<ServiceName, Throwable>();
    private ServiceBasedNamingStore store;
    private final ServiceName base = ServiceName.JBOSS;

    @Before
    public void setUp() {
        ServiceRegistry registry = (ServiceRegistry) Proxy.newProxyInstance(getClass().getClassLoader(),
                new Class<?>[]{ServiceRegistry.class}, new InvocationHandler() {
                    @Override
                    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                        if (method.getName().equals("getService")) {
                            final ServiceName sn = (ServiceName) args[0];
                            if (!values.containsKey(sn) && !errors.containsKey(sn)) {
                                return null;
                            }
                            return controller(sn);
                        }
                        return null;
                    }
                });
        store = new ServiceBasedNamingStore(registry, base);
    }

    private ServiceController<?> controller(final ServiceName sn) {
        return (ServiceController<?>) Proxy.newProxyInstance(getClass().getClassLoader(),
                new Class<?>[]{ServiceController.class}, new InvocationHandler() {
                    @Override
                    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                        if (method.getName().equals("getValue")) {
                            if (errors.containsKey(sn)) {
                                throw errors.get(sn);
                            }
                            return values.get(sn);
                        }
                        return null;
                    }
                });
    }

    private static ManagedReferenceFactory factory(final Object instance, final boolean nullRef) {
        return new ManagedReferenceFactory() {
            @Override
            public ManagedReference getReference() {
                if (nullRef) {
                    return null;
                }
                return new ManagedReference() {
                    @Override
                    public void release() {
                    }

                    @Override
                    public Object getInstance() {
                        return instance;
                    }
                };
            }
        };
    }

    @Test
    public void testEmptyName() throws Exception {
        Object o = store.lookup(new CompositeName());
        assertTrue(o instanceof NamingContext);
    }

    @Test
    public void testDirectValue() throws Exception {
        values.put(base.append("foo"), "bar");
        store.add(base.append("foo"));
        assertEquals("bar", store.lookup(new CompositeName("foo")));
    }

    @Test
    public void testEmptyComponentsSkipped() throws Exception {
        values.put(base.append("foo"), "bar");
        assertEquals("bar", store.lookup(new CompositeName("foo/")));
    }

    @Test
    public void testManagedReferenceFactoryDereferenced() throws Exception {
        values.put(base.append("mrf"), factory("inst", false));
        assertEquals("inst", store.lookup(new CompositeName("mrf")));
    }

    @Test
    public void testManagedReferenceFactoryNullReference() throws Exception {
        values.put(base.append("mrf"), factory("inst", true));
        store.add(base.append("mrf"));
        assertNull(store.lookup(new CompositeName("mrf")));
    }

    @Test
    public void testNotDereferenced() throws Exception {
        ManagedReferenceFactory f = factory("inst", false);
        values.put(base.append("mrf"), f);
        assertSame(f, store.lookup(new CompositeName("mrf"), false));
    }

    @Test(expected = NameNotFoundException.class)
    public void testNotFound() throws Exception {
        store.lookup(new CompositeName("missing"));
    }

    @Test
    public void testIllegalStateException() throws Exception {
        errors.put(base.append("bad"), new IllegalStateException("x"));
        try {
            store.lookup(new CompositeName("bad"));
            fail();
        } catch (NameNotFoundException e) {
            assertTrue(e.getCause() instanceof IllegalStateException);
        }
    }

    @Test(expected = SecurityException.class)
    public void testSecurityException() throws Exception {
        errors.put(base.append("sec"), new SecurityException("x"));
        store.lookup(new CompositeName("sec"));
    }

    @Test(expected = NamingException.class)
    public void testOtherThrowable() throws Exception {
        errors.put(base.append("err"), new RuntimeException("x"));
        store.lookup(new CompositeName("err"));
    }

    @Test
    public void testParentReturnsResolveResult() throws Exception {
        values.put(base.append("parent"), "linkObj");
        store.add(base.append("parent"));
        Object o = store.lookup(new CompositeName("parent/child/x"));
        assertTrue(o instanceof ResolveResult);
        ResolveResult rr = (ResolveResult) o;
        assertEquals("linkObj", rr.getResolvedObj());
        assertEquals(new CompositeName("child/x"), rr.getRemainingName());
    }

    @Test
    public void testParentReferenceWithoutNns() throws Exception {
        Reference ref = new Reference("java.lang.String");
        values.put(base.append("parent"), ref);
        store.add(base.append("parent"));
        Object o = store.lookup(new CompositeName("parent/child"));
        assertTrue(o instanceof ResolveResult);
        assertSame(ref, ((ResolveResult) o).getResolvedObj());
    }

    @Test
    public void testParentReferenceWithNns() throws Exception {
        Reference ref = new Reference("java.lang.String");
        ref.add(new StringRefAddr("nns", "value"));
        values.put(base.append("parent"), ref);
        store.add(base.append("parent"));
        try {
            store.lookup(new CompositeName("parent/child"));
            fail();
        } catch (CannotProceedException e) {
            assertSame(ref, e.getResolvedObj());
        }
    }

    @Test
    public void testParentIsNamingContextThenNotFound() throws Exception {
        values.put(base.append("ctx"), new NamingContext(new CompositeName(), store, null));
        store.add(base.append("ctx"));
        try {
            store.lookup(new CompositeName("ctx/child"));
            fail();
        } catch (NameNotFoundException expected) {
        }
    }

    @Test
    public void testParentIsNamingContextChildContext() throws Exception {
        values.put(base.append("ctx"), new NamingContext(new CompositeName(), store, null));
        store.add(base.append("ctx"));
        store.add(base.append("ctx", "child", "leaf"));
        Object o = store.lookup(new CompositeName("ctx/child"));
        assertTrue(o instanceof NamingContext);
    }

    @Test
    public void testLowerNotParent() throws Exception {
        store.add(base.append("a"));
        try {
            store.lookup(new CompositeName("b"));
            fail();
        } catch (NameNotFoundException expected) {
        }
    }

    @Test
    public void testBoundButNullValue() throws Exception {
        values.put(base.append("nullval"), null);
        store.add(base.append("nullval"));
        assertNull(store.lookup(new CompositeName("nullval")));
    }

    @Test
    public void testImplicitContext() throws Exception {
        store.add(base.append("comp", "env", "x"));
        Object o = store.lookup(new CompositeName("comp/env"));
        assertTrue(o instanceof NamingContext);
    }

    @Test
    public void testCeilingNotChild() throws Exception {
        store.add(base.append("zzz"));
        try {
            store.lookup(new CompositeName("aaa"));
            fail();
        } catch (NameNotFoundException expected) {
        }
    }
}
