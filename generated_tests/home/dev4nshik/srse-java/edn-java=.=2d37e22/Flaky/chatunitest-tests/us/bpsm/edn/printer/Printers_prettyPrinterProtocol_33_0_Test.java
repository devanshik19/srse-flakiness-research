package us.bpsm.edn.printer;

import us.bpsm.edn.protocols.Protocol;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.IOException;
import java.io.Closeable;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.sql.Timestamp;
import java.util.*;
import us.bpsm.edn.EdnException;
import us.bpsm.edn.EdnIOException;
import us.bpsm.edn.Keyword;
import us.bpsm.edn.Symbol;
import us.bpsm.edn.Tag;
import us.bpsm.edn.TaggedValue;
import us.bpsm.edn.parser.InstantUtils;
import us.bpsm.edn.parser.Parser;
import us.bpsm.edn.protocols.Protocols;
import us.bpsm.edn.util.CharClassify;

class Printers_prettyPrinterProtocol_33_0_Test {

    @Test
    void testPrettyPrinterProtocol() {
        try {
            // Use reflection to access the private static method 'prettyProtocolBuilder'
            Method prettyProtocolBuilderMethod = Printers.class.getDeclaredMethod("prettyProtocolBuilder");
            prettyProtocolBuilderMethod.setAccessible(true);
            // Invoke the method to get the Protocol.Builder instance
            Object builder = prettyProtocolBuilderMethod.invoke(null);
            // Use reflection to access the 'build' method on the Protocol.Builder instance
            Method buildMethod = builder.getClass().getDeclaredMethod("build");
            buildMethod.setAccessible(true);
            // Invoke the 'build' method to get the Protocol instance
            Protocol<?> protocol = (Protocol<?>) buildMethod.invoke(builder);
            // Verify that the protocol is not null
            assertNotNull(protocol, "The protocol should not be null");
            // Verify that the protocol is an instance of the expected type
            assertTrue(protocol instanceof Protocol, "The protocol should be an instance of Protocol");
        } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
            fail("Reflection failed: " + e.getMessage());
        }
    }
}
