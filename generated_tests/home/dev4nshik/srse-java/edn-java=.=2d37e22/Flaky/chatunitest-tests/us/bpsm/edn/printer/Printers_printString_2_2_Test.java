package us.bpsm.edn.printer;

import org.junit.jupiter.api.function.Executable;
import us.bpsm.edn.protocols.Protocol;
import us.bpsm.edn.printer.Printer;
import us.bpsm.edn.printer.Printers;
import java.lang.reflect.Constructor;
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

public class Printers_printString_2_2_Test {

    private Protocol<Printer.Fn<?>> mockProtocol;

    private Printer mockPrinter;

    @BeforeEach
    public void setUp() {
        mockProtocol = mock(Protocol.class);
        mockPrinter = mock(Printer.class);
    }

    @Test
    public void testPrivateConstructor() throws Exception {
        Constructor<Printers> constructor = Printers.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        Assertions.assertThrows(InvocationTargetException.class, new Executable() {

            @Override
            public void execute() throws Throwable {
                constructor.newInstance();
            }
        });
    }
}
