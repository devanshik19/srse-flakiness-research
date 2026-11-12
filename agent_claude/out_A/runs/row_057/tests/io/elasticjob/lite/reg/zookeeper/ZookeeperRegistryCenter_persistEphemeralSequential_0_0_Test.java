package io.elasticjob.lite.reg.zookeeper;

import io.elasticjob.lite.reg.exception.RegException;
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.api.ACLBackgroundPathAndBytesable;
import org.apache.curator.framework.api.CreateBuilder;
import org.apache.curator.framework.api.ProtectACLCreateModePathAndBytesable;
import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.KeeperException;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.lang.reflect.Field;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@SuppressWarnings("unchecked")
public class ZookeeperRegistryCenter_persistEphemeralSequential_0_0_Test {

    private ZookeeperRegistryCenter center;

    private ACLBackgroundPathAndBytesable<String> pathable;

    @Before
    public void setUp() throws Exception {
        center = new ZookeeperRegistryCenter(new ZookeeperConfiguration("localhost:1", "test"));
        CuratorFramework client = mock(CuratorFramework.class);
        CreateBuilder createBuilder = mock(CreateBuilder.class);
        ProtectACLCreateModePathAndBytesable<String> parents = mock(ProtectACLCreateModePathAndBytesable.class);
        pathable = mock(ACLBackgroundPathAndBytesable.class);
        when(client.create()).thenReturn(createBuilder);
        when(createBuilder.creatingParentsIfNeeded()).thenReturn(parents);
        when(parents.withMode(CreateMode.EPHEMERAL_SEQUENTIAL)).thenReturn(pathable);
        Field field = ZookeeperRegistryCenter.class.getDeclaredField("client");
        field.setAccessible(true);
        field.set(center, client);
    }

    @After
    public void tearDown() {
        Thread.interrupted();
    }

    @Test
    public void assertPersistSuccess() throws Exception {
        when(pathable.forPath("/seq")).thenReturn("/seq0000000001");
        center.persistEphemeralSequential("/seq");
        verify(pathable).forPath("/seq");
    }

    @Test
    public void assertIgnoredException() throws Exception {
        when(pathable.forPath("/seq")).thenThrow(new KeeperException.NodeExistsException());
        center.persistEphemeralSequential("/seq");
        verify(pathable).forPath("/seq");
    }

    @Test
    public void assertInterruptedException() throws Exception {
        when(pathable.forPath("/seq")).thenThrow(new InterruptedException());
        center.persistEphemeralSequential("/seq");
        assertTrue(Thread.interrupted());
    }

    @Test(expected = RegException.class)
    public void assertOtherException() throws Exception {
        when(pathable.forPath("/seq")).thenThrow(new RuntimeException("fail"));
        center.persistEphemeralSequential("/seq");
    }

    @Test
    public void assertNotInterruptedOnSuccess() throws Exception {
        center.persistEphemeralSequential("/seq");
        assertFalse(Thread.currentThread().isInterrupted());
    }
}
