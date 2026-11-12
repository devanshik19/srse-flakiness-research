package org.apache.camel.component.reactor.engine;

import java.util.Map;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import org.apache.camel.CamelContext;
import org.apache.camel.Exchange;
import org.apache.camel.ProducerTemplate;
import org.apache.camel.RoutesBuilder;
import org.apache.camel.spi.UuidGenerator;
import org.junit.Assert;
import org.junit.Test;
import org.mockito.Mockito;
import org.reactivestreams.Publisher;
import reactor.core.publisher.Flux;

public class ReactorStreamsService_from_0_0_Test extends ReactorStreamsServiceTestSupport {

    @Test
    public void testFromDirect() throws Exception {
        context.start();
        Publisher<Exchange> pub = crs.from("direct:in");
        Assert.assertNotNull(pub);

        CountDownLatch latch = new CountDownLatch(3);
        AtomicInteger value = new AtomicInteger(0);
        Flux.from(pub)
            .map(e -> e.getIn().getBody(Integer.class))
            .doOnNext(n -> Assert.assertEquals(value.incrementAndGet(), n.intValue()))
            .doOnNext(n -> latch.countDown())
            .subscribe();

        ProducerTemplate template = context.createProducerTemplate();
        template.sendBody("direct:in", 1);
        template.sendBody("direct:in", 2);
        template.sendBody("direct:in", 3);

        Assert.assertTrue(latch.await(5, TimeUnit.SECONDS));
        Assert.assertEquals(1, context.getRoutes().size());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testFromSameUriReused() throws Exception {
        context.start();
        ReactorStreamsService service = new ReactorStreamsService(context);
        Publisher<Exchange> p1 = service.from("direct:a");
        Publisher<Exchange> p2 = service.from("direct:a");
        Assert.assertNotNull(p1);
        Assert.assertNotNull(p2);
        Assert.assertEquals(1, context.getRoutes().size());

        java.lang.reflect.Field f = ReactorStreamsService.class.getDeclaredField("publishedUriToStream");
        f.setAccessible(true);
        Map<String, String> map = (Map<String, String>) f.get(service);
        Assert.assertEquals(1, map.size());
        Assert.assertTrue(map.containsKey("direct:a"));

        service.from("direct:b");
        Assert.assertEquals(2, map.size());
        Assert.assertEquals(2, context.getRoutes().size());
    }

    @Test
    public void testFromAddRoutesFails() throws Exception {
        CamelContext ctx = Mockito.mock(CamelContext.class);
        UuidGenerator gen = Mockito.mock(UuidGenerator.class);
        Mockito.when(ctx.getUuidGenerator()).thenReturn(gen);
        Mockito.when(gen.generateUuid()).thenReturn("uuid-1");
        Mockito.doThrow(new RuntimeException("boom")).when(ctx).addRoutes(Mockito.any(RoutesBuilder.class));

        ReactorStreamsService service = new ReactorStreamsService(ctx);
        try {
            service.from("direct:x");
            Assert.fail("expected exception");
        } catch (IllegalStateException e) {
            Assert.assertTrue(e.getMessage().contains("direct:x"));
            Assert.assertEquals("boom", e.getCause().getMessage());
        }
    }

    @Test
    public void testFromUuidGeneratorFails() throws Exception {
        CamelContext ctx = Mockito.mock(CamelContext.class);
        Mockito.when(ctx.getUuidGenerator()).thenThrow(new RuntimeException("nogen"));

        ReactorStreamsService service = new ReactorStreamsService(ctx);
        try {
            service.from("direct:y");
            Assert.fail("expected exception");
        } catch (IllegalStateException e) {
            Assert.assertEquals("nogen", e.getCause().getMessage());
        }
    }
}
