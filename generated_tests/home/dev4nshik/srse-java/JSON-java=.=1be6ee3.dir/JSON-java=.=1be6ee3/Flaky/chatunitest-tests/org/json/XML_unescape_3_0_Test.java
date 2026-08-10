package org.json;

import org.json.XML;
import org.json.XMLTokener;
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

public class XML_unescape_3_0_Test {

    @Test
    public void testUnescape() throws Exception {
        // Access the private method using reflection
        Method unescapeMethod = XML.class.getDeclaredMethod("unescape", String.class);
        unescapeMethod.setAccessible(true);
        // Test cases
        String input1 = "Hello &amp; World";
        String expected1 = "Hello & World";
        String result1 = (String) unescapeMethod.invoke(null, input1);
        assertEquals(expected1, result1);
        String input2 = "The &lt;tag&gt; is here";
        String expected2 = "The <tag> is here";
        String result2 = (String) unescapeMethod.invoke(null, input2);
        assertEquals(expected2, result2);
        String input3 = "Use &quot;quotes&quot; wisely";
        String expected3 = "Use \"quotes\" wisely";
        String result3 = (String) unescapeMethod.invoke(null, input3);
        assertEquals(expected3, result3);
        String input4 = "Incomplete &entity";
        String expected4 = "Incomplete &entity";
        String result4 = (String) unescapeMethod.invoke(null, input4);
        assertEquals(expected4, result4);
        String input5 = "No entities here";
        String expected5 = "No entities here";
        String result5 = (String) unescapeMethod.invoke(null, input5);
        assertEquals(expected5, result5);
        String input6 = "Numeric &#x41; and decimal &#65;";
        String expected6 = "Numeric A and decimal A";
        String result6 = (String) unescapeMethod.invoke(null, input6);
        assertEquals(expected6, result6);
    }
}
