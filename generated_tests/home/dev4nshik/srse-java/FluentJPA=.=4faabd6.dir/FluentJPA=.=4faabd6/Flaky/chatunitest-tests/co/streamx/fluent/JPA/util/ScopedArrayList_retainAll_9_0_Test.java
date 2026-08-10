package co.streamx.fluent.JPA.util;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Arrays;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import lombok.RequiredArgsConstructor;

public class ScopedArrayList_retainAll_9_0_Test {

    private ScopedArrayList scopedArrayList;

    private List<Object> upperList;

    @BeforeEach
    public void setUp() throws Exception {
        upperList = new ArrayList<>(Arrays.asList("A", "B", "C"));
        Constructor<?> constructor = ScopedArrayList.class.getDeclaredConstructor(List.class);
        constructor.setAccessible(true);
        scopedArrayList = (ScopedArrayList) constructor.newInstance(upperList);
    }

    @Test
    public void testRetainAllThrowsUnsupportedOperationException() {
        Collection<Object> collection = Arrays.asList("A", "B");
        Exception exception = assertThrows(UnsupportedOperationException.class, () -> {
            Method method = ScopedArrayList.class.getDeclaredMethod("retainAll", Collection.class);
            method.setAccessible(true);
            method.invoke(scopedArrayList, collection);
        });
        String expectedMessage = "UnsupportedOperationException";
        String actualMessage = exception.getClass().getSimpleName();
        assertTrue(actualMessage.contains(expectedMessage));
    }
}
