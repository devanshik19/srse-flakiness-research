package us.bpsm.edn.printer;

import java.lang.reflect.Method;
import us.bpsm.edn.printer.Printers;
import us.bpsm.edn.protocols.Protocol;
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

public class Printers_printString_1_0_Test {

    @Test
    public void testPrintString() throws Exception {
        // Arrange
        Object testObject = "test";
        // Act
        String result = Printers.printString(testObject);
        // Assert
        assertNotNull(result);
    }

    @Test
    public void testDefaultPrinterProtocol() throws Exception {
        // Using reflection to invoke private method
        Method method = Printers.class.getDeclaredMethod("defaultPrinterProtocol");
        method.setAccessible(true);
        // Act
        Protocol<?> protocol = (Protocol<?>) method.invoke(null);
        // Assert
        assertNotNull(protocol);
    }
}
