package org.apache.hadoop.metrics2.impl;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

import java.lang.reflect.Field;
import java.util.Map;

import org.apache.hadoop.metrics2.MetricsRecord;
import org.apache.hadoop.metrics2.MetricsSink;
import org.apache.hadoop.metrics2.annotation.Metric;
import org.apache.hadoop.metrics2.annotation.Metrics;
import org.apache.hadoop.metrics2.lib.DefaultMetricsSystem;
import org.apache.hadoop.metrics2.lib.MutableCounterLong;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class MetricsSystemImpl_publishMetricsNow_0_0_Test {

  @Metrics(context = "test")
  public static class Src {
    @Metric("C1 desc") MutableCounterLong c1;
  }

  private MetricsSystemImpl ms;

  @Before
  public void setUp() {
    DefaultMetricsSystem.shutdown();
    new ConfigBuilder().add("*.period", 8)
        .save(TestMetricsConfig.getTestFilename("hadoop-metrics2-test"));
    ms = new MetricsSystemImpl("Test");
    ms.start();
  }

  @After
  public void tearDown() {
    if (ms != null) {
      try { ms.stop(); } catch (Exception e) { }
      ms.shutdown();
    }
  }

  @SuppressWarnings("unchecked")
  private int sinkCount() throws Exception {
    Field f = MetricsSystemImpl.class.getDeclaredField("sinks");
    f.setAccessible(true);
    return ((Map<String, ?>) f.get(ms)).size();
  }

  @Test
  public void testNoSinks() throws Exception {
    assertEquals(0, sinkCount());
    long before = ms.publishStat.lastStat().numSamples();
    ms.publishMetricsNow();
    assertEquals(before, ms.publishStat.lastStat().numSamples());
    assertEquals(0L, ms.droppedPubAll.value());
  }

  @Test(timeout = 30000)
  public void testWithSinks() throws Exception {
    Src s = ms.register("s1", "s1 desc", new Src());
    s.c1.incr();
    MetricsSink sink1 = mock(MetricsSink.class);
    MetricsSink sink2 = mock(MetricsSink.class);
    ms.registerSink("sink1", "sink1 desc", sink1);
    ms.registerSink("sink2", "sink2 desc", sink2);
    assertEquals(2, sinkCount());
    ms.publishMetricsNow();
    verify(sink1, atLeastOnce()).putMetrics(any(MetricsRecord.class));
    verify(sink2, atLeastOnce()).putMetrics(any(MetricsRecord.class));
    verify(sink1, atLeastOnce()).flush();
    assertEquals(0L, ms.droppedPubAll.value());
  }
}
