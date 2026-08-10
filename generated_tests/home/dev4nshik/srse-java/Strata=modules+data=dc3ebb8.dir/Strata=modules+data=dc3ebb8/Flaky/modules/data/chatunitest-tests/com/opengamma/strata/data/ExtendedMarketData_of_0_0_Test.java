package com.opengamma.strata.data;

import com.opengamma.strata.data.MarketData;
import com.opengamma.strata.data.MarketDataId;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.Serializable;
import java.lang.invoke.MethodHandles;
import java.time.LocalDate;
import java.util.Optional;
import java.util.Set;
import org.joda.beans.ImmutableBean;
import org.joda.beans.JodaBeanUtils;
import org.joda.beans.MetaBean;
import org.joda.beans.TypedMetaBean;
import org.joda.beans.gen.BeanDefinition;
import org.joda.beans.gen.PropertyDefinition;
import org.joda.beans.impl.light.LightMetaBean;
import com.google.common.collect.ImmutableSet;
import com.opengamma.strata.collect.timeseries.LocalDateDoubleTimeSeries;

class ExtendedMarketData_of_0_0_Test {

    private MarketDataId<String> marketDataId;

    private String value;

    private MarketData marketData;

    @BeforeEach
    void setUp() {
        marketDataId = mock(MarketDataId.class);
        value = "SampleValue";
        marketData = mock(MarketData.class);
    }

    @Test
    void testOf() {
        ExtendedMarketData<String> extendedMarketData = ExtendedMarketData.of(marketDataId, value, marketData);
        assertNotNull(extendedMarketData);
        assertEquals(marketDataId, extendedMarketData.getId());
        assertEquals(value, extendedMarketData.getValue());
        assertEquals(marketData, extendedMarketData.getUnderlying());
    }

    @Test
    void testOf_NullId() {
        assertThrows(NullPointerException.class, () -> {
            ExtendedMarketData.of(null, value, marketData);
        });
    }

    @Test
    void testOf_NullValue() {
        assertThrows(NullPointerException.class, () -> {
            ExtendedMarketData.of(marketDataId, null, marketData);
        });
    }

    @Test
    void testOf_NullUnderlying() {
        assertThrows(NullPointerException.class, () -> {
            ExtendedMarketData.of(marketDataId, value, null);
        });
    }
}
