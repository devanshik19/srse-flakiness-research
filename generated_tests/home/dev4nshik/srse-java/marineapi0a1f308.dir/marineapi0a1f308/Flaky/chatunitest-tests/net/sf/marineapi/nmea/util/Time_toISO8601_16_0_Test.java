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

public class Time_toISO8601_16_0_Test {

    private Time time;

    @BeforeEach
    public void setUp() {
        time = new Time();
    }

    @Test
    public void testToISO8601_DefaultConstructor() throws Exception {
        // Use reflection to invoke private methods
        Method getHourMethod = Time.class.getDeclaredMethod("getHour");
        Method getMinutesMethod = Time.class.getDeclaredMethod("getMinutes");
        Method getSecondsMethod = Time.class.getDeclaredMethod("getSeconds");
        Method getOffsetHoursMethod = Time.class.getDeclaredMethod("getOffsetHours");
        Method getOffsetMinutesMethod = Time.class.getDeclaredMethod("getOffsetMinutes");
        getHourMethod.setAccessible(true);
        getMinutesMethod.setAccessible(true);
        getSecondsMethod.setAccessible(true);
        getOffsetHoursMethod.setAccessible(true);
        getOffsetMinutesMethod.setAccessible(true);
        int hour = (int) getHourMethod.invoke(time);
        int minutes = (int) getMinutesMethod.invoke(time);
        int seconds = (int) Math.floor((double) getSecondsMethod.invoke(time));
        int offsetHours = (int) getOffsetHoursMethod.invoke(time);
        int offsetMinutes = (int) getOffsetMinutesMethod.invoke(time);
        String expected = String.format("%02d:%02d:%02d%+03d:%02d", hour, minutes, seconds, offsetHours, offsetMinutes);
        String actual = time.toISO8601();
        assertEquals(expected, actual);
    }

    @Test
    public void testToISO8601_WithParameters() {
        time = new Time(10, 15, 30.5, 2, 30);
        String expected = "10:15:30+02:30";
        String actual = time.toISO8601();
        assertEquals(expected, actual);
    }

    @Test
    public void testToISO8601_ZeroOffset() {
        time = new Time(23, 59, 59.999, 0, 0);
        String expected = "23:59:59+00:00";
        String actual = time.toISO8601();
        assertEquals(expected, actual);
    }

    @Test
    public void testToISO8601_NegativeOffset() {
        time = new Time(5, 45, 12.5, -3, -15);
        String expected = "05:45:12-03:15";
        String actual = time.toISO8601();
        assertEquals(expected, actual);
    }
}
