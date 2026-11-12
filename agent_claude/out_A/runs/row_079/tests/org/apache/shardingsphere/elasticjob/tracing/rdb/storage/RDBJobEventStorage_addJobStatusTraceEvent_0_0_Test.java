package org.apache.shardingsphere.elasticjob.tracing.rdb.storage;

import org.apache.commons.dbcp2.BasicDataSource;
import org.apache.shardingsphere.elasticjob.tracing.event.JobStatusTraceEvent;
import org.apache.shardingsphere.elasticjob.tracing.event.JobStatusTraceEvent.Source;
import org.apache.shardingsphere.elasticjob.tracing.event.JobStatusTraceEvent.State;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import javax.sql.DataSource;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.sql.SQLException;
import java.util.List;
import java.util.UUID;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class RDBJobEventStorage_addJobStatusTraceEvent_0_0_Test {

    private BasicDataSource dataSource;

    private RDBJobEventStorage storage;

    @Before
    public void setUp() throws SQLException {
        dataSource = new BasicDataSource();
        dataSource.setDriverClassName(org.h2.Driver.class.getName());
        dataSource.setUrl("jdbc:h2:mem:status_" + UUID.randomUUID().toString().replace("-", ""));
        dataSource.setUsername("sa");
        dataSource.setPassword("");
        storage = new RDBJobEventStorage(dataSource);
    }

    @After
    public void tearDown() throws SQLException {
        dataSource.close();
    }

    @Test
    public void testStagingStateKeepsOriginalTaskId() {
        JobStatusTraceEvent event = new JobStatusTraceEvent("job", "t1", "slave", Source.LITE_EXECUTOR, "FAILOVER", "0", State.TASK_STAGING, "msg");
        event.setOriginalTaskId("orig1");
        assertTrue(storage.addJobStatusTraceEvent(event));
        List<JobStatusTraceEvent> events = storage.getJobStatusTraceEvents("t1");
        assertEquals(1, events.size());
        assertEquals("orig1", events.get(0).getOriginalTaskId());
    }

    @Test
    public void testNonStagingLooksUpOriginalTaskId() {
        JobStatusTraceEvent staging = new JobStatusTraceEvent("job", "t2", "slave", Source.LITE_EXECUTOR, "FAILOVER", "0", State.TASK_STAGING, "msg");
        staging.setOriginalTaskId("orig2");
        assertTrue(storage.addJobStatusTraceEvent(staging));
        JobStatusTraceEvent failed = new JobStatusTraceEvent("job", "t2", "slave", Source.LITE_EXECUTOR, "FAILOVER", "0", State.TASK_FAILED, "msg");
        failed.setOriginalTaskId("ignored");
        assertTrue(storage.addJobStatusTraceEvent(failed));
        List<JobStatusTraceEvent> events = storage.getJobStatusTraceEvents("t2");
        assertEquals(2, events.size());
        for (JobStatusTraceEvent each : events) {
            assertEquals("orig2", each.getOriginalTaskId());
        }
    }

    @Test
    public void testNonStagingWithoutPriorRecord() {
        JobStatusTraceEvent event = new JobStatusTraceEvent("job", "t3", "slave", Source.CLOUD_SCHEDULER, "READY", "0", State.TASK_RUNNING, null);
        assertTrue(storage.addJobStatusTraceEvent(event));
        List<JobStatusTraceEvent> events = storage.getJobStatusTraceEvents("t3");
        assertEquals(1, events.size());
        assertEquals("", events.get(0).getOriginalTaskId());
    }

    @Test
    public void testLongMessageTruncated() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 4100; i++) {
            sb.append('a');
        }
        JobStatusTraceEvent event = new JobStatusTraceEvent("job", "t4", "slave", Source.CLOUD_EXECUTOR, "READY", "0", State.TASK_STAGING, sb.toString());
        assertTrue(storage.addJobStatusTraceEvent(event));
        List<JobStatusTraceEvent> events = storage.getJobStatusTraceEvents("t4");
        assertEquals(1, events.size());
        assertEquals(4000, events.get(0).getMessage().length());
    }

    @Test
    public void testEmptyMessage() {
        JobStatusTraceEvent event = new JobStatusTraceEvent("job", "t5", "slave", Source.LITE_EXECUTOR, "READY", "0", State.TASK_STAGING, "");
        assertTrue(storage.addJobStatusTraceEvent(event));
    }

    @Test
    public void testSQLExceptionReturnsFalse() throws Exception {
        DataSource broken = mock(DataSource.class);
        when(broken.getConnection()).thenThrow(new SQLException("boom"));
        Field field = RDBJobEventStorage.class.getDeclaredField("dataSource");
        field.setAccessible(true);
        field.set(storage, broken);
        JobStatusTraceEvent running = new JobStatusTraceEvent("job", "t6", "slave", Source.LITE_EXECUTOR, "READY", "0", State.TASK_RUNNING, "msg");
        assertFalse(storage.addJobStatusTraceEvent(running));
        JobStatusTraceEvent staging = new JobStatusTraceEvent("job", "t6", "slave", Source.LITE_EXECUTOR, "READY", "0", State.TASK_STAGING, "msg");
        assertFalse(storage.addJobStatusTraceEvent(staging));
    }

    @Test
    public void testPrivateHelpersViaReflection() throws Exception {
        Method truncate = RDBJobEventStorage.class.getDeclaredMethod("truncateString", String.class);
        truncate.setAccessible(true);
        assertEquals(null, truncate.invoke(storage, (Object) null));
        assertEquals("abc", truncate.invoke(storage, "abc"));
        Method getOriginal = RDBJobEventStorage.class.getDeclaredMethod("getOriginalTaskId", String.class);
        getOriginal.setAccessible(true);
        assertEquals("", getOriginal.invoke(storage, "none"));
    }
}
