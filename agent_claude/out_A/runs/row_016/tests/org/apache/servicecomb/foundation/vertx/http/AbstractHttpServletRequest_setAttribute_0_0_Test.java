package org.apache.servicecomb.foundation.vertx.http;

import java.lang.reflect.Field;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class AbstractHttpServletRequest_setAttribute_0_0_Test {
  private AbstractHttpServletRequest request;

  @BeforeEach
  public void setUp() {
    request = new AbstractHttpServletRequest() {
    };
  }

  @SuppressWarnings("unchecked")
  private Map<String, Object> attributeMap() throws Exception {
    Field f = AbstractHttpServletRequest.class.getDeclaredField("attributeMap");
    f.setAccessible(true);
    return (Map<String, Object>) f.get(request);
  }

  @Test
  public void testSetAttribute() throws Exception {
    Object value = new Object();
    request.setAttribute("k", value);
    Assertions.assertSame(value, request.getAttribute("k"));
    Assertions.assertSame(value, attributeMap().get("k"));
  }

  @Test
  public void testOverwrite() throws Exception {
    request.setAttribute("k", "v1");
    request.setAttribute("k", "v2");
    Assertions.assertEquals("v2", request.getAttribute("k"));
    Assertions.assertEquals(1, attributeMap().size());
  }

  @Test
  public void testNullValueAndNullKey() throws Exception {
    request.setAttribute("k", null);
    Assertions.assertTrue(attributeMap().containsKey("k"));
    Assertions.assertNull(request.getAttribute("k"));
    request.setAttribute(null, "v");
    Assertions.assertEquals("v", request.getAttribute(null));
  }

  @Test
  public void testMultiple() {
    request.setAttribute("a", 1);
    request.setAttribute("b", 2);
    List<String> names = Collections.list(request.getAttributeNames());
    Assertions.assertEquals(new HashSet<>(java.util.Arrays.asList("a", "b")), new HashSet<>(names));
    request.removeAttribute("a");
    Assertions.assertNull(request.getAttribute("a"));
    Assertions.assertEquals(2, request.getAttribute("b"));
  }
}
