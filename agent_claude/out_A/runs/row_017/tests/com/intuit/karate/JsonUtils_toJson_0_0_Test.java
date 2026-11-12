package com.intuit.karate;

import java.util.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class JsonUtils_toJson_0_0_Test {

    @Test
    void testNull() {
        assertEquals("null", JsonUtils.toJson(null));
    }

    @Test
    void testString() {
        assertEquals("\"hello\"", JsonUtils.toJson("hello"));
    }

    @Test
    void testNumberAndBoolean() {
        assertEquals("5", JsonUtils.toJson(5));
        assertEquals("true", JsonUtils.toJson(true));
    }

    @Test
    void testMap() {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("a", 1);
        map.put("b", "x");
        assertEquals("{\"a\":1,\"b\":\"x\"}", JsonUtils.toJson(map));
    }

    @Test
    void testList() {
        List<Object> list = new ArrayList<>();
        list.add(1);
        list.add("two");
        list.add(null);
        assertEquals("[1,\"two\",null]", JsonUtils.toJson(list));
    }

    @Test
    void testCyclicMapFallsBackToSafe() {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("a", 1);
        map.put("self", map);
        String json = JsonUtils.toJson(map);
        assertTrue(json.startsWith("{\"a\":1,\"self\":"));
        assertTrue(json.contains("#ref:"));
    }

    @Test
    void testThrowingMapFallsBackToSafe() {
        Map<String, Object> map = new LinkedHashMap<String, Object>() {
            int calls = 0;
            @Override
            public Set<Map.Entry<String, Object>> entrySet() {
                if (calls++ == 0) {
                    throw new RuntimeException("boom");
                }
                return super.entrySet();
            }
        };
        map.put("k", "v");
        assertEquals("{\"k\":\"v\"}", JsonUtils.toJson(map));
    }
}
