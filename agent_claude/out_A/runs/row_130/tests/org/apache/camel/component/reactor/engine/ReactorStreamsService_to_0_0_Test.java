package org.apache.camel.component.reactor.engine;

import java.lang.reflect.Field;
import java.util.Map;

import org.apache.camel.Exchange;
import org.apache.camel.RoutesBuilder;
import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.impl.DefaultCamelContext;
import org.junit.Assert;
import org.junit.Test;
import org.reactivestreams.Publisher;
import reactor.core.publisher.Flux;

public class ReactorStreamsService_to_0_0_Test extends ReactorStreamsServiceTestSupport {

    @Test
    public void testToCreatesRouteAndReturnsResult() throws Exception {
        context.addRoutes(new RouteBuilder() {
            @Override
            public void configure() throws Exception {
                from("direct:echo").setBody().simple("echo: ${body}");
            }
        });
        context.start();

        int routesBefore = context.getRoutes().size();
        Publisher<Exchange> pub = crs.to("direct:echo", "hello");
        Assert.assertNotNull(pub);
        Exchange ex = Flux.from(pub).blockFirst();
        Assert.assertEquals("echo: hello", ex.getIn().getBody(String.class));
        int routesAfterFirst = context.getRoutes().size();
        Assert.assertEquals(routesBefore + 1, routesAfterFirst);

        // second call reuses the stream
        Exchange ex2 = Flux.from(crs.to("direct:echo", "world")).blockFirst();
        Assert.assertEquals("echo: world", ex2.getIn().getBody(String.class));
        Assert.assertEquals(routesAfterFirst, context.getRoutes().size());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testToStoresStreamName() throws Exception {
        context.addRoutes(new RouteBuilder() {
            @Override
            public void configure() throws Exception {
                from("direct:x").setBody().constant("X");
            }
        });
        context.start();
        ReactorStreamsService service = (ReactorStreamsService) crs;
        Flux.from(service.to("direct:x", 1)).blockFirst();
        Field f = ReactorStreamsService.class.getDeclaredField("requestedUriToStream");
        f.setAccessible(true);
        Map<String, String> map = (Map<String, String>) f.get(service);
        Assert.assertTrue(map.containsKey("direct:x"));
        Assert.assertNotNull(map.get("direct:x"));
    }

    @Test
    public void testToAddRoutesFailure() throws Exception {
        DefaultCamelContext failing = new DefaultCamelContext() {
            @Override
            public void addRoutes(RoutesBuilder builder) throws Exception {
                throw new RuntimeException("boom");
            }
        };
        ReactorStreamsService service = new ReactorStreamsService(failing);
        try {
            service.to("direct:fail", "data");
            Assert.fail("Expected IllegalStateException");
        } catch (IllegalStateException e) {
            Assert.assertTrue(e.getMessage().contains("direct:fail"));
            Assert.assertEquals("boom", e.getCause().getMessage());
        }
    }
}
