package org.apache.hadoop.yarn.service.client;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.yarn.api.protocolrecords.GetApplicationsRequest;
import org.apache.hadoop.yarn.api.records.ApplicationId;
import org.apache.hadoop.yarn.api.records.ApplicationReport;
import org.apache.hadoop.yarn.api.records.YarnApplicationState;
import org.apache.hadoop.yarn.client.api.YarnClient;
import org.apache.hadoop.yarn.exceptions.YarnException;
import org.apache.hadoop.yarn.proto.ClientAMProtocol.UpgradeServiceRequestProto;
import org.apache.hadoop.yarn.proto.ClientAMProtocol.UpgradeServiceResponseProto;
import org.apache.hadoop.yarn.service.ClientAMProtocol;
import org.apache.hadoop.yarn.service.ServiceTestUtils;
import org.apache.hadoop.yarn.service.api.records.Service;
import org.apache.hadoop.yarn.service.api.records.ServiceState;
import org.apache.hadoop.yarn.service.conf.YarnServiceConf;
import org.apache.hadoop.yarn.service.exceptions.ErrorStrings;
import org.junit.Assert;
import org.junit.Rule;
import org.junit.Test;
import org.mockito.ArgumentCaptor;

import java.io.IOException;
import java.util.ArrayList;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

public class ServiceClient_actionUpgradeExpress_0_0_Test {

  @Rule
  public ServiceTestUtils.ServiceFSWatcher rule =
      new ServiceTestUtils.ServiceFSWatcher();

  private static final class MockClient extends ServiceClient {
    final ApplicationId appId =
        ApplicationId.newInstance(System.currentTimeMillis(), 1);
    final ClientAMProtocol amProxy = mock(ClientAMProtocol.class);

    @Override
    protected void serviceInit(Configuration configuration) throws Exception {
    }

    @Override
    protected ClientAMProtocol createAMProxy(String serviceName,
        ApplicationReport appReport) throws IOException, YarnException {
      return amProxy;
    }

    @Override
    ApplicationId submitApp(Service app) throws IOException, YarnException {
      return appId;
    }

    @Override
    public Service getStatus(String serviceName) throws IOException,
        YarnException {
      Service s = new Service();
      s.setName(serviceName);
      s.setState(ServiceState.STABLE);
      return s;
    }
  }

  private MockClient create(Service service, boolean enable,
      UpgradeServiceResponseProto response) throws Exception {
    MockClient client = new MockClient();
    service.setId(client.appId.toString());
    YarnClient yarnClient = mock(YarnClient.class);
    when(yarnClient.getApplications(any(GetApplicationsRequest.class)))
        .thenReturn(new ArrayList<>());
    ApplicationReport appReport = mock(ApplicationReport.class);
    when(appReport.getHost()).thenReturn("localhost");
    when(appReport.getYarnApplicationState())
        .thenReturn(YarnApplicationState.RUNNING);
    when(yarnClient.getApplicationReport(client.appId)).thenReturn(appReport);
    when(client.amProxy.upgrade(any(UpgradeServiceRequestProto.class)))
        .thenReturn(response);
    client.setFileSystem(rule.getFs());
    client.setYarnClient(yarnClient);
    rule.getConf().setBoolean(YarnServiceConf.YARN_SERVICE_UPGRADE_ENABLED,
        enable);
    client.init(rule.getConf());
    client.start();
    client.actionCreate(service);
    return client;
  }

  private Service createService() throws Exception {
    Service service = ServiceTestUtils.createExampleApplication();
    service.setVersion("v1");
    service.setState(ServiceState.UPGRADING);
    return service;
  }

  private UpgradeServiceRequestProto run(ServiceState state) throws Exception {
    Service service = createService();
    MockClient client = create(service, true,
        UpgradeServiceResponseProto.newBuilder().build());
    service.setVersion("v2");
    service.setState(state);
    Assert.assertEquals(0, client.actionUpgradeExpress(service));
    ArgumentCaptor<UpgradeServiceRequestProto> captor =
        ArgumentCaptor.forClass(UpgradeServiceRequestProto.class);
    verify(client.amProxy).upgrade(captor.capture());
    client.stop();
    UpgradeServiceRequestProto req = captor.getValue();
    Assert.assertEquals("v2", req.getVersion());
    return req;
  }

  @Test
  public void testExpressUpgrading() throws Exception {
    UpgradeServiceRequestProto req = run(ServiceState.EXPRESS_UPGRADING);
    Assert.assertTrue(req.getExpressUpgrade());
    Assert.assertTrue(req.getAutoFinalize());
  }

  @Test
  public void testAutoFinalize() throws Exception {
    UpgradeServiceRequestProto req =
        run(ServiceState.UPGRADING_AUTO_FINALIZE);
    Assert.assertFalse(req.getExpressUpgrade());
    Assert.assertTrue(req.getAutoFinalize());
  }

  @Test
  public void testPlainUpgrading() throws Exception {
    UpgradeServiceRequestProto req = run(ServiceState.UPGRADING);
    Assert.assertFalse(req.getExpressUpgrade());
    Assert.assertFalse(req.getAutoFinalize());
  }

  @Test
  public void testErrorResponse() throws Exception {
    Service service = createService();
    MockClient client = create(service, true,
        UpgradeServiceResponseProto.newBuilder().setError("boom").build());
    service.setVersion("v2");
    service.setState(ServiceState.EXPRESS_UPGRADING);
    try {
      client.actionUpgradeExpress(service);
      Assert.fail();
    } catch (YarnException e) {
      Assert.assertTrue(e.getMessage().contains("boom"));
      Assert.assertTrue(e.getMessage().contains("v2"));
    }
    client.stop();
  }

  @Test
  public void testUpgradeDisabled() throws Exception {
    Service service = createService();
    MockClient client = create(service, false,
        UpgradeServiceResponseProto.newBuilder().build());
    service.setVersion("v2");
    service.setState(ServiceState.EXPRESS_UPGRADING);
    try {
      client.actionUpgradeExpress(service);
      Assert.fail();
    } catch (YarnException e) {
      Assert.assertEquals(ErrorStrings.SERVICE_UPGRADE_DISABLED,
          e.getMessage());
    }
    verify(client.amProxy, never()).upgrade(
        any(UpgradeServiceRequestProto.class));
    client.stop();
  }

  @Test
  public void testSameVersion() throws Exception {
    Service service = createService();
    MockClient client = create(service, true,
        UpgradeServiceResponseProto.newBuilder().build());
    service.setState(ServiceState.EXPRESS_UPGRADING);
    try {
      client.actionUpgradeExpress(service);
      Assert.fail();
    } catch (YarnException e) {
      Assert.assertTrue(e.getMessage().contains("already at version"));
    }
    client.stop();
  }
}
