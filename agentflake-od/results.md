# AgentFlake OD — results

**38 rows** — 12 SKIPPED_FOCAL, 10 CANDIDATE_FAILED, 8 NOT_OD, 5 NA_NO_CONFIG, 3 SWEEP_NA

| subject | module | focal_method | generated_test | 100x (pass/orders) | od_verdict | notes |
| --- | --- | --- | --- | --- | --- | --- |
| dubbodubborpcdubborpcapiba89f44 | dubbo-rpc/dubbo-rpc-api | JavassistProxyFactory#getInvoker | JavassistProxyFactory_getInvoker_1_1_Test | 100/100 | NOT_OD | robust but weak assertion (only assertNotNull); coverage/mutation pending |
| dubbodubborpcdubborpcapiba89f441 | dubbo-rpc/dubbo-rpc-api | JdkProxyFactory#getInvoker | JdkProxyFactory_getInvoker_1_0_Test | 100/100 | NOT_OD | jdk proxy focal; robust; coverage/mutation pending |
| ormlitecore59309e5 | . | RuntimeExceptionDao#assignEmptyForeignCollection | com.j256.ormlite.dao.RuntimeExceptionDao_assignEmptyForeignCollection_73_0_Test | 100/100 | NOT_OD | focal jaccard+llm agreed; pristine pom + mockito(junit excl); ordering 3.8.6 custom-surefire; coverage/mutation pending |
| ormlitecore59309e6 | . | RuntimeExceptionDao#callBatchTasks | com.j256.ormlite.dao.RuntimeExceptionDao_callBatchTasks_63_0_Test | 100/100 | NOT_OD | focal jaccard+llm agreed; pristine pom + mockito(junit excl); ordering 3.8.6 custom-surefire; coverage/mutation pending |
| ormlitecore59309e10 | . | RuntimeExceptionDao#countOf | com.j256.ormlite.dao.RuntimeExceptionDao_countOf_71_0_Test | 100/100 | NOT_OD | focal jaccard+llm agreed; pristine pom + mockito(junit excl); ordering 3.8.6 custom-surefire; coverage/mutation pending |
| ormlitecore59309e90 | . | SchemaUtils#dropSchema | GENERATED | 0/0 | CANDIDATE_FAILED | generated candidate(s) did not pass alone |
| ormlitecore59309e88 | . | SchemaUtils#createSchema | GENERATED | 0/0 | CANDIDATE_FAILED | generated candidate(s) did not pass alone |
| ormlitecore59309e59 | . | RuntimeExceptionDao#updateRaw | com.j256.ormlite.dao.RuntimeExceptionDao_updateRaw_60_0_Test | 100/100 | NOT_OD | focal jaccard+llm agreed; pristine pom + mockito(junit excl); ordering 3.8.6 custom-surefire; coverage/mutation pending |
| ormlitecore59309e60 | . | RuntimeExceptionDao#update | com.j256.ormlite.dao.RuntimeExceptionDao_update_21_0_Test | 100/100 | NOT_OD | focal jaccard+llm agreed; pristine pom + mockito(junit excl); ordering 3.8.6 custom-surefire; coverage/mutation pending |
| wildflynaming3a83b7b1 | naming | InitialContextFactoryTestCase#testInitialFactory | FOCAL_UNCONFIRMED | 0/0 | SKIPPED_FOCAL | status=disagreed |
| wildflynaming3a83b7b18 | naming | NamingSubsystemTestCase#testSubsystem | FOCAL_UNCONFIRMED | 0/0 | SKIPPED_FOCAL | status=victim-not-found |
| wildflynaming3a83b7b17 | naming | NamingSubsystemTestCase#testRejectionsEAP7 | FOCAL_UNCONFIRMED | 0/0 | SKIPPED_FOCAL | status=disagreed |
| wildflynaming3a83b7b13 | naming | NamingSubsystemTestCase#testCompositeBindingOps | FOCAL_UNCONFIRMED | 0/0 | SKIPPED_FOCAL | status=disagreed |
| wildflynaming3a83b7b12 | naming | ServiceBasedNamingStoreTestCase#testStoredContext | FOCAL_UNCONFIRMED | 0/0 | SKIPPED_FOCAL | status=disagreed |
| wildflynaming3a83b7b10 | naming | ServiceBasedNamingStoreTestCase#testLookupBinding | FOCAL_UNCONFIRMED | 0/0 | SKIPPED_FOCAL | status=disagreed |
| odshardingsphereelasticjob1 | NA | ElectionListenerManagerTest#assertLeaderElectionWhenRemoveLeaderInstancePathWithAvailableServerButJobInstanceIsShutdown | NONE | 0/0 | NA_NO_CONFIG | canonical OD test with no test_config entry (not runnable via config) |
| oduniversalgcodesender1 | NA | GrblControllerTest#rawResponseHandlerOnErrorWithNoSentCommandsShouldSendMessageToConsole | NONE | 0/0 | NA_NO_CONFIG | canonical OD test with no test_config entry (not runnable via config) |
| oduniversalgcodesender2 | NA | GrblControllerTest#rawResponseHandlerWithKnownErrorShouldWriteMessageToConsole | NONE | 0/0 | NA_NO_CONFIG | canonical OD test with no test_config entry (not runnable via config) |
| oduniversalgcodesender3 | NA | GrblControllerTest#rawResponseHandlerWithUnknownErrorShouldWriteGenericMessageToConsole | NONE | 0/0 | NA_NO_CONFIG | canonical OD test with no test_config entry (not runnable via config) |
| oddubbo1 | NA | CacheTest#testCache | NONE | 0/0 | NA_NO_CONFIG | canonical OD test with no test_config entry (not runnable via config) |
| shardingsphereelasticjobelasticjoblitecore23a2ab6 | elastic-job-lite-core | ShutdownListenerManagerTest#assertIsShutdownAlready | FOCAL_UNCONFIRMED | 0/0 | SKIPPED_FOCAL | status=disagreed |
| shardingsphereelasticjobelasticjoblitecore4b9afa4 | elastic-job-lite-core | JobRegistryTest#assertGetCurrentShardingTotalCountIfNull | FOCAL_UNCONFIRMED | 0/0 | SKIPPED_FOCAL | status=disagreed |
| ACCUMULO-2102_testSetInstance_HdfsZooInstance_HostsGiven | core | ShellSetInstanceTest#testSetInstance_HdfsZooInstance_HostsGiven | FOCAL_UNCONFIRMED | 0/0 | SKIPPED_FOCAL | status=llm |
| ACCUMULO-2102_testSetInstance_HdfsZooInstance_InstanceGiven | core | ShellSetInstanceTest#testSetInstance_HdfsZooInstance_InstanceGiven | FOCAL_UNCONFIRMED | 0/0 | SKIPPED_FOCAL | status=llm |
| ACCUMULO-2102_testSetInstance_HdfsZooInstance_Explicit | core | ShellSetInstanceTest#testSetInstance_HdfsZooInstance_Explicit | FOCAL_UNCONFIRMED | 0/0 | SKIPPED_FOCAL | status=llm |
| ACCUMULO-2102_testSetInstance_HdfsZooInstance_Implicit | core | ShellSetInstanceTest#testSetInstance_HdfsZooInstance_Implicit | FOCAL_UNCONFIRMED | 0/0 | SKIPPED_FOCAL | status=llm |
| jnrposixd9f3f84 | . | LazyPOSIX#getgroups | jnr.posix.LazyPOSIX_getgroups_146_0_Test | 0/0 | SWEEP_NA | focal jaccard+llm agreed; pristine pom + mockito(junit excl); ordering 3.8.6 custom-surefire; coverage/mutation pending |
| marineapi0a1f308 | . | AbstractAISMessageListener#sentenceRead | net.sf.marineapi.ais.event.AbstractAISMessageListener_sentenceRead_0_0_Test | 100/100 | NOT_OD | focal jaccard+llm agreed; pristine pom + mockito(junit excl); ordering 3.8.6 custom-surefire; coverage/mutation pending |
| ormlitecore59309e89 | . | SchemaUtils#dropSchema | GENERATED | 0/0 | CANDIDATE_FAILED | generated candidate(s) did not pass alone |
| dubbodubborpcdubborpcdubbo628ad771 | dubbo-rpc/dubbo-rpc-dubbo | PortTelnetHandler#telnet | org.apache.dubbo.rpc.protocol.dubbo.telnet.PortTelnetHandler_telnet_0_0_Test | 0/0 | SWEEP_NA | focal jaccard+llm agreed; pristine pom + mockito(junit excl); ordering 3.8.6 custom-surefire; coverage/mutation pending |
| dubbodubborpcdubborpcdubbo628ad77 | dubbo-rpc/dubbo-rpc-dubbo | PortTelnetHandler#telnet | GENERATED | 0/0 | CANDIDATE_FAILED | generated candidate(s) did not pass alone |
| shardingsphereelasticjobelasticjoblitecore23a2ab5 | elastic-job-lite-core | FailoverService#getLocalFailoverItems | GENERATED | 0/0 | CANDIDATE_FAILED | generated candidate(s) did not pass alone |
| shardingsphereelasticjobelasticjoblitecore90e3a7f | elastic-job-lite-core | ZookeeperRegistryCenter#persistEphemeralSequential | GENERATED | 0/0 | CANDIDATE_FAILED | generated candidate(s) did not pass alone |
| wildflynaming3a83b7b21 | naming | WritableServiceBasedNamingStore#rebind | GENERATED | 0/0 | CANDIDATE_FAILED | generated candidate(s) did not pass alone |
| wildflynaming3a83b7b20 | naming | WritableServiceBasedNamingStore#bind | GENERATED | 0/0 | CANDIDATE_FAILED | generated candidate(s) did not pass alone |
| dubbodubborpcdubborpcdubbo628ad77 | dubbo-rpc/dubbo-rpc-dubbo | PortTelnetHandler#telnet | org.apache.dubbo.rpc.protocol.dubbo.telnet.PortTelnetHandler_telnet_0_0_Test | 0/0 | SWEEP_NA | focal jaccard+llm agreed; pristine pom + mockito(junit excl); ordering 3.8.6 custom-surefire; coverage/mutation pending |
| wildflynaming3a83b7b19 | naming | WritableServiceBasedNamingStore#bind | GENERATED | 0/0 | CANDIDATE_FAILED | generated candidate(s) did not pass alone |
| wildflynaming3a83b7b11 | naming | ServiceBasedNamingStore#lookup | GENERATED | 0/0 | CANDIDATE_FAILED | generated candidate(s) did not pass alone |
