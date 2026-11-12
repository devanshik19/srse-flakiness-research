package org.apache.dubbo.rpc.protocol.dubbo.telnet;

import org.apache.dubbo.common.URL;
import org.apache.dubbo.remoting.exchange.ExchangeChannel;
import org.apache.dubbo.remoting.exchange.ExchangeServer;
import org.apache.dubbo.rpc.protocol.dubbo.DubboProtocol;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.lang.reflect.Field;
import java.net.InetSocketAddress;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class PortTelnetHandler_telnet_0_0_Test {

    private PortTelnetHandler handler = new PortTelnetHandler();
    private Map<String, ExchangeServer> serverMap;
    private Map<String, ExchangeServer> backup;

    @SuppressWarnings("unchecked")
    @Before
    public void setUp() throws Exception {
        DubboProtocol protocol = DubboProtocol.getDubboProtocol();
        Field f = DubboProtocol.class.getDeclaredField("serverMap");
        f.setAccessible(true);
        serverMap = (Map<String, ExchangeServer>) f.get(protocol);
        backup = new HashMap<>(serverMap);
        serverMap.clear();
    }

    @After
    public void tearDown() {
        serverMap.clear();
        serverMap.putAll(backup);
    }

    private ExchangeServer server(int port, ExchangeChannel... channels) {
        ExchangeServer s = mock(ExchangeServer.class);
        when(s.getUrl()).thenReturn(URL.valueOf("dubbo://127.0.0.1:" + port + "/demo"));
        when(s.getExchangeChannels()).thenReturn(new ArrayList<>(Arrays.asList(channels)));
        return s;
    }

    private ExchangeChannel channel(int remote, int local) {
        ExchangeChannel c = mock(ExchangeChannel.class);
        when(c.getRemoteAddress()).thenReturn(new InetSocketAddress("127.0.0.1", remote));
        when(c.getLocalAddress()).thenReturn(new InetSocketAddress("127.0.0.1", local));
        return c;
    }

    @Test
    public void testIllegalPort() {
        assertEquals("Illegal port a, must be integer.", handler.telnet(null, "a"));
        assertEquals("Illegal port x, must be integer.", handler.telnet(null, "-l x"));
    }

    @Test
    public void testEmptyNoServers() {
        assertEquals("", handler.telnet(null, ""));
        assertEquals("", handler.telnet(null, "-l"));
    }

    @Test
    public void testListPorts() {
        serverMap.put("a", server(30001));
        serverMap.put("b", server(30002));
        String r = handler.telnet(null, "");
        assertTrue(r.contains("30001"));
        assertTrue(r.contains("30002"));
        assertTrue(r.contains("\r\n"));
    }

    @Test
    public void testListPortsDetail() {
        serverMap.put("a", server(30001));
        serverMap.put("b", server(30002));
        String r = handler.telnet(null, "-l");
        assertTrue(r.contains("dubbo://127.0.0.1:30001"));
        assertTrue(r.contains("dubbo://127.0.0.1:30002"));
        assertTrue(r.contains("\r\n"));
    }

    @Test
    public void testNoSuchPort() {
        serverMap.put("a", server(30001));
        assertEquals("No such port 30009", handler.telnet(null, "30009"));
        assertEquals("No such port 30009", handler.telnet(null, "-l 30009"));
    }

    @Test
    public void testPortChannels() {
        serverMap.put("b", server(30002));
        serverMap.put("a", server(30001, channel(40001, 30001), channel(40002, 30001)));
        String r = handler.telnet(null, "30001");
        assertTrue(r.contains("40001"));
        assertTrue(r.contains("40002"));
        assertTrue(r.contains("\r\n"));
        assertTrue(!r.contains("->"));
    }

    @Test
    public void testPortChannelsDetail() {
        serverMap.put("a", server(30001, channel(40001, 30001), channel(40002, 30001)));
        String r = handler.telnet(null, "-l 30001");
        assertTrue(r.contains("40001 -> "));
        assertTrue(r.contains("40002 -> "));
        assertTrue(r.contains("\r\n"));
    }

    @Test
    public void testPortNoChannels() {
        serverMap.put("a", server(30001));
        assertEquals("", handler.telnet(null, "30001"));
    }
}
