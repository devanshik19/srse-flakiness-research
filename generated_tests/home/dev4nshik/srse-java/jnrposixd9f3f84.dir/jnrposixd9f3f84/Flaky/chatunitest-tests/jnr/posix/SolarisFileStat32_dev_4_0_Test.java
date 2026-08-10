package jnr.posix;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import jnr.ffi.Memory;
import jnr.ffi.Pointer;
import jnr.ffi.Runtime;
import jnr.posix.NativePOSIX;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import jnr.ffi.StructLayout;

@ExtendWith(MockitoExtension.class)
public class SolarisFileStat32_dev_4_0_Test {

    private SolarisFileStat32 solarisFileStat32;

    private static Runtime runtime;

    private static Pointer memory;

    @BeforeAll
    public static void setupClass() {
        runtime = Runtime.getSystemRuntime();
        // Allocate memory for testing
        memory = Memory.allocate(runtime, 8);
    }

    @BeforeEach
    public void setUp() {
        NativePOSIX posix = mock(NativePOSIX.class);
        when(posix.getRuntime()).thenReturn(runtime);
        solarisFileStat32 = new SolarisFileStat32(posix);
    }

    @Test
    public void testDev() throws Exception {
        // Use reflection to access the private Layout class and its field
        Field layoutField = SolarisFileStat32.class.getDeclaredField("layout");
        layoutField.setAccessible(true);
        Object layout = layoutField.get(solarisFileStat32);
        // Use reflection to access the private st_dev field
        Field st_devField = layout.getClass().getDeclaredField("st_dev");
        st_devField.setAccessible(true);
        Object st_dev = st_devField.get(layout);
        // Use reflection to access the get method of the st_dev field
        Method getMethod = st_dev.getClass().getDeclaredMethod("get", Pointer.class);
        getMethod.setAccessible(true);
        // Set a value in the allocated memory for testing
        memory.putLong(0, 12345L);
        // Invoke the dev() method
        long devValue = solarisFileStat32.dev();
        // Verify the result
        assertEquals(12345L, devValue);
    }
}
