package org.apache.camel.component.reactor.engine;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import org.apache.camel.Exchange;
import org.apache.camel.ProducerTemplate;
import org.apache.camel.builder.RouteBuilder;
import org.junit.Assert;
import org.junit.Test;
import org.reactivestreams.Publisher;
import reactor.core.publisher.Flux;

public class ReactorStreamsService_fromStream_0_0_Test extends ReactorStreamsServiceTestSupport {

    @Test
    public void testExchangeTypeReturnsSamePublisher() throws Exception {
        context.start();
        Publisher<Exchange> raw = crs.fromStream("ex");
        Publisher<Exchange> typed = crs.fromStream("ex", Exchange.class);
        Assert.assertSame(raw, typed);
    }

    @Test
    public void testExchangeTypeReceivesExchanges() throws Exception {
        context.addRoutes(new RouteBuilder() {
            public void configure() {
                from("direct:ex").to("reactive-streams:ex2");
            }
        });
        context.start();
        CountDownLatch latch = new CountDownLatch(2);
        List<Object> bodies = new CopyOnWriteArrayList<>();
        Flux.from(crs.fromStream("ex2", Exchange.class))
            .doOnNext(e -> bodies.add(e.getIn().getBody()))
            .doOnNext(e -> latch.countDown())
            .subscribe();
        ProducerTemplate template = context.createProducerTemplate();
        template.sendBody("direct:ex", "a");
        template.sendBody("direct:ex", "b");
        Assert.assertTrue(latch.await(5, TimeUnit.SECONDS));
        Assert.assertEquals(2, bodies.size());
        Assert.assertEquals("a", bodies.get(0));
    }

    @Test
    public void testConvertedType() throws Exception {
        context.addRoutes(new RouteBuilder() {
            public void configure() {
                from("direct:num").to("reactive-streams:nums");
            }
        });
        context.start();
        Publisher<Integer> pub = crs.fromStream("nums", Integer.class);
        Assert.assertNotNull(pub);
        Assert.assertNotSame(crs.fromStream("nums"), pub);
        CountDownLatch latch = new CountDownLatch(2);
        List<Integer> values = new CopyOnWriteArrayList<>();
        Flux.from(pub).doOnNext(values::add).doOnNext(v -> latch.countDown()).subscribe();
        ProducerTemplate template = context.createProducerTemplate();
        template.sendBody("direct:num", "1");
        template.sendBody("direct:num", 2);
        Assert.assertTrue(latch.await(5, TimeUnit.SECONDS));
        Assert.assertEquals(Integer.valueOf(1), values.get(0));
        Assert.assertEquals(Integer.valueOf(2), values.get(1));
    }

    @Test
    public void testDirectInstantiation() throws Exception {
        ReactorStreamsService service = new ReactorStreamsService(context);
        Publisher<String> p = service.fromStream("s", String.class);
        Assert.assertNotNull(p);
        Assert.assertTrue(p instanceof Flux);
        Publisher<Exchange> e = service.fromStream("s", Exchange.class);
        Assert.assertSame(service.fromStream("s"), e);
    }
}
