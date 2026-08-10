package net.sf.marineapi.nmea.util;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
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

class Time_hashCode_7_0_Test {

    @Test
    void testHashCode() throws Exception {
        // Create a Time object using reflection
        Constructor<?> constructor = Time.class.getDeclaredConstructor();
        constructor.setAccessible(true);
        Time time = (Time) constructor.newInstance();
        // Set private fields using reflection
        Field hourField = Time.class.getDeclaredField("hour");
        hourField.setAccessible(true);
        hourField.setInt(time, 12);
        Field minutesField = Time.class.getDeclaredField("minutes");
        minutesField.setAccessible(true);
        minutesField.setInt(time, 30);
        Field secondsField = Time.class.getDeclaredField("seconds");
        secondsField.setAccessible(true);
        secondsField.setDouble(time, 45.5);
        // Invoke the hashCode method
        Method hashCodeMethod = Time.class.getDeclaredMethod("hashCode");
        hashCodeMethod.setAccessible(true);
        int hashCode = (int) hashCodeMethod.invoke(time);
        // Calculate expected hashCode
        String s = String.format("%2d%2d%2f", 12, 30, 45.5);
        int expectedHashCode = s.hashCode();
        // Assert the hashCode is as expected
        assertEquals(expectedHashCode, hashCode);
    }
}
