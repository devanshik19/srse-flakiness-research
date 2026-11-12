package io.elasticjob.lite.internal.failover;

import io.elasticjob.lite.api.strategy.JobInstance;
import io.elasticjob.lite.internal.schedule.JobRegistry;
import io.elasticjob.lite.internal.schedule.JobScheduleController;
import io.elasticjob.lite.internal.sharding.ShardingService;
import io.elasticjob.lite.internal.storage.JobNodeStorage;
import io.elasticjob.lite.reg.base.CoordinatorRegistryCenter;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.lang.reflect.Field;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

public final class FailoverService_getLocalFailoverItems_0_0_Test {
    
    private static final String JOB_NAME = "failover_local_items_test_job";
    
    @Mock
    private CoordinatorRegistryCenter regCenter;
    
    @Mock
    private JobScheduleController jobScheduleController;
    
    @Mock
    private JobNodeStorage jobNodeStorage;
    
    @Mock
    private ShardingService shardingService;
    
    private FailoverService failoverService;
    
    @Before
    public void setUp() throws Exception {
        MockitoAnnotations.initMocks(this);
        failoverService = new FailoverService(regCenter, JOB_NAME);
        setField("jobNodeStorage", jobNodeStorage);
        setField("shardingService", shardingService);
        JobRegistry.getInstance().shutdown(JOB_NAME);
    }
    
    @After
    public void tearDown() {
        JobRegistry.getInstance().shutdown(JOB_NAME);
    }
    
    private void setField(final String name, final Object value) throws Exception {
        Field field = FailoverService.class.getDeclaredField(name);
        field.setAccessible(true);
        field.set(failoverService, value);
    }
    
    @Test
    public void assertEmptyWhenNotRegistered() {
        List<Integer> result = failoverService.getLocalFailoverItems();
        assertTrue(result.isEmpty());
        verify(jobNodeStorage, never()).getJobNodeChildrenKeys("sharding");
    }
    
    @Test
    public void assertEmptyWhenOnlySchedulerRegistered() {
        JobRegistry.getInstance().registerJob(JOB_NAME, jobScheduleController, regCenter);
        assertTrue(failoverService.getLocalFailoverItems().isEmpty());
        verify(jobNodeStorage, never()).getJobNodeChildrenKeys("sharding");
    }
    
    @Test
    public void assertEmptyWhenOnlyInstanceRegistered() {
        JobRegistry.getInstance().addJobInstance(JOB_NAME, new JobInstance("127.0.0.1@-@0"));
        assertTrue(failoverService.getLocalFailoverItems().isEmpty());
    }
    
    @Test
    public void assertGetLocalFailoverItems() {
        JobRegistry.getInstance().registerJob(JOB_NAME, jobScheduleController, regCenter);
        JobRegistry.getInstance().addJobInstance(JOB_NAME, new JobInstance("127.0.0.1@-@0"));
        when(jobNodeStorage.getJobNodeChildrenKeys("sharding")).thenReturn(Arrays.asList("2", "0", "1", "3"));
        when(jobNodeStorage.isJobNodeExisted("sharding/0/failover")).thenReturn(true);
        when(jobNodeStorage.isJobNodeExisted("sharding/1/failover")).thenReturn(true);
        when(jobNodeStorage.isJobNodeExisted("sharding/2/failover")).thenReturn(true);
        when(jobNodeStorage.isJobNodeExisted("sharding/3/failover")).thenReturn(false);
        when(jobNodeStorage.getJobNodeDataDirectly("sharding/0/failover")).thenReturn("127.0.0.1@-@0");
        when(jobNodeStorage.getJobNodeDataDirectly("sharding/1/failover")).thenReturn("127.0.0.1@-@1");
        when(jobNodeStorage.getJobNodeDataDirectly("sharding/2/failover")).thenReturn("127.0.0.1@-@0");
        assertEquals(Arrays.asList(0, 2), failoverService.getLocalFailoverItems());
    }
    
    @Test
    public void assertGetLocalFailoverItemsWhenNoChildren() {
        JobRegistry.getInstance().registerJob(JOB_NAME, jobScheduleController, regCenter);
        JobRegistry.getInstance().addJobInstance(JOB_NAME, new JobInstance("127.0.0.1@-@0"));
        when(jobNodeStorage.getJobNodeChildrenKeys("sharding")).thenReturn(Collections.<String>emptyList());
        assertTrue(failoverService.getLocalFailoverItems().isEmpty());
    }
}
