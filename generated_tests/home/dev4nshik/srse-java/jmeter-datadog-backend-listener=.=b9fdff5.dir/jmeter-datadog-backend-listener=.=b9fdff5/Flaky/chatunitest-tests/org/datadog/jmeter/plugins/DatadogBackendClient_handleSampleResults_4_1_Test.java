package org.datadog.jmeter.plugins;

import org.datadog.jmeter.plugins.DatadogBackendClient;
import org.datadog.jmeter.plugins.DatadogConfiguration;
import org.apache.jmeter.samplers.SampleResult;
import org.apache.jmeter.visualizers.backend.BackendListenerContext;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.ArrayList;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.regex.Matcher;
import java.util.stream.Collectors;
import net.minidev.json.JSONObject;
import org.apache.jmeter.config.Arguments;
import org.apache.jmeter.protocol.http.sampler.HTTPSampleResult;
import org.apache.jmeter.util.JMeterUtils;
import org.apache.jmeter.visualizers.backend.AbstractBackendListenerClient;
import org.apache.jmeter.visualizers.backend.UserMetric;
import org.datadog.jmeter.plugins.aggregation.ConcurrentAggregator;
import org.datadog.jmeter.plugins.exceptions.DatadogApiException;
import org.datadog.jmeter.plugins.exceptions.DatadogConfigurationException;
import org.datadog.jmeter.plugins.metrics.DatadogMetric;
import org.datadog.jmeter.plugins.util.CommonUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@ExtendWith(MockitoExtension.class)
class DatadogBackendClient_handleSampleResults_4_1_Test {

    private DatadogBackendClient datadogBackendClient;

    private DatadogConfiguration mockConfiguration;

    private BackendListenerContext mockBackendListenerContext;

    @BeforeEach
    void setUp() throws Exception {
        datadogBackendClient = new DatadogBackendClient();
        mockConfiguration = mock(DatadogConfiguration.class);
        mockBackendListenerContext = mock(BackendListenerContext.class);
        // Use reflection to set the private field 'configuration'
        Field configurationField = DatadogBackendClient.class.getDeclaredField("configuration");
        configurationField.setAccessible(true);
        configurationField.set(datadogBackendClient, mockConfiguration);
    }

    @Test
    void testHandleSampleResults_noMatchRegex() {
        // Setup
        SampleResult sampleResult = mock(SampleResult.class);
        when(sampleResult.getSampleLabel()).thenReturn("nonMatchingLabel");
        List<SampleResult> sampleResults = Arrays.asList(sampleResult);
        when(mockConfiguration.getSamplersRegex()).thenReturn(Pattern.compile("matching.*"));
        // Execute
        datadogBackendClient.handleSampleResults(sampleResults, mockBackendListenerContext);
        // Verify
        verify(sampleResult, never()).getSubResults();
    }
}
