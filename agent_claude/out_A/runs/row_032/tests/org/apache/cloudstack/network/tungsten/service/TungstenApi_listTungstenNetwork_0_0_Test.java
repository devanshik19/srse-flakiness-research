package org.apache.cloudstack.network.tungsten.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import net.juniper.tungsten.api.ApiConnector;
import net.juniper.tungsten.api.ApiObjectBase;
import net.juniper.tungsten.api.types.Project;
import net.juniper.tungsten.api.types.VirtualNetwork;

import org.junit.Before;
import org.junit.Test;

public class TungstenApi_listTungstenNetwork_0_0_Test {

    private TungstenApi api;
    private ApiConnector connector;
    private Project project;

    @Before
    public void setUp() throws IOException {
        api = new TungstenApi();
        connector = mock(ApiConnector.class);
        api.setApiConnector(connector);
        project = new Project();
        project.setName("p1");
        doReturn(project).when(connector).findById(Project.class, "proj");
    }

    @Test
    public void testWithNetworkUuid() throws IOException {
        VirtualNetwork vn = new VirtualNetwork();
        doReturn(vn).when(connector).findById(VirtualNetwork.class, "net");
        List<ApiObjectBase> result = api.listTungstenNetwork("proj", "net");
        assertEquals(1, result.size());
        assertSame(vn, result.get(0));
    }

    @Test
    public void testWithoutNetworkUuidList() throws IOException {
        VirtualNetwork vn1 = new VirtualNetwork();
        vn1.setUuid("u1");
        VirtualNetwork vn2 = new VirtualNetwork();
        vn2.setUuid("u2");
        VirtualNetwork full1 = new VirtualNetwork();
        VirtualNetwork full2 = new VirtualNetwork();
        doReturn(Arrays.asList(vn1, vn2)).when(connector).list(eq(VirtualNetwork.class), anyList());
        doReturn(full1).when(connector).findById(VirtualNetwork.class, "u1");
        doReturn(full2).when(connector).findById(VirtualNetwork.class, "u2");
        List<ApiObjectBase> result = api.listTungstenNetwork("proj", null);
        assertEquals(2, result.size());
        assertSame(full1, result.get(0));
        assertSame(full2, result.get(1));
    }

    @Test
    public void testWithoutNetworkUuidNullList() throws IOException {
        doReturn(null).when(connector).list(eq(VirtualNetwork.class), anyList());
        assertTrue(api.listTungstenNetwork("proj", null).isEmpty());
    }

    @Test
    public void testWithoutNetworkUuidEmptyList() throws IOException {
        doReturn(new ArrayList<>()).when(connector).list(eq(VirtualNetwork.class), anyList());
        assertTrue(api.listTungstenNetwork("proj", null).isEmpty());
    }

    @Test
    public void testIOExceptionOnFindNetwork() throws IOException {
        doThrow(new IOException("x")).when(connector).findById(VirtualNetwork.class, "net");
        assertTrue(api.listTungstenNetwork("proj", "net").isEmpty());
    }

    @Test
    public void testIOExceptionOnList() throws IOException {
        doThrow(new IOException("x")).when(connector).list(eq(VirtualNetwork.class), anyList());
        assertTrue(api.listTungstenNetwork("proj", null).isEmpty());
    }

    @Test
    public void testProjectLookupIOExceptionWithNetworkUuid() throws IOException {
        doThrow(new IOException("x")).when(connector).findById(Project.class, "bad");
        VirtualNetwork vn = new VirtualNetwork();
        doReturn(vn).when(connector).findById(VirtualNetwork.class, "net");
        List<ApiObjectBase> result = api.listTungstenNetwork("bad", "net");
        assertEquals(1, result.size());
        assertSame(vn, result.get(0));
    }
}
