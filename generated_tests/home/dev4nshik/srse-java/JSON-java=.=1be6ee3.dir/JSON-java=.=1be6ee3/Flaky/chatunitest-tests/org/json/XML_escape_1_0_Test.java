package org.json;

import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import /*
Public Domain.
*/
java.io.Reader;
import java.io.StringReader;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Iterator;

public class XML_escape_1_0_Test {

    @Test
    public void testEscape() throws Exception {
        // Test cases for the escape method
        assertEquals("Hello &amp; World", invokeEscape("Hello & World"));
        assertEquals("&lt;tag&gt;", invokeEscape("<tag>"));
        assertEquals("This is a &quot;quote&quot;", invokeEscape("This is a \"quote\""));
        assertEquals("Apostrophe&apos;s test", invokeEscape("Apostrophe's test"));
        // Control character
        assertEquals("&#x1F;", invokeEscape("\u001F"));
        assertEquals("Normal text", invokeEscape("Normal text"));
        // Invalid XML character
        assertEquals("&#xFFFE;", invokeEscape("\uFFFE"));
    }

    private String invokeEscape(String input) throws Exception {
        // Use reflection to access the private method
        Method escapeMethod = XML.class.getDeclaredMethod("escape", String.class);
        escapeMethod.setAccessible(true);
        return (String) escapeMethod.invoke(null, input);
    }
}
