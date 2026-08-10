package co.streamx.fluent.JPA.util;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.Collection;
import lombok.RequiredArgsConstructor;

public class ScopedArrayList_clear_10_0_Test {

    @Test
    public void testClearThrowsUnsupportedOperationException() throws NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {
        // Use reflection to access the constructor of ScopedArrayList
        Constructor<ScopedArrayList> constructor = ScopedArrayList.class.getDeclaredConstructor(List.class);
        constructor.setAccessible(true);
        // Create an instance of ScopedArrayList with an empty upper list
        ScopedArrayList scopedArrayList = constructor.newInstance(new ArrayList<>());
        // Use reflection to access the clear method
        Method clearMethod = ScopedArrayList.class.getDeclaredMethod("clear");
        clearMethod.setAccessible(true);
        // Assert that calling clear throws UnsupportedOperationException
        assertThrows(UnsupportedOperationException.class, () -> clearMethod.invoke(scopedArrayList));
    }
}
