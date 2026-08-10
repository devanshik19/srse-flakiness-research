package us.bpsm.edn.printer;

import us.bpsm.edn.printer.Printers;
import us.bpsm.edn.protocols.Protocol;
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

public class Printers_defaultProtocolBuilder_5_1_Test {

    @Test
    public void testDefaultProtocolBuilder() {
        try {
            // Use reflection to access the private method
            Method method = Printers.class.getDeclaredMethod("defaultProtocolBuilder");
            method.setAccessible(true);
            // Invoke the method
            Protocol.Builder<?> protocolBuilder = (Protocol.Builder<?>) method.invoke(null);
            // Assert that the protocol builder is not null
            assertNotNull(protocolBuilder, "Protocol builder should not be null.");
            // Optionally, you can add more assertions here to check the state of the protocolBuilder
            // For example, you might want to check if certain classes are mapped to expected functions
        } catch (Exception e) {
            fail("Exception occurred while testing defaultProtocolBuilder: " + e.getMessage());
        }
    }
}
