package io.elasticjob.lite.reg.zookeeper;

import io.elasticjob.lite.fixture.EmbedTestingServer;
import io.elasticjob.lite.reg.exception.RegException;
import org.apache.curator.framework.CuratorFramework;
import org.apache.zookeeper.KeeperException;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.stubbing.Answer;

import java.lang.reflect.Field;

import static org.hamcrest.CoreMatchers.startsWith;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public final class ZookeeperRegistryCenter_persistSequential_0_0_Test {
    
    private static final ZookeeperConfiguration ZOOKEEPER_CONFIGURATION = new ZookeeperConfiguration(EmbedTestingServer.getConnectionString(), ZookeeperRegistryCenter_persistSequential_0_0_Test.class.getName());
    
    private static ZookeeperRegistryCenter zkRegCenter;
    
    @BeforeClass
    public static void setUp() {
        EmbedTestingServer.start();
        ZOOKEEPER_CONFIGURATION.setConnectionTimeoutMilliseconds(30000);
        zkRegCenter = new ZookeeperRegistryCenter(ZOOKEEPER_CONFIGURATION);
        zkRegCenter.init();
    }
    
    @AfterClass
    public static void tearDown() {
        zkRegCenter.close();
    }
    
    @After
    public void clearInterrupt() {
        Thread.interrupted();
    }
    
    private ZookeeperRegistryCenter centerWithClient(final CuratorFramework client) throws Exception {
        ZookeeperRegistryCenter center = new ZookeeperRegistryCenter(new ZookeeperConfiguration("localhost:1", "ns"));
        Field field = ZookeeperRegistryCenter.class.getDeclaredField("client");
        field.setAccessible(true);
        field.set(center, client);
        return center;
    }
    
    private CuratorFramework throwingClient(final Exception ex) {
        CuratorFramework client = mock(CuratorFramework.class);
        when(client.create()).thenAnswer(new Answer<Object>() {
            @Override
            public Object answer(final InvocationOnMock invocation) throws Throwable {
                throw ex;
            }
        });
        return client;
    }
    
    @Test
    public void assertPersistSequentialSuccess() {
        String result = zkRegCenter.persistSequential("/sequential/test_sequential", "test_value");
        assertThat(result, startsWith("/sequential/test_sequential"));
        String result2 = zkRegCenter.persistSequential("/sequential/test_sequential", "test_value2");
        assertTrue(result2.compareTo(result) > 0);
        assertEquals("test_value", zkRegCenter.getDirectly(result.substring(0)));
    }
    
    @Test(expected = RegException.class)
    public void assertPersistSequentialWithRuntimeException() throws Exception {
        centerWithClient(throwingClient(new RuntimeException("fail"))).persistSequential("/a", "b");
    }
    
    @Test
    public void assertPersistSequentialWithIgnoredException() throws Exception {
        assertNull(centerWithClient(throwingClient(new KeeperException.NoNodeException())).persistSequential("/a", "b"));
        assertNull(centerWithClient(throwingClient(new KeeperException.NodeExistsException())).persistSequential("/a", "b"));
        assertNull(centerWithClient(throwingClient(new KeeperException.ConnectionLossException())).persistSequential("/a", "b"));
    }
    
    @Test
    public void assertPersistSequentialWithIgnoredCause() throws Exception {
        assertNull(centerWithClient(throwingClient(new RuntimeException(new KeeperException.NoNodeException()))).persistSequential("/a", "b"));
    }
    
    @Test
    public void assertPersistSequentialWithInterruptedException() throws Exception {
        assertNull(centerWithClient(throwingClient(new InterruptedException())).persistSequential("/a", "b"));
        assertTrue(Thread.currentThread().isInterrupted());
    }
    
    @Test(expected = RegException.class)
    public void assertPersistSequentialWithNullValue() {
        zkRegCenter.persistSequential("/sequential/null", null);
    }
}
