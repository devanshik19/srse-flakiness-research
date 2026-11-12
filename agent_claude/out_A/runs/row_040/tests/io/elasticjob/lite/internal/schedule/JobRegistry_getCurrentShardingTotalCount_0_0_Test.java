package io.elasticjob.lite.internal.schedule;

import org.junit.After;
import org.junit.Test;

import java.lang.reflect.Field;
import java.util.Map;

import static org.junit.Assert.assertEquals;

public class JobRegistry_getCurrentShardingTotalCount_0_0_Test {

    private static final String JOB = "JobRegistry_getCurrentShardingTotalCount_test_job";

    @After
    @SuppressWarnings("unchecked")
    public void tearDown() throws Exception {
        Field f = JobRegistry.class.getDeclaredField("currentShardingTotalCountMap");
        f.setAccessible(true);
        ((Map<String, Integer>) f.get(JobRegistry.getInstance())).remove(JOB);
    }

    @Test
    public void assertReturnsZeroWhenAbsent() {
        assertEquals(0, JobRegistry.getInstance().getCurrentShardingTotalCount(JOB));
    }

    @Test
    public void assertReturnsValueWhenPresent() {
        JobRegistry.getInstance().setCurrentShardingTotalCount(JOB, 10);
        assertEquals(10, JobRegistry.getInstance().getCurrentShardingTotalCount(JOB));
    }

    @Test
    public void assertReturnsZeroValueWhenSetZero() {
        JobRegistry.getInstance().setCurrentShardingTotalCount(JOB, 0);
        assertEquals(0, JobRegistry.getInstance().getCurrentShardingTotalCount(JOB));
    }

    @Test
    public void assertOverwrite() {
        JobRegistry.getInstance().setCurrentShardingTotalCount(JOB, 3);
        JobRegistry.getInstance().setCurrentShardingTotalCount(JOB, 5);
        assertEquals(5, JobRegistry.getInstance().getCurrentShardingTotalCount(JOB));
        assertEquals(0, JobRegistry.getInstance().getCurrentShardingTotalCount(JOB + "_other"));
    }
}
