package net.sf.marineapi.nmea.util;

import java.lang.reflect.Method;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;

public class Time_toDate_14_0_Test {

    private Time time;

    @BeforeEach
    public void setUp() {
        time = new Time();
    }

    @Test
    public void testToDate() throws Exception {
        // Set up a specific time
        time.setHour(10);
        time.setMinutes(30);
        time.setSeconds(45.123);
        // Create a date to pass to the toDate method
        GregorianCalendar calendar = new GregorianCalendar(2023, Calendar.OCTOBER, 10, 0, 0, 0);
        Date date = calendar.getTime();
        // Use reflection to access the private toDate method
        Method toDateMethod = Time.class.getDeclaredMethod("toDate", Date.class);
        toDateMethod.setAccessible(true);
        // Invoke the toDate method
        Date result = (Date) toDateMethod.invoke(time, date);
        // Create a calendar to check the result
        calendar.setTime(result);
        // Assert the time is correctly set
        assertEquals(10, calendar.get(Calendar.HOUR_OF_DAY));
        assertEquals(30, calendar.get(Calendar.MINUTE));
        assertEquals(45, calendar.get(Calendar.SECOND));
        assertEquals(123, calendar.get(Calendar.MILLISECOND));
    }
}
