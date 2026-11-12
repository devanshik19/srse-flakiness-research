package org.apache.camel.component.reactor.engine;

import java.time.Duration;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

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
    public void testToSingleValue() throws Exception {
        context.start();
        Publisher<String> p = crs.to("bean:hello", 1, String.class);
        Assert.assertNotNull(p);
        String res = Flux.from(p).blockFirst(Duration.ofSeconds(5));
        Assert.assertEquals("Hello 1", res);
    }

    @Test
    public void testToMultipleValuesSameUri() throws Exception {
        context.start();
        List<String> list = Flux.just(1, 2, 3)
            .flatMap(e -> crs.to("bean:hello", e, String.class))
            .collectList()
            .block(Duration.ofSeconds(5));
        Assert.assertNotNull(list);
        Set<String> set = new HashSet<>(list);
        Assert.assertEquals(3, set.size());
        Assert.assertTrue(set.contains("Hello 1"));
        Assert.assertTrue(set.contains("Hello 2"));
        Assert.assertTrue(set.contains("Hello 3"));
    }

    @Test
    public void testToConvertsType() throws Exception {
        context.start();
        Integer res = Flux.from(crs.to("log:test", "42", Integer.class)).blockFirst(Duration.ofSeconds(5));
        Assert.assertEquals(Integer.valueOf(42), res);
    }

    @Test
    public void testToInvalidUri() throws Exception {
        context.start();
        try {
            crs.to("unknowncomponentxyz:foo", 1, String.class);
            Assert.fail("Expected exception");
        } catch (IllegalStateException e) {
            Assert.assertTrue(e.getMessage().contains("unknowncomponentxyz:foo"));
        }
    }
}
