package org.apache.shardingsphere.elasticjob.tracing.rdb.storage;

import org.apache.commons.dbcp2.BasicDataSource;
import org.apache.shardingsphere.elasticjob.tracing.event.JobStatusTraceEvent;
import org.apache.shardingsphere.elasticjob.tracing.event.JobStatusTraceEvent.Source;
import org.apache.shardingsphere.elasticjob.tracing.event.JobStatusTraceEvent.State;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.lang.reflect.Method;
import java.sql.SQLException;
import java.util.List;
import java.util.UUID;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public final class RDBJobEventStorage_addJobStatusTraceEvent_0_0_Test {
    
    private BasicDataSource dataSource;
    
    private RDBJobEventStorage storage;
    
    @Before
    public void setUp() throws SQLException {
        dataSource = new BasicDataSource();
        dataSource.setDriverClassName(org.h2.Driver.class.getName());
        dataSource.setUrl("jdbc:h2:mem:add_status_" + UUID.randomUUID().toString().replace("-", "") + ";DB_CLOSE_DELAY=-1");
        dataSource.setUsername("sa");
        dataSource.setPassword("");
        storage = new RDBJobEventStorage(dataSource);
    }
    
    @After
    public void tearDown() throws SQLException {
        if (!dataSource.isClosed()) {
            dataSource.close();
        }
    }
    
    private JobStatusTraceEvent event(final String taskId, final State state, final String message) {
        return new JobStatusTraceEvent("test_job", taskId, "slave", Source.LITE_EXECUTOR, "READY", "0", state, message);
    }
    
    @Test
    public void testStagingUsesOriginalTaskIdFromEvent() {
        JobStatusTraceEvent e = event("task_a", State.TASK_STAGING, "msg");
        e.setOriginalTaskId("orig_a");
        assertTrue(storage.addJobStatusTraceEvent(e));
        List<JobStatusTraceEvent> result = storage.getJobStatusTraceEvents("task_a");
        assertEquals(1, result.size());
        assertEquals("orig_a", result.get(0).getOriginalTaskId());
    }
    
    @Test
    public void testNonStagingLooksUpOriginalTaskId() {
        JobStatusTraceEvent staging = event("task_b", State.TASK_STAGING, "msg");
        staging.setOriginalTaskId("orig_b");
        assertTrue(storage.addJobStatusTraceEvent(staging));
        JobStatusTraceEvent failed = event("task_b", State.TASK_FAILED, "failed");
        assertTrue(storage.addJobStatusTraceEvent(failed));
        List<JobStatusTraceEvent> result = storage.getJobStatusTraceEvents("task_b");
        assertEquals(2, result.size());
        for (JobStatusTraceEvent each : result) {
            assertEquals("orig_b", each.getOriginalTaskId());
        }
    }
    
    @Test
    public void testNonStagingWithoutPreviousRecord() {
        assertTrue(storage.addJobStatusTraceEvent(event("task_c", State.TASK_RUNNING, "running")));
        List<JobStatusTraceEvent> result = storage.getJobStatusTraceEvents("task_c");
        assertEquals(1, result.size());
        assertEquals("", result.get(0).getOriginalTaskId());
    }
    
    @Test
    public void testLongMessageTruncated() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 5000; i++) {
            sb.append('x');
        }
        JobStatusTraceEvent e = event("task_d", State.TASK_STAGING, sb.toString());
        e.setOriginalTaskId("orig_d");
        assertTrue(storage.addJobStatusTraceEvent(e));
        List<JobStatusTraceEvent> result = storage.getJobStatusTraceEvents("task_d");
        assertEquals(1, result.size());
        assertEquals(4000, result.get(0).getMessage().length());
    }
    
    @Test
    public void testNullMessage() {
        JobStatusTraceEvent e = event("task_e", State.TASK_STAGING, null);
        e.setOriginalTaskId("orig_e");
        assertTrue(storage.addJobStatusTraceEvent(e));
    }
    
    @Test
    public void testTruncateStringViaReflection() throws Exception {
        Method m = RDBJobEventStorage.class.getDeclaredMethod("truncateString", String.class);
        m.setAccessible(true);
        assertEquals("", m.invoke(storage, ""));
        assertEquals("abc", m.invoke(storage, "abc"));
        assertEquals(null, m.invoke(storage, (Object) null));
    }
    
    @Test
    public void testSQLExceptionReturnsFalseForStaging() throws SQLException {
        dataSource.close();
        JobStatusTraceEvent e = event("task_f", State.TASK_STAGING, "msg");
        e.setOriginalTaskId("orig_f");
        assertFalse(storage.addJobStatusTraceEvent(e));
    }
    
    @Test
    public void testSQLExceptionReturnsFalseForNonStaging() throws SQLException {
        dataSource.close();
        assertFalse(storage.addJobStatusTraceEvent(event("task_g", State.TASK_FINISHED, "msg")));
    }
}
