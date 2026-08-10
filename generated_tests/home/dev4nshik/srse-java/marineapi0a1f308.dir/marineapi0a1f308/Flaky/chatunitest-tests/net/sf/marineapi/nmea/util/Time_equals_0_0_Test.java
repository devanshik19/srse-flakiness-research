package net.sf.marineapi.nmea.util;

import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

public class Time_equals_0_0_Test {

    private Time time1;

    private Time time2;

    @BeforeEach
    public void setUp() {
        time1 = new Time(10, 30, 45.0, 2, 15);
        time2 = new Time(10, 30, 45.0, 2, 15);
    }

    @Test
    public void testEquals_SameObject() {
        assertTrue(time1.equals(time1));
    }

    @Test
    public void testEquals_NullObject() {
        assertFalse(time1.equals(null));
    }

    @Test
    public void testEquals_DifferentClass() {
        assertFalse(time1.equals("NotATimeObject"));
    }

    @Test
    public void testEquals_EqualTimeObjects() {
        assertTrue(time1.equals(time2));
    }

    @Test
    public void testEquals_DifferentHour() throws Exception {
        Method setHour = Time.class.getDeclaredMethod("setHour", int.class);
        setHour.setAccessible(true);
        setHour.invoke(time2, 11);
        assertFalse(time1.equals(time2));
    }

    @Test
    public void testEquals_DifferentMinutes() throws Exception {
        Method setMinutes = Time.class.getDeclaredMethod("setMinutes", int.class);
        setMinutes.setAccessible(true);
        setMinutes.invoke(time2, 31);
        assertFalse(time1.equals(time2));
    }

    @Test
    public void testEquals_DifferentSeconds() throws Exception {
        Method setSeconds = Time.class.getDeclaredMethod("setSeconds", double.class);
        setSeconds.setAccessible(true);
        setSeconds.invoke(time2, 46.0);
        assertFalse(time1.equals(time2));
    }

    @Test
    public void testEquals_DifferentOffsetHours() throws Exception {
        Method setOffsetHours = Time.class.getDeclaredMethod("setOffsetHours", int.class);
        setOffsetHours.setAccessible(true);
        setOffsetHours.invoke(time2, 3);
        assertFalse(time1.equals(time2));
    }

    @Test
    public void testEquals_DifferentOffsetMinutes() throws Exception {
        Method setOffsetMinutes = Time.class.getDeclaredMethod("setOffsetMinutes", int.class);
        setOffsetMinutes.setAccessible(true);
        setOffsetMinutes.invoke(time2, 16);
        assertFalse(time1.equals(time2));
    }
}
