package co.streamx.fluent.JPA.util;

import co.streamx.fluent.JPA.util.ScopedArrayList;
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

public class ScopedArrayList_get_11_0_Test {

    @Test
    public void testGetMethodThrowsUnsupportedOperationException() throws NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {
        // Use reflection to create an instance of ScopedArrayList
        Constructor<ScopedArrayList> constructor = ScopedArrayList.class.getDeclaredConstructor(List.class);
        constructor.setAccessible(true);
        // Create a list to pass to the constructor
        List<Object> list = new ArrayList<>();
        ScopedArrayList scopedArrayList = constructor.newInstance(list);
        // Use reflection to access the private get method
        Method getMethod = ScopedArrayList.class.getDeclaredMethod("get", int.class);
        getMethod.setAccessible(true);
        // Assert that calling get method throws UnsupportedOperationException
        assertThrows(UnsupportedOperationException.class, () -> getMethod.invoke(scopedArrayList, 0));
    }
}
