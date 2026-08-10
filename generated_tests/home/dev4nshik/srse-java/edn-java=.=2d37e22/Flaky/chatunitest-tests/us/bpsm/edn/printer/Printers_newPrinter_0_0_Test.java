package us.bpsm.edn.printer;

import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;
import us.bpsm.edn.printer.Printers;
import us.bpsm.edn.protocols.Protocol;
import us.bpsm.edn.printer.Printer;
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

public class Printers_newPrinter_0_0_Test {

    private Appendable testAppendable;

    @BeforeEach
    public void setUp() {
        testAppendable = new StringBuilder();
    }

    @AfterEach
    public void tearDown() {
        testAppendable = null;
    }

    @Test
    public void testNewPrinter() {
        try {
            // Use reflection to access the private method newPrinter(Protocol, Appendable)
            Method newPrinterMethod = Printers.class.getDeclaredMethod("newPrinter", Protocol.class, Appendable.class);
            newPrinterMethod.setAccessible(true);
            // Get the default protocol using the public method
            Protocol<Printer.Fn<?>> protocol = Printers.defaultPrinterProtocol();
            // Invoke the private method newPrinter(Protocol, Appendable)
            Printer printer = (Printer) newPrinterMethod.invoke(null, protocol, testAppendable);
            assertNotNull(printer, "The printer should not be null");
        } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
            fail("Exception occurred during reflection: " + e.getMessage());
        }
    }
}
