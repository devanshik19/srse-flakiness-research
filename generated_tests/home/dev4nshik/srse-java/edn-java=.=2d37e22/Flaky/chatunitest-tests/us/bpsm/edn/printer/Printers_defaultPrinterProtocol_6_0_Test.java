package us.bpsm.edn.printer;

import us.bpsm.edn.printer.Printers;
import us.bpsm.edn.protocols.Protocol;
import us.bpsm.edn.printer.Printer;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
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

@ExtendWith(MockitoExtension.class)
class Printers_defaultPrinterProtocol_6_0_Test {

    @Test
    void testDefaultPrinterProtocol() {
        try {
            // Use reflection to invoke the private static method defaultProtocolBuilder
            Method method = Printers.class.getDeclaredMethod("defaultPrinterProtocol");
            method.setAccessible(true);
            // Invoke the method and get the result
            Protocol<Printer.Fn<?>> protocol = (Protocol<Printer.Fn<?>>) method.invoke(null);
            // Assert that the protocol is not null
            assertNotNull(protocol, "The protocol should not be null");
            // Further assertions can be added here based on expected behavior of the protocol
            // Since the Protocol class might not have a get method, we cannot directly test it
            // without knowing the actual implementation details of Protocol.
            // Add more assertions as necessary for other classes
        } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
            fail("Exception occurred while testing defaultPrinterProtocol: " + e.getMessage());
        }
    }
}
