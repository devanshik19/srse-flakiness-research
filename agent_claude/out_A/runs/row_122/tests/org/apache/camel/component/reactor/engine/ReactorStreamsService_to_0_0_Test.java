package org.apache.camel.component.reactor.engine;

import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.function.Function;

import org.apache.camel.Exchange;
import org.apache.camel.impl.JndiRegistry;
import org.junit.Assert;
import org.junit.Test;
import org.reactivestreams.Publisher;
import reactor.core.publisher.Flux;

public class ReactorStreamsService_to_0_0_Test extends ReactorStreamsServiceTestSupport {

    @Override
    protected JndiRegistry createRegistry() throws Exception {
        JndiRegistry registry = super.createRegistry();
        registry.bind("hello", new SampleBean());
        return registry;
    }

    public static class SampleBean {
        public String hello(String name) {
            return "Hello " + name;
        }
    }

    @Test
    public void testToFunctionReturnsWorkingPublisher() throws Exception {
        context.start();
        Function<Object, Publisher<Exchange>> fun = crs.to("bean:hello");
        Assert.assertNotNull(fun);

        List<String> res = Flux.just(1, 2, 3)
            .concatMap(fun)
            .map(e -> e.hasOut() ? e.getOut().getBody(String.class) : e.getIn().getBody(String.class))
            .collectList()
            .block(java.time.Duration.ofSeconds(5));

        Assert.assertEquals(3, res.size());
        Assert.assertEquals("Hello 1", res.get(0));
        Assert.assertEquals("Hello 2", res.get(1));
        Assert.assertEquals("Hello 3", res.get(2));
    }

    @Test
    public void testToFunctionReusesStream() throws Exception {
        context.start();
        int routes = context.getRoutes().size();
        Function<Object, Publisher<Exchange>> fun = crs.to("bean:hello");
        Exchange ex1 = Flux.from(fun.apply("a")).blockFirst(java.time.Duration.ofSeconds(5));
        Exchange ex2 = Flux.from(fun.apply("b")).blockFirst(java.time.Duration.ofSeconds(5));
        Assert.assertNotNull(ex1);
        Assert.assertNotNull(ex2);
        Assert.assertEquals(routes + 1, context.getRoutes().size());
    }

    @Test
    public void testToFunctionLazy() throws Exception {
        context.start();
        int routes = context.getRoutes().size();
        Function<Object, Publisher<Exchange>> fun = crs.to("bean:hello");
        Assert.assertEquals(routes, context.getRoutes().size());
    }

    @Test
    public void testToFunctionInvalidUri() throws Exception {
        context.start();
        Function<Object, Publisher<Exchange>> fun = crs.to("nonexistingcomponent:foo");
        try {
            fun.apply("x");
            Assert.fail("Expected IllegalStateException");
        } catch (IllegalStateException e) {
            Assert.assertTrue(e.getMessage().contains("nonexistingcomponent:foo"));
        }
    }

    @Test
    public void testDirectServiceTo() throws Exception {
        context.start();
        ReactorStreamsService service = new ReactorStreamsService(context);
        Function<Object, Publisher<Exchange>> fun = service.to("bean:hello");
        Assert.assertNotNull(fun);
    }
}
