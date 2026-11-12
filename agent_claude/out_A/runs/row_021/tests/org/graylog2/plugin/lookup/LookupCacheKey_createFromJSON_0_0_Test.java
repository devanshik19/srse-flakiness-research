package org.graylog2.plugin.lookup;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.Test;

import static org.junit.Assert.*;

public class LookupCacheKey_createFromJSON_0_0_Test {

    @Test
    public void createWithKey() {
        LookupCacheKey k = LookupCacheKey.createFromJSON("prefix", "key");
        assertEquals("prefix", k.prefix());
        assertEquals("key", k.key());
        assertFalse(k.isPrefixOnly());
        assertEquals(LookupCacheKey.createFromJSON("prefix", "key"), k);
        assertEquals(LookupCacheKey.createFromJSON("prefix", "key").hashCode(), k.hashCode());
    }

    @Test
    public void createWithNullKey() {
        LookupCacheKey k = LookupCacheKey.createFromJSON("prefix", null);
        assertEquals("prefix", k.prefix());
        assertNull(k.key());
        assertTrue(k.isPrefixOnly());
    }

    @Test(expected = NullPointerException.class)
    public void createWithNullPrefix() {
        LookupCacheKey.createFromJSON(null, "key");
    }

    @Test
    public void jsonRoundTrip() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        LookupCacheKey k = LookupCacheKey.createFromJSON("p", 42);
        String json = mapper.writeValueAsString(k);
        LookupCacheKey back = mapper.readValue(json, LookupCacheKey.class);
        assertEquals(k, back);
        LookupCacheKey n = mapper.readValue("{\"prefix\":\"x\"}", LookupCacheKey.class);
        assertEquals("x", n.prefix());
        assertTrue(n.isPrefixOnly());
    }
}
