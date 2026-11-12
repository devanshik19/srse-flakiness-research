package org.apache.camel.component.reactor.engine;

import java.util.List;
import java.util.function.Function;

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
    public void testToFunctionNotNullAndLazy() throws Exception {
        context.start();
        ReactorStreamsService service = new ReactorStreamsService(context);
        Function<Object, Publisher<String>> fun = service.to("bean:hello", String.class);
        Assert.assertNotNull(fun);
        // no route created until function applied
        Assert.assertEquals(0, context.getRoutes().size());
    }

    @Test
    public void testToFunctionViaService() throws Exception {
        context.start();
        Function<Object, Publisher<String>> fun = crs.to("bean:hello", String.class);
        String res = Flux.from(fun.apply(1)).blockFirst();
        Assert.assertEquals("Hello 1", res);
    }

    @Test
    public void testToFunctionMultiple() throws Exception {
        context.start();
        Function<Object, Publisher<String>> fun = crs.to("bean:hello", String.class);
        List<String> res = Flux.just(1, 2, 3).concatMap(fun).collectList().block();
        Assert.assertEquals(3, res.size());
        Assert.assertEquals("Hello 1", res.get(0));
        Assert.assertEquals("Hello 2", res.get(1));
        Assert.assertEquals("Hello 3", res.get(2));
        // only one route created for same uri
        Assert.assertEquals(1, context.getRoutes().size());
    }

    @Test
    public void testToFunctionInvalidUri() throws Exception {
        context.start();
        Function<Object, Publisher<String>> fun = crs.to("unknowncomponentxyz:foo", String.class);
        try {
            fun.apply("x");
            Assert.fail("Expected exception");
        } catch (IllegalStateException e) {
            Assert.assertTrue(e.getMessage().contains("unknowncomponentxyz:foo"));
        }
    }
}
