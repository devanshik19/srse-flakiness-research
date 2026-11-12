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
import org.jboss.msc.service.ServiceTarget;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class WritableServiceBasedNamingStore_bind_0_0_Test {

    private ServiceContainer container;
    private WritableServiceBasedNamingStore store;
    private static final ServiceName OWNER = ServiceName.of("OwnerX");

    @Before
    public void setup() throws Exception {
        container = ServiceContainer.Factory.create();
        final CountDownLatch l1 = new CountDownLatch(1);
        container.addService(JndiNamingDependencyProcessor.serviceName(OWNER), new RuntimeBindReleaseService())
                .setInitialMode(ServiceController.Mode.ACTIVE)
                .addListener(latchListener(l1)).install();
        l1.await(10, TimeUnit.SECONDS);
        final CountDownLatch l2 = new CountDownLatch(1);
        final NamingStoreService nss = new NamingStoreService();
        container.addService(ContextNames.JAVA_CONTEXT_SERVICE_NAME, nss)
                .setInitialMode(ServiceController.Mode.ACTIVE)
                .addListener(latchListener(l2)).install();
        l2.await(10, TimeUnit.SECONDS);
        store = (WritableServiceBasedNamingStore) nss.getValue();
    }

    private LifecycleListener latchListener(final CountDownLatch latch) {
        return new LifecycleListener() {
            public void handleEvent(ServiceController<?> controller, LifecycleEvent event) {
                if (event == LifecycleEvent.UP || event == LifecycleEvent.FAILED) {
                    latch.countDown();
                }
            }
        };
    }

    @After
    public void tearDown() throws Exception {
        if (container != null) {
            container.shutdown();
            container.awaitTermination(5, TimeUnit.SECONDS);
            container = null;
        }
        store = null;
    }

    @Test
    public void testBindNoOwner() throws Exception {
        try {
            store.bind(new CompositeName("test"), new Object());
            fail();
        } catch (UnsupportedOperationException expected) {
        }
    }

    @Test
    public void testBindWithServiceNameOwner() throws Exception {
        final Name name = new CompositeName("a/b");
        final Object value = new Object();
        WritableServiceBasedNamingStore.pushOwner(OWNER);
        try {
            store.bind(name, value);
        } finally {
            WritableServiceBasedNamingStore.popOwner();
        }
        assertSame(value, store.lookup(name));
        RuntimeBindReleaseService.References refs = (RuntimeBindReleaseService.References) container
                .getService(JndiNamingDependencyProcessor.serviceName(OWNER)).getValue();
        assertNotNull(refs);
    }

    @Test
    public void testBindWithServiceTargetOwner() throws Exception {
        final Name name = new CompositeName("target");
        final Object value = "val";
        WritableServiceBasedNamingStore.pushOwner((ServiceTarget) container);
        try {
            store.bind(name, value);
        } finally {
            WritableServiceBasedNamingStore.popOwner();
        }
        assertEquals(value, store.lookup(name));
    }

    @Test
    public void testBindDuplicateFails() throws Exception {
        final Name name = new CompositeName("dup");
        WritableServiceBasedNamingStore.pushOwner(OWNER);
        try {
            store.bind(name, "one");
            try {
                store.bind(name, "two");
                fail();
            } catch (NamingException expected) {
                assertNotNull(expected.getMessage());
            }
        } finally {
            WritableServiceBasedNamingStore.popOwner();
        }
    }

    @Test
    public void testBindMissingOwnerReferencesFails() throws Exception {
        WritableServiceBasedNamingStore.pushOwner(ServiceName.of("NoSuchOwner"));
        try {
            store.bind(new CompositeName("x"), "v");
            fail();
        } catch (NamingException expected) {
        } finally {
            WritableServiceBasedNamingStore.popOwner();
        }
    }
}
