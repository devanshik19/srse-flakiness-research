# AgentFlake OD — results

| subject | module | focal_method | generated_test | alone | sweep_orders | sweep_pass | od_verdict | notes |
|---|---|---|---|---|---|---|---|---|
| dubbodubborpcdubborpcapiba89f44 | dubbo-rpc/dubbo-rpc-api | JavassistProxyFactory#getInvoker | JavassistProxyFactory_getInvoker_1_1_Test | pass | 100 | 100 | NOT_OD | robust but weak assertion (only assertNotNull); coverage/mutation pending |
| dubbodubborpcdubborpcapiba89f441 | dubbo-rpc/dubbo-rpc-api | JdkProxyFactory#getInvoker | JdkProxyFactory_getInvoker_1_0_Test | pass | 100 | 100 | NOT_OD | jdk proxy focal; robust; coverage/mutation pending |
