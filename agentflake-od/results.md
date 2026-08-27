# AgentFlake OD — results

| subject | module | focal_method | generated_test | alone | sweep_orders | sweep_pass | ctrl_polluterFirst | ctrl_victimFirst | gen_polluterFirst | od_verdict | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dubbodubborpcdubborpcapiba89f44 | dubbo-rpc/dubbo-rpc-api | JavassistProxyFactory#getInvoker | JavassistProxyFactory_getInvoker_1_1_Test | pass | 100 | 100 | 0/30 | 30/0 | 30/0 | NOT_OD | generated test robust but weak-assertion (only assertNotNull); coverage/mutation pending |
| apiba89f441 | dubbo-rpc/dubbo-rpc-api | org.apache.dubbo.rpc.proxy.jdk.JdkProxyFactory#getInvoker | org.apache.dubbo.rpc.proxy.jdk.JdkProxyFactory_getInvoker_1_0_Test#testGetInvoker | alone=pass | sweep=100/100 | ctrlPF=0/30 | ctrlVF=30/0 | genPF=30/0 | NOT_OD | jdk proxy focal; robust; coverage/mutation pending |  |
