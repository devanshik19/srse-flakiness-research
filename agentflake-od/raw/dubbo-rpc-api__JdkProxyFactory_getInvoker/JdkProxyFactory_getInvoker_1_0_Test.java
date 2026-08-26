package org.apache.dubbo.rpc.proxy.jdk;

import org.apache.dubbo.common.URL;
import org.apache.dubbo.rpc.Invoker;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.apache.dubbo.rpc.proxy.AbstractProxyFactory;
import org.apache.dubbo.rpc.proxy.AbstractProxyInvoker;
import org.apache.dubbo.rpc.proxy.InvokerInvocationHandler;
import java.lang.reflect.Proxy;

class JdkProxyFactory_getInvoker_1_0_Test {

    private JdkProxyFactory jdkProxyFactory;

    @BeforeEach
    void setUp() {
        jdkProxyFactory = new JdkProxyFactory();
    }

    @Test
    void testGetInvoker() throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        // Create a proxy object
        TestClass proxy = new TestClass();
        Class<TestClass> type = TestClass.class;
        URL url = URL.valueOf("dubbo://localhost:12345");
        // Get the invoker
        Invoker<TestClass> invoker = jdkProxyFactory.getInvoker(proxy, type, url);
        // Verify that the invoker is not null
        assertNotNull(invoker);
        // Invoke a method through the invoker
        Method method = invoker.getClass().getSuperclass().getDeclaredMethod("doInvoke", Object.class, String.class, Class[].class, Object[].class);
        method.setAccessible(true);
        Object result = method.invoke(invoker, proxy, "sayHello", new Class[] { String.class }, new Object[] { "World" });
        // Verify the result
        assertEquals("Hello, World", result);
    }

    // Test class to be proxied
    public static class TestClass {

        public String sayHello(String name) {
            return "Hello, " + name;
        }
    }
}
