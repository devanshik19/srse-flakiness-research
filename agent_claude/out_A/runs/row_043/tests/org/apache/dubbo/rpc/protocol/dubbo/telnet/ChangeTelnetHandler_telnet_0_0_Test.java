package org.apache.dubbo.rpc.protocol.dubbo.telnet;

import org.apache.dubbo.common.URL;
import org.apache.dubbo.remoting.Channel;
import org.apache.dubbo.rpc.Invoker;
import org.apache.dubbo.rpc.protocol.dubbo.DubboProtocol;
import org.apache.dubbo.rpc.protocol.dubbo.support.DemoService;
import org.apache.dubbo.rpc.protocol.dubbo.support.ProtocolUtils;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

public class ChangeTelnetHandler_telnet_0_0_Test {

    private ChangeTelnetHandler change;
    private Channel channel;
    private Invoker<DemoService> invoker;

    @SuppressWarnings("unchecked")
    @Before
    public void setUp() {
        change = new ChangeTelnetHandler();
        channel = mock(Channel.class);
        invoker = mock(Invoker.class);
        when(invoker.getInterface()).thenReturn(DemoService.class);
        when(invoker.getUrl()).thenReturn(URL.valueOf("dubbo://127.0.0.1:20891/demoPath"));
    }

    @After
    public void tearDown() {
        ProtocolUtils.closeAll();
    }

    @Test
    public void testNullMessage() {
        assertEquals("Please input service name, eg: \r\ncd XxxService\r\ncd com.xxx.XxxService",
                change.telnet(channel, null));
    }

    @Test
    public void testEmptyMessage() {
        assertEquals("Please input service name, eg: \r\ncd XxxService\r\ncd com.xxx.XxxService",
                change.telnet(channel, ""));
    }

    @Test
    public void testCancelSlash() {
        when(channel.getAttribute(ChangeTelnetHandler.SERVICE_KEY)).thenReturn("DemoService");
        assertEquals("Cancelled default service DemoService.", change.telnet(channel, "/"));
        verify(channel).removeAttribute(ChangeTelnetHandler.SERVICE_KEY);
    }

    @Test
    public void testCancelDotDot() {
        assertEquals("Cancelled default service null.", change.telnet(channel, ".."));
        verify(channel).removeAttribute(ChangeTelnetHandler.SERVICE_KEY);
    }

    @Test
    public void testNotFoundNoExporters() {
        assertEquals("No such service xyz", change.telnet(channel, "xyz"));
        verify(channel, never()).setAttribute(ChangeTelnetHandler.SERVICE_KEY, "xyz");
    }

    @Test
    public void testSimpleName() {
        DubboProtocol.getDubboProtocol().export(invoker);
        assertEquals("Used the DemoService as default.\r\nYou can cancel default service by command: cd /",
                change.telnet(channel, "DemoService"));
        verify(channel).setAttribute(ChangeTelnetHandler.SERVICE_KEY, "DemoService");
    }

    @Test
    public void testFullName() {
        DubboProtocol.getDubboProtocol().export(invoker);
        String name = DemoService.class.getName();
        assertEquals("Used the " + name + " as default.\r\nYou can cancel default service by command: cd /",
                change.telnet(channel, name));
    }

    @Test
    public void testPath() {
        DubboProtocol.getDubboProtocol().export(invoker);
        assertEquals("Used the demoPath as default.\r\nYou can cancel default service by command: cd /",
                change.telnet(channel, "demoPath"));
    }

    @Test
    public void testNotFoundWithExporter() {
        DubboProtocol.getDubboProtocol().export(invoker);
        assertEquals("No such service other", change.telnet(channel, "other"));
    }
}
