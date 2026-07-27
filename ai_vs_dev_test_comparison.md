# AI-Generated vs Developer Test — Same Method Comparison

## Test under comparison
- Method under test: `Time.toString()`
- Class: `net.sf.marineapi.nmea.util.Time`
- Project: ktuukkan/marine-api
- Commit: 0a1f308
- Source: https://github.com/ktuukkan/marine-api
- AI test file: `Flaky/chatunitest-tests/net/sf/marineapi/nmea/util/Time_toString_15_0_Test.java` (ChatUniTest, gpt-4o)
- Developer test file: `Flaky/src/backup/net/sf/marineapi/nmea/util/TimeTest.java`

This is the one class out of 36 where the AI-generated test came back flaky (17/100 runs). The developer test for the same method is not flaky. So this is a direct AI-flaky vs developer-non-flaky comparison on the same method.

## Developer test (for toString)
```java
@Test
public void testFormatTimeWithDecimals() {
    Time t = new Time(1, 2, 3.456);
    assertEquals("010203.456", t.toString());
}

@Test
public void testFormatTimeWithOneDecimal() {
    Time t = new Time(1, 2, 3.4);
    assertEquals("010203.400", t.toString());
}
```

## AI-generated test (for toString)
```java
@BeforeEach
public void setUp() {
    time = new Time();
}

@Test
public void testToStringDefaultConstructor() {
    try {
        Method getHourMethod = Time.class.getDeclaredMethod("getHour");
        Method getMinutesMethod = Time.class.getDeclaredMethod("getMinutes");
        Method getSecondsMethod = Time.class.getDeclaredMethod("getSeconds");
        getHourMethod.setAccessible(true);
        getMinutesMethod.setAccessible(true);
        getSecondsMethod.setAccessible(true);
        int hour = (int) getHourMethod.invoke(time);
        int minutes = (int) getMinutesMethod.invoke(time);
        double seconds = (double) getSecondsMethod.invoke(time);
        String expected = String.format("%02d%02d%05.3f", hour, minutes, seconds);
        assertEquals(expected, time.toString());
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

## Differences

1. **Input.** The developer fixes the time with `new Time(1, 2, 3.456)` so the test is deterministic. The AI uses `new Time()`, the no-arg constructor, which reads the system clock. The input changes every run. This is the root cause of the flakiness.

2. **Expected value.** The developer hardcodes the expected string (`"010203.456"`). The AI recomputes the expected value at runtime with its own `String.format("%02d%02d%05.3f", ...)`. It doesn't check against a known answer, it re-derives one, so it's really testing its own formatting logic against the code's, not the code against a fixed truth.

3. **Reflection.** The AI reaches into private methods (`getDeclaredMethod("getHour").invoke(...)`) to build the expected value. The developer only uses the public API. The reflection is fragile and unnecessary.

4. **Swallowed failures.** The AI wraps everything in try/catch and only calls `printStackTrace()` on error, so an exception passes the test instead of failing it. The developer test has no such catch.
