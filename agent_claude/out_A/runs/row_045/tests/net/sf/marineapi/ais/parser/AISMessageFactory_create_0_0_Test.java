package net.sf.marineapi.ais.parser;

import static org.junit.Assert.*;

import net.sf.marineapi.ais.message.AISMessage;
import net.sf.marineapi.ais.message.AISMessage01;
import net.sf.marineapi.ais.message.AISMessage05;
import net.sf.marineapi.nmea.parser.SentenceFactory;
import net.sf.marineapi.nmea.sentence.AISSentence;

import org.junit.Test;

public class AISMessageFactory_create_0_0_Test {

    private final SentenceFactory sf = SentenceFactory.getInstance();
    private final AISMessageFactory amf = AISMessageFactory.getInstance();

    private AISSentence s(String str) {
        return (AISSentence) sf.createParser(str);
    }

    @Test
    public void testSingleton() {
        assertSame(amf, AISMessageFactory.getInstance());
    }

    @Test
    public void testCreateType1() {
        AISMessage msg = amf.create(s("!AIVDM,1,1,,A,13aEOK?P00PD2wVMdLDRhgvL289?,0*26"));
        assertTrue(msg instanceof AISMessage01);
        assertEquals(1, msg.getMessageType());
    }

    @Test
    public void testCreateType5Fragmented() {
        AISMessage msg = amf.create(
                s("!AIVDM,2,1,9,B,53nFBv01SJ<thHp6220H4heHTf2222222222221?50:454o<`9QSlUDp,0*09"),
                s("!AIVDM,2,2,9,B,888888888888880,2*2E"));
        assertTrue(msg instanceof AISMessage05);
        assertEquals(5, msg.getMessageType());
    }

    @Test
    public void testIncorrectOrder() {
        try {
            amf.create(s("!AIVDM,2,2,9,B,888888888888880,2*2E"),
                    s("!AIVDM,2,1,9,B,53nFBv01SJ<thHp6220H4heHTf2222222222221?50:454o<`9QSlUDp,0*09"));
            fail();
        } catch (IllegalArgumentException e) {
            assertEquals("Incorrect order of AIS sentences", e.getMessage());
        }
    }

    @Test
    public void testUnsupportedType() {
        try {
            amf.create(s("!AIVDM,1,1,,A,63aEOK?P00PD2wVMdLDRhgvL289?,0"));
            fail();
        } catch (IllegalArgumentException e) {
            assertEquals("no parser for message type 6", e.getMessage());
        }
    }

    @Test
    public void testInvalidMessageLength() {
        try {
            amf.create(s("!AIVDM,1,1,,A,13aEOK?P00,0"));
            fail();
        } catch (IllegalStateException e) {
            // expected
        }
    }
}
