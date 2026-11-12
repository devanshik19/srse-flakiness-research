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
    private ServiceBasedNamingStore store;

    private static final Object NULL_VALUE = new Object();

    @Before
    public void setUp() {
        ServiceRegistry registry = (ServiceRegistry) Proxy.newProxyInstance(getClass().getClassLoader(),
                new Class<?>[]{ServiceRegistry.class}, new InvocationHandler() {
                    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                        if (method.getName().equals("getService")) {
                            final Object v = values.get(args[0]);
                            if (v == null) {
                                return null;
                            }
                            return controller(v);
                        }
                        if (method.getName().equals("hashCode")) return 1;
                        if (method.getName().equals("equals")) return proxy == args[0];
                        return null;
                    }
                });
        store = new ServiceBasedNamingStore(registry, ServiceName.JBOSS);
    }

    private ServiceController<?> controller(final Object v) {
        return (ServiceController<?>) Proxy.newProxyInstance(getClass().getClassLoader(),
                new Class<?>[]{ServiceController.class}, new InvocationHandler() {
                    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                        if (method.getName().equals("getValue")) {
                            if (v instanceof Throwable) {
                                throw (Throwable) v;
                            }
                            return v == NULL_VALUE ? null : v;
                        }
                        if (method.getName().equals("hashCode")) return 1;
                        if (method.getName().equals("equals")) return proxy == args[0];
                        return null;
                    }
                });
    }

    @Test
    public void testEmptyName() throws Exception {
        Object o = store.lookup(new CompositeName());
        assertTrue(o instanceof NamingContext);
    }

    @Test
    public void testDirectValue() throws Exception {
        Object v = "value";
        values.put(ServiceName.JBOSS.append("foo", "bar"), v);
        assertSame(v, store.lookup(new CompositeName("foo/bar")));
    }

    @Test
    public void testEmptyComponentsSkipped() throws Exception {
        Object v = "value";
        values.put(ServiceName.JBOSS.append("foo", "bar"), v);
        assertSame(v, store.lookup(new CompositeName("foo//bar")));
    }

    @Test
    public void testManagedReferenceFactoryDereferenced() throws Exception {
        values.put(ServiceName.JBOSS.append("mrf"), new ManagedReferenceFactory() {
            public ManagedReference getReference() {
                return new ManagedReference() {
                    public void release() {
                    }

                    public Object getInstance() {
                        return "instance";
                    }
                };
            }
        });
        assertEquals("instance", store.lookup(new CompositeName("mrf")));
    }

    @Test
    public void testManagedReferenceFactoryNullReference() throws Exception {
        values.put(ServiceName.JBOSS.append("mrf"), new ManagedReferenceFactory() {
            public ManagedReference getReference() {
                return null;
            }
        });
        // returns null -> not bound -> NameNotFound
        try {
            store.lookup(new CompositeName("mrf"));
            fail();
        } catch (NameNotFoundException expected) {
        }
        store.add(ServiceName.JBOSS.append("mrf"));
        assertNull(store.lookup(new CompositeName("mrf")));
    }

    @Test(expected = NameNotFoundException.class)
    public void testNotFound() throws Exception {
        store.lookup(new CompositeName("missing"));
    }

    @Test
    public void testParentContext() throws Exception {
        store.add(ServiceName.JBOSS.append("foo", "bar"));
        Object o = store.lookup(new CompositeName("foo"));
        assertTrue(o instanceof NamingContext);
    }

    @Test
    public void testBoundButNullValue() throws Exception {
        store.add(ServiceName.JBOSS.append("foo"));
        assertNull(store.lookup(new CompositeName("foo")));
    }

    @Test
    public void testResolveResultFromParent() throws Exception {
        ServiceName parent = ServiceName.JBOSS.append("link");
        store.add(parent);
        values.put(parent, "linked");
        Object o = store.lookup(new CompositeName("link/a/b"));
        assertTrue(o instanceof ResolveResult);
        ResolveResult rr = (ResolveResult) o;
        assertEquals("linked", rr.getResolvedObj());
        assertEquals(new CompositeName("a/b"), rr.getRemainingName());
    }

    @Test
    public void testReferenceWithoutNns() throws Exception {
        ServiceName parent = ServiceName.JBOSS.append("ref");
        store.add(parent);
        Reference ref = new Reference("java.lang.String");
        values.put(parent, ref);
        Object o = store.lookup(new CompositeName("ref/x"));
        assertTrue(o instanceof ResolveResult);
        assertSame(ref, ((ResolveResult) o).getResolvedObj());
    }

    @Test
    public void testReferenceWithNns() throws Exception {
        ServiceName parent = ServiceName.JBOSS.append("ref");
        store.add(parent);
        Reference ref = new Reference("java.lang.String", new StringRefAddr("nns", "x"));
        values.put(parent, ref);
        try {
            store.lookup(new CompositeName("ref/x"));
            fail();
        } catch (CannotProceedException e) {
            assertSame(ref, e.getResolvedObj());
            assertEquals(new CompositeName("ref/x"), e.getRemainingName());
        }
    }

    @Test(expected = NameNotFoundException.class)
    public void testParentIsNamingContextFallsThrough() throws Exception {
        ServiceName parent = ServiceName.JBOSS.append("ctx");
        store.add(parent);
        values.put(parent, new NamingContext(new CompositeName(), store, null));
        store.lookup(new CompositeName("ctx/a"));
    }

    @Test
    public void testParentIsNamingContextWithChild() throws Exception {
        ServiceName parent = ServiceName.JBOSS.append("ctx");
        store.add(parent);
        store.add(parent.append("a", "b"));
        values.put(parent, new NamingContext(new CompositeName(), store, null));
        Object o = store.lookup(new CompositeName("ctx/a"));
        assertTrue(o instanceof NamingContext);
    }

    @Test(expected = NameNotFoundException.class)
    public void testLowerNotParent() throws Exception {
        store.add(ServiceName.JBOSS.append("aaa"));
        store.lookup(new CompositeName("bbb"));
    }

    @Test(expected = NameNotFoundException.class)
    public void testCeilingNotChild() throws Exception {
        store.add(ServiceName.JBOSS.append("zzz"));
        store.lookup(new CompositeName("bbb"));
    }

    @Test
    public void testIllegalStateException() throws Exception {
        values.put(ServiceName.JBOSS.append("ise"), new IllegalStateException("x"));
        try {
            store.lookup(new CompositeName("ise"));
            fail();
        } catch (NameNotFoundException e) {
            assertTrue(e.getCause() instanceof IllegalStateException);
        }
    }

    @Test(expected = SecurityException.class)
    public void testSecurityException() throws Exception {
        values.put(ServiceName.JBOSS.append("sec"), new SecurityException("x"));
        store.lookup(new CompositeName("sec"));
    }

    @Test
    public void testOtherThrowable() throws Exception {
        values.put(ServiceName.JBOSS.append("err"), new RuntimeException("x"));
        try {
            store.lookup(new CompositeName("err"));
            fail();
        } catch (NamingException e) {
            assertFalse(e instanceof NameNotFoundException);
        }
    }
}
