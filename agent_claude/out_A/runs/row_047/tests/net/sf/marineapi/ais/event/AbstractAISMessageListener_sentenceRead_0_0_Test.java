package net.sf.marineapi.ais.event;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.List;

import net.sf.marineapi.ais.message.AISMessage;
import net.sf.marineapi.ais.message.AISMessage01;
import net.sf.marineapi.ais.message.AISMessage05;
import net.sf.marineapi.nmea.parser.SentenceFactory;
import net.sf.marineapi.nmea.sentence.AISSentence;

import org.junit.Test;

public class AbstractAISMessageListener_sentenceRead_0_0_Test {

    private final SentenceFactory sf = SentenceFactory.getInstance();

    private final AISSentence AIS_01 = (AISSentence) sf.createParser("!AIVDM,1,1,,A,13aEOK?P00PD2wVMdLDRhgvL289?,0*26");
    private final AISSentence AIS_05_1 = (AISSentence) sf.createParser("!AIVDM,2,1,3,B,55P5TL01VIaAL@7WKO@mBplU@<PDhh000000001S;AJ::4A80?4i@E53,0*3E");
    private final AISSentence AIS_05_2 = (AISSentence) sf.createParser("!AIVDM,2,2,3,B,1@0000000000000,2*55");

    static class Collector<T extends AISMessage> extends AbstractAISMessageListener<T> {
        final List<T> received = new ArrayList<>();
        Collector(Class<T> c) { super(c); }
        @Override
        public void onMessage(T msg) { received.add(msg); }
    }

    @Test
    public void singleFragmentMatchingType() {
        Collector<AISMessage01> c = new Collector<>(AISMessage01.class);
        c.sentenceRead(AIS_01);
        assertEquals(1, c.received.size());
        assertTrue(c.received.get(0) instanceof AISMessage01);
    }

    @Test
    public void supertypeListenerReceivesAll() {
        Collector<AISMessage> c = new Collector<>(AISMessage.class);
        c.sentenceRead(AIS_01);
        c.sentenceRead(AIS_05_1);
        c.sentenceRead(AIS_05_2);
        assertEquals(2, c.received.size());
    }

    @Test
    public void nonMatchingTypeNotDelivered() {
        Collector<AISMessage05> c = new Collector<>(AISMessage05.class);
        c.sentenceRead(AIS_01);
        assertTrue(c.received.isEmpty());
    }

    @Test
    public void multiFragmentMessage() {
        Collector<AISMessage05> c = new Collector<>(AISMessage05.class);
        c.sentenceRead(AIS_05_1);
        assertTrue(c.received.isEmpty());
        c.sentenceRead(AIS_05_2);
        assertEquals(1, c.received.size());
    }

    @Test
    public void firstFragmentClearsQueue() {
        Collector<AISMessage05> c = new Collector<>(AISMessage05.class);
        c.sentenceRead(AIS_05_1);
        c.sentenceRead(AIS_05_1);
        c.sentenceRead(AIS_05_2);
        assertEquals(1, c.received.size());
    }

    @Test
    public void incorrectOrderIgnored() {
        Collector<AISMessage05> c = new Collector<>(AISMessage05.class);
        c.sentenceRead(AIS_05_2);
        c.sentenceRead(AIS_05_2);
        assertTrue(c.received.isEmpty());
    }

    @Test
    public void unsupportedMessageTypeIgnored() {
        AISSentence s = (AISSentence) sf.createParser("!AIVDM,1,1,,A,85MwpKiKf:MPiQa:ofV@v2mQTfB26oEtbEVqh4j1QDQPHjhpkNJ3,0");
        Collector<AISMessage> c = new Collector<>(AISMessage.class);
        c.sentenceRead(s);
        assertTrue(c.received.isEmpty());
    }
}
