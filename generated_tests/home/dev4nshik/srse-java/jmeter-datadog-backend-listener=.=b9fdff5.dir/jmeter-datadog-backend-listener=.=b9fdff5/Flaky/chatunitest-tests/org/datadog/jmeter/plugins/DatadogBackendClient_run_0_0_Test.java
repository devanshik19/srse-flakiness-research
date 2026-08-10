package org.datadog.jmeter.plugins;

import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import org.datadog.jmeter.plugins.DatadogBackendClient;
import org.datadog.jmeter.plugins.aggregation.ConcurrentAggregator;
import org.datadog.jmeter.plugins.metrics.DatadogMetric;
import java.util.Arrays;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.jmeter.config.Arguments;
import org.apache.jmeter.protocol.http.sampler.HTTPSampleResult;
import org.apache.jmeter.samplers.SampleResult;
import org.apache.jmeter.util.JMeterUtils;
import org.apache.jmeter.visualizers.backend.AbstractBackendListenerClient;
import org.apache.jmeter.visualizers.backend.BackendListenerContext;
import org.apache.jmeter.visualizers.backend.UserMetric;
import org.datadog.jmeter.plugins.exceptions.DatadogApiException;
import org.datadog.jmeter.plugins.exceptions.DatadogConfigurationException;
import org.datadog.jmeter.plugins.util.CommonUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import net.minidev.json.JSONObject;

@ExtendWith(MockitoExtension.class)
public class DatadogBackendClient_run_0_0_Test {

    @InjectMocks
    private DatadogBackendClient datadogBackendClient;

    @Mock
    private DatadogHttpClient datadogClient;

    @Mock
    private DatadogConfiguration configuration;

    @Mock
    private ConcurrentAggregator aggregator;

    @BeforeEach
    public void setUp() throws Exception {
        datadogBackendClient = new DatadogBackendClient();
        Field datadogClientField = DatadogBackendClient.class.getDeclaredField("datadogClient");
        datadogClientField.setAccessible(true);
        datadogClientField.set(datadogBackendClient, datadogClient);
        Field configurationField = DatadogBackendClient.class.getDeclaredField("configuration");
        configurationField.setAccessible(true);
        configurationField.set(datadogBackendClient, configuration);
        Field aggregatorField = DatadogBackendClient.class.getDeclaredField("aggregator");
        aggregatorField.setAccessible(true);
        aggregatorField.set(datadogBackendClient, aggregator);
    }

    @Test
    public void testRun() throws Exception {
        // Arrange
        List<DatadogMetric> mockMetrics = new ArrayList<>();
        mockMetrics.add(new DatadogMetric("metricName", "host", 1.0, new String[] { "tag1", "tag2" }));
        when(aggregator.flushMetrics()).thenReturn(mockMetrics);
        when(configuration.getMetricsMaxBatchSize()).thenReturn(10);
        // Act
        Method sendMetricsMethod = DatadogBackendClient.class.getDeclaredMethod("sendMetrics");
        sendMetricsMethod.setAccessible(true);
        sendMetricsMethod.invoke(datadogBackendClient);
        // Assert
        verify(aggregator, times(1)).flushMetrics();
        verify(datadogClient, times(1)).submitMetrics(anyList());
    }
}
