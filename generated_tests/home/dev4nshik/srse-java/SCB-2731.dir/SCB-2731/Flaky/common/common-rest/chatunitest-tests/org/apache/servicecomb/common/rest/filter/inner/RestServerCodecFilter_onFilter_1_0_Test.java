package org.apache.servicecomb.common.rest.filter.inner;

import java.lang.reflect.Method;
import java.util.concurrent.CompletableFuture;
import org.apache.servicecomb.core.Invocation;
import org.apache.servicecomb.core.filter.FilterNode;
import org.apache.servicecomb.swagger.invocation.Response;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import static com.google.common.net.HttpHeaders.CONTENT_LENGTH;
import static com.google.common.net.HttpHeaders.TRANSFER_ENCODING;
import static org.apache.servicecomb.core.exception.Exceptions.toProducerResponse;
import java.util.Map;
import java.util.Map.Entry;
import javax.annotation.Nonnull;
import javax.servlet.http.Part;
import org.apache.servicecomb.common.rest.HttpTransportContext;
import org.apache.servicecomb.common.rest.RestConst;
import org.apache.servicecomb.common.rest.codec.RestCodec;
import org.apache.servicecomb.common.rest.codec.produce.ProduceProcessor;
import org.apache.servicecomb.common.rest.definition.RestOperationMeta;
import org.apache.servicecomb.core.definition.OperationMeta;
import org.apache.servicecomb.core.filter.ProducerFilter;
import org.apache.servicecomb.foundation.common.utils.AsyncUtils;
import org.apache.servicecomb.foundation.vertx.http.HttpServletRequestEx;
import org.apache.servicecomb.foundation.vertx.http.HttpServletResponseEx;
import org.apache.servicecomb.foundation.vertx.stream.BufferOutputStream;
import org.springframework.stereotype.Component;
import io.netty.buffer.Unpooled;
import io.vertx.core.MultiMap;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

public class RestServerCodecFilter_onFilter_1_0_Test {

    private RestServerCodecFilter filter;

    @Mock
    private Invocation invocation;

    @Mock
    private FilterNode nextNode;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        filter = new RestServerCodecFilter();
    }

    @Test
    public void testInvokeNext() throws Exception {
        // Arrange
        Method method = RestServerCodecFilter.class.getDeclaredMethod("invokeNext", Invocation.class, FilterNode.class);
        method.setAccessible(true);
        Response response = Response.ok(new Object());
        when(nextNode.onFilter(invocation)).thenReturn(CompletableFuture.completedFuture(response));
        // Act
        CompletableFuture<Response> result = (CompletableFuture<Response>) method.invoke(filter, invocation, nextNode);
        // Assert
        assertNotNull(result);
        assertEquals(response, result.join());
    }
}
