package org.jboss.as.naming;

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
import org.jboss.msc.service.Service;
import org.jboss.msc.service.ServiceContainer;
import org.jboss.msc.service.ServiceController;
import org.jboss.msc.service.ServiceName;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class WritableServiceBasedNamingStore_bind_0_0_Test {
    private ServiceContainer container;
    private WritableServiceBasedNamingStore store;
    private static final ServiceName OWNER_FOO = ServiceName.of("Foo");
    private static final ServiceName OWNER_NOREF = ServiceName.of("NoRef");

    @Before
    public void setup() throws Exception {
        container = ServiceContainer.Factory.create();
        install(JndiNamingDependencyProcessor.serviceName(OWNER_FOO), new RuntimeBindReleaseService());
        NamingStoreService nss = new NamingStoreService();
        install(ContextNames.JAVA_CONTEXT_SERVICE_NAME, nss);
        store = (WritableServiceBasedNamingStore) nss.getValue();
    }

    private void install(ServiceName name, Service<?> service) throws InterruptedException {
        final CountDownLatch latch = new CountDownLatch(1);
        container.addService(name, service).setInitialMode(ServiceController.Mode.ACTIVE)
                .addListener(new LifecycleListener() {
                    public void handleEvent(ServiceController<?> controller, LifecycleEvent event) {
                        if (event == LifecycleEvent.UP || event == LifecycleEvent.FAILED) {
                            latch.countDown();
                        }
                    }
                }).install();
        latch.await(10, TimeUnit.SECONDS);
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
    public void testBindServiceNameOwner() throws Exception {
        Name name = new CompositeName("a/b");
        Object value = new Object();
        WritableServiceBasedNamingStore.pushOwner(OWNER_FOO);
        try {
            store.bind(name, value);
        } finally {
            WritableServiceBasedNamingStore.popOwner();
        }
        assertSame(value, store.lookup(name));
        assertNotNull(container.getService(ContextNames.JAVA_CONTEXT_SERVICE_NAME.append("a", "b")));
    }

    @Test
    public void testBindServiceTargetOwner() throws Exception {
        Name name = new CompositeName("target");
        Object value = "value";
        WritableServiceBasedNamingStore.pushOwner(container.subTarget());
        try {
            store.bind(name, value);
        } finally {
            WritableServiceBasedNamingStore.popOwner();
        }
        assertEquals(value, store.lookup(name));
    }

    @Test
    public void testBindDuplicateFails() throws Exception {
        Name name = new CompositeName("dup");
        WritableServiceBasedNamingStore.pushOwner(OWNER_FOO);
        try {
            store.bind(name, "v1");
            try {
                store.bind(name, "v2");
                fail();
            } catch (NamingException expected) {
                assertNotNull(expected.getMessage());
            }
        } finally {
            WritableServiceBasedNamingStore.popOwner();
        }
    }

    @Test
    public void testBindOwnerWithoutReferencesServiceFails() throws Exception {
        WritableServiceBasedNamingStore.pushOwner(OWNER_NOREF);
        try {
            store.bind(new CompositeName("noref"), "v");
            fail();
        } catch (NamingException expected) {
        } finally {
            WritableServiceBasedNamingStore.popOwner();
        }
    }
}
