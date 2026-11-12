package com.ctrip.framework.apollo.openapi.client.service;

import static org.junit.Assert.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.ctrip.framework.apollo.openapi.dto.OpenItemDTO;
import com.ctrip.framework.apollo.openapi.dto.OpenPageDTO;
import com.google.gson.Gson;
import java.io.IOException;
import org.apache.http.StatusLine;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;

public class ItemOpenApiService_findItemsByNamespace_0_0_Test {

  private CloseableHttpClient client;
  private CloseableHttpResponse response;
  private StatusLine statusLine;
  private ItemOpenApiService service;
  private final String baseUrl = "http://someBaseUrl";

  @Before
  public void setUp() throws Exception {
    client = mock(CloseableHttpClient.class);
    response = mock(CloseableHttpResponse.class);
    statusLine = mock(StatusLine.class);
    when(response.getStatusLine()).thenReturn(statusLine);
    when(statusLine.getStatusCode()).thenReturn(200);
    when(response.getEntity()).thenReturn(new StringEntity(
        "{\"page\":1,\"size\":10,\"total\":1,\"content\":[{\"key\":\"k\",\"value\":\"v\"}]}"));
    when(client.execute(any(HttpUriRequest.class))).thenReturn(response);
    service = new ItemOpenApiService(client, baseUrl, new Gson());
  }

  private String capturedUrl() throws IOException {
    ArgumentCaptor<HttpGet> captor = ArgumentCaptor.forClass(HttpGet.class);
    verify(client, times(1)).execute(captor.capture());
    return captor.getValue().getURI().toString();
  }

  @Test
  public void testSuccess() throws Exception {
    OpenPageDTO<OpenItemDTO> result = service.findItemsByNamespace("app", "DEV", "cluster", "ns", 1, 10);
    assertNotNull(result);
    assertEquals(1, result.getPage());
    assertEquals(10, result.getSize());
    assertEquals(1L, result.getTotal());
    assertEquals(1, result.getContent().size());
    assertEquals("k", result.getContent().get(0).getKey());
    assertEquals("v", result.getContent().get(0).getValue());
    String url = capturedUrl();
    assertTrue(url.startsWith(baseUrl + "/envs/DEV/apps/app/clusters/cluster/namespaces/ns/items?"));
    assertTrue(url.contains("page=1"));
    assertTrue(url.contains("size=10"));
    verify(response).close();
  }

  @Test
  public void testDefaultClusterAndNamespaceWhenNull() throws Exception {
    service.findItemsByNamespace("app", "DEV", null, null, 0, 5);
    String url = capturedUrl();
    assertTrue(url.startsWith(baseUrl + "/envs/DEV/apps/app/clusters/default/namespaces/application/items?"));
  }

  @Test
  public void testDefaultClusterAndNamespaceWhenEmpty() throws Exception {
    service.findItemsByNamespace("app", "DEV", "", "", 0, 5);
    String url = capturedUrl();
    assertTrue(url.startsWith(baseUrl + "/envs/DEV/apps/app/clusters/default/namespaces/application/items?"));
  }

  @Test(expected = IllegalArgumentException.class)
  public void testNullAppId() {
    service.findItemsByNamespace(null, "DEV", "c", "n", 0, 5);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testEmptyAppId() {
    service.findItemsByNamespace("", "DEV", "c", "n", 0, 5);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testEmptyEnv() {
    service.findItemsByNamespace("app", "", "c", "n", 0, 5);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testNullEnv() {
    service.findItemsByNamespace("app", null, "c", "n", 0, 5);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testNegativePage() {
    service.findItemsByNamespace("app", "DEV", "c", "n", -1, 5);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testZeroSize() {
    service.findItemsByNamespace("app", "DEV", "c", "n", 0, 0);
  }

  @Test
  public void testErrorStatus() throws Exception {
    when(statusLine.getStatusCode()).thenReturn(400);
    when(statusLine.getReasonPhrase()).thenReturn("Bad");
    try {
      service.findItemsByNamespace("app", "DEV", "c", "n", 0, 5);
      fail();
    } catch (RuntimeException e) {
      assertEquals("Paging get items: appId: app, cluster: c, namespace: n in env: DEV failed", e.getMessage());
      assertNotNull(e.getCause());
    }
  }

  @Test
  public void testIOException() throws Exception {
    when(client.execute(any(HttpUriRequest.class))).thenThrow(new IOException("io"));
    try {
      service.findItemsByNamespace("app", "DEV", null, null, 0, 5);
      fail();
    } catch (RuntimeException e) {
      assertEquals("Paging get items: appId: app, cluster: default, namespace: application in env: DEV failed",
          e.getMessage());
      assertTrue(e.getCause() instanceof IOException);
    }
  }
}
