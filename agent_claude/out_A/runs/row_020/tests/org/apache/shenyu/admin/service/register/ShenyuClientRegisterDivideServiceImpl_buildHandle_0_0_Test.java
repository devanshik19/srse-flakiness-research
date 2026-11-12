package org.apache.shenyu.admin.service.register;

import org.apache.shenyu.admin.model.entity.SelectorDO;
import org.apache.shenyu.admin.service.converter.DivideSelectorHandleConverter;
import org.apache.shenyu.admin.service.impl.UpstreamCheckService;
import org.apache.shenyu.admin.utils.CommonUpstreamUtils;
import org.apache.shenyu.common.dto.convert.selector.CommonUpstream;
import org.apache.shenyu.common.dto.convert.selector.DivideUpstream;
import org.apache.shenyu.common.utils.GsonUtils;
import org.apache.shenyu.register.common.dto.URIRegisterDTO;
import org.apache.shenyu.register.common.enums.EventType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.test.util.ReflectionTestUtils;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class ShenyuClientRegisterDivideServiceImpl_buildHandle_0_0_Test {

    private ShenyuClientRegisterDivideServiceImpl service;

    private UpstreamCheckService upstreamCheckService;

    @BeforeEach
    public void setUp() {
        service = new ShenyuClientRegisterDivideServiceImpl();
        upstreamCheckService = mock(UpstreamCheckService.class);
        when(upstreamCheckService.checkAndSubmit(anyString(), any(CommonUpstream.class))).thenReturn(false);
        ReflectionTestUtils.setField(service, "divideSelectorHandleConverter", new DivideSelectorHandleConverter());
        ReflectionTestUtils.setField(service, AbstractShenyuClientRegisterServiceImpl.class, "upstreamCheckService", upstreamCheckService, UpstreamCheckService.class);
    }

    private URIRegisterDTO uri(final int port, final EventType type) {
        return URIRegisterDTO.builder().protocol("http://").appName("app").host("localhost").port(port).eventType(type).build();
    }

    private SelectorDO selector(final String handle) {
        SelectorDO selectorDO = new SelectorDO();
        selectorDO.setId("1");
        selectorDO.setHandle(handle);
        return selectorDO;
    }

    private String existHandle(final boolean status, final int... ports) {
        List<DivideUpstream> list = new ArrayList<>();
        for (int p : ports) {
            DivideUpstream u = CommonUpstreamUtils.buildDivideUpstream("http://", "localhost", p);
            u.setStatus(status);
            list.add(u);
        }
        return GsonUtils.getInstance().toJson(list);
    }

    @Test
    public void testEmptyExistNullHandle() {
        List<URIRegisterDTO> list = new ArrayList<>();
        list.add(uri(8080, null));
        list.add(uri(8081, null));
        String result = service.buildHandle(list, selector(null));
        List<DivideUpstream> res = GsonUtils.getInstance().fromCurrentList(result, DivideUpstream.class);
        assertEquals(2, res.size());
    }

    @Test
    public void testEmptyExistEmptyArrayDeleted() {
        String result = service.buildHandle(Collections.singletonList(uri(8080, EventType.DELETED)), selector("[]"));
        List<DivideUpstream> res = GsonUtils.getInstance().fromCurrentList(result, DivideUpstream.class);
        assertEquals(1, res.size());
        assertFalse(res.get(0).isStatus());
    }

    @Test
    public void testDoSubmitTrue() {
        when(upstreamCheckService.checkAndSubmit(anyString(), any(CommonUpstream.class))).thenReturn(true);
        assertNull(service.buildHandle(Collections.singletonList(uri(8080, null)), selector(null)));
    }

    @Test
    public void testExistWithDiff() {
        List<URIRegisterDTO> list = new ArrayList<>();
        list.add(uri(8080, null));
        list.add(uri(8081, null));
        String result = service.buildHandle(list, selector(existHandle(true, 8080)));
        List<DivideUpstream> res = GsonUtils.getInstance().fromCurrentList(result, DivideUpstream.class);
        assertEquals(2, res.size());
        assertTrue(res.stream().allMatch(DivideUpstream::isStatus));
    }

    @Test
    public void testExistNoDiffSameStatus() {
        String result = service.buildHandle(Collections.singletonList(uri(8080, null)), selector(existHandle(true, 8080)));
        List<DivideUpstream> res = GsonUtils.getInstance().fromCurrentList(result, DivideUpstream.class);
        assertEquals(1, res.size());
        assertTrue(res.get(0).isStatus());
    }

    @Test
    public void testExistDiffStatus() {
        String result = service.buildHandle(Collections.singletonList(uri(8080, EventType.REGISTER)), selector(existHandle(false, 8080)));
        List<DivideUpstream> res = GsonUtils.getInstance().fromCurrentList(result, DivideUpstream.class);
        assertEquals(1, res.size());
        assertTrue(res.get(0).isStatus());
    }

    @Test
    public void testExistDeleted() {
        String result = service.buildHandle(Collections.singletonList(uri(8080, EventType.DELETED)), selector(existHandle(true, 8080, 8081)));
        assertNotNull(result);
        List<DivideUpstream> res = GsonUtils.getInstance().fromCurrentList(result, DivideUpstream.class);
        assertEquals(2, res.size());
        for (DivideUpstream u : res) {
            if (u.getUpstreamUrl().endsWith("8080")) {
                assertFalse(u.isStatus());
            } else {
                assertTrue(u.isStatus());
            }
        }
    }

    @Test
    public void testExistDeletedOnlyOne() {
        String result = service.buildHandle(Collections.singletonList(uri(8080, EventType.DELETED)), selector(existHandle(true, 8080)));
        List<DivideUpstream> res = GsonUtils.getInstance().fromCurrentList(result, DivideUpstream.class);
        assertTrue(res.isEmpty());
    }
}
