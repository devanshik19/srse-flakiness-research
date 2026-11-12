package org.jboss.as.naming;

import static org.junit.Assert.*;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import javax.naming.CompositeName;
import javax.naming.Name;
import javax.naming.NamingException;

import org.jboss.as.naming.deployment.ContextNames;
import org.jboss.as.naming.deployment.JndiNamingDependencyProcessor;
import org.jboss.as.naming.deployment.RuntimeBindReleaseService;
import org.jboss.as.naming.service.NamingStoreService;
import org.jboss.msc.service.LifecycleEvent;
import org.jboss.msc.service.LifecycleListener;
import org.jboss.msc.service.ServiceContainer;
import org.jboss.msc.service.ServiceController;
import org.jboss.msc.service.ServiceName;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class WritableServiceBasedNamingStore_rebind_0_0_Test {
    private ServiceContainer container;
    private WritableServiceBasedNamingStore store;
    private static final ServiceName OWNER = ServiceName.of("RebindOwner");

    @Before
    public void setup() throws Exception {
        container = ServiceContainer.Factory.create();
        install(JndiNamingDependencyProcessor.serviceName(OWNER), new RuntimeBindReleaseService());
        NamingStoreService nss = new NamingStoreService();
        container.addService(ContextNames.JAVA_CONTEXT_SERVICE_NAME, nss)
                .setInitialMode(ServiceController.Mode.ACTIVE).install();
        container.awaitStability();
        store = (WritableServiceBasedNamingStore) nss.getValue();
    }

    private void install(ServiceName name, org.jboss.msc.service.Service<?> svc) throws Exception {
        final CountDownLatch latch = new CountDownLatch(1);
        container.addService(name, svc).setInitialMode(ServiceController.Mode.ACTIVE)
                .addListener(new LifecycleListener() {
                    public void handleEvent(ServiceController<?> c, LifecycleEvent e) {
                        if (e == LifecycleEvent.UP || e == LifecycleEvent.FAILED) latch.countDown();
                    }
                }).install();
        latch.await(10, TimeUnit.SECONDS);
    }

    @After
    public void tearDown() throws Exception {
        container.shutdown();
        container.awaitTermination();
    }

    private RuntimeBindReleaseService.References refs() {
        return (RuntimeBindReleaseService.References) container
                .getService(JndiNamingDependencyProcessor.serviceName(OWNER)).getValue();
    }

    @Test(expected = UnsupportedOperationException.class)
    public void testRebindNoOwner() throws Exception {
        store.rebind(new CompositeName("x"), new Object());
    }

    @Test
    public void testRebindNewWithServiceNameOwner() throws Exception {
        Name name = new CompositeName("a");
        Object v = new Object();
        WritableServiceBasedNamingStore.pushOwner(OWNER);
        try {
            store.rebind(name, v);
        } finally {
            WritableServiceBasedNamingStore.popOwner();
        }
        assertSame(v, store.lookup(name));
        assertTrue(refs().contains(store.buildServiceName(name)));
    }

    @Test
    public void testRebindExistingWithServiceNameOwner() throws Exception {
        Name name = new CompositeName("b");
        Object v1 = new Object();
        Object v2 = new Object();
        WritableServiceBasedNamingStore.pushOwner(OWNER);
        try {
            store.rebind(name, v1);
            store.rebind(name, v2);
        } finally {
            WritableServiceBasedNamingStore.popOwner();
        }
        assertSame(v2, store.lookup(name));
        assertTrue(refs().contains(store.buildServiceName(name)));
    }

    @Test
    public void testRebindNewAndExistingWithServiceTargetOwner() throws Exception {
        Name name = new CompositeName("c/d");
        Object v1 = new Object();
        Object v2 = new Object();
        WritableServiceBasedNamingStore.pushOwner(container.subTarget());
        try {
            store.rebind(name, v1);
            assertSame(v1, store.lookup(name));
            store.rebind(name, v2);
        } finally {
            WritableServiceBasedNamingStore.popOwner();
        }
        assertSame(v2, store.lookup(name));
        assertFalse(refs().contains(store.buildServiceName(name)));
    }

    @Test
    public void testRebindNewFailsWhenNoReferencesService() throws Exception {
        Name name = new CompositeName("e");
        WritableServiceBasedNamingStore.pushOwner(ServiceName.of("NoSuchOwner"));
        try {
            store.rebind(name, new Object());
            fail("expected NamingException");
        } catch (NamingException expected) {
            assertNotNull(expected.getMessage());
        } finally {
            WritableServiceBasedNamingStore.popOwner();
        }
    }
}
