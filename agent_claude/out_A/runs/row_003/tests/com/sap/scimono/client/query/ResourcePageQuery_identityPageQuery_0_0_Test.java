package com.sap.scimono.client.query;

import static org.junit.jupiter.api.Assertions.*;

import java.lang.reflect.Field;
import java.util.Map;

import org.junit.jupiter.api.Test;

class ResourcePageQuery_identityPageQuery_0_0_Test {

  @SuppressWarnings("unchecked")
  private Map<String, Object> params(IdentityPageQuery q) throws Exception {
    Field f = IdentityPageQuery.class.getDeclaredField("resourcePageQuery");
    f.setAccessible(true);
    ResourcePageQuery rpq = (ResourcePageQuery) f.get(q);
    Field m = ResourcePageQuery.class.getDeclaredField("queryParams");
    m.setAccessible(true);
    return (Map<String, Object>) m.get(rpq);
  }

  @Test
  void returnsQueryWithDefaults() throws Exception {
    IdentityPageQuery q = ResourcePageQuery.identityPageQuery();
    assertNotNull(q);
    Map<String, Object> p = params(q);
    assertEquals(2, p.size());
    assertEquals("00000000-0000-1000-9000-000000000000", p.get("startId"));
    assertEquals(100, p.get("count"));
    assertEquals(ResourcePageQuery.DEFAULT_COUNT, p.get("count"));
  }

  @Test
  void returnsNewInstanceEachCall() throws Exception {
    IdentityPageQuery q1 = ResourcePageQuery.identityPageQuery();
    IdentityPageQuery q2 = ResourcePageQuery.identityPageQuery();
    assertNotSame(q1, q2);
    q1.withCount(5);
    assertEquals(5, params(q1).get("count"));
    assertEquals(100, params(q2).get("count"));
  }
}
