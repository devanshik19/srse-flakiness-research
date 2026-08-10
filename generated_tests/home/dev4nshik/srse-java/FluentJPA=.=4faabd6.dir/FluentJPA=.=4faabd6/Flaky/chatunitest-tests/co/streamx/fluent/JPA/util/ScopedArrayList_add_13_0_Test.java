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

public class ScopedArrayList_add_13_0_Test {

    private ScopedArrayList scopedArrayList;

    private List<Object> upperList;

    @BeforeEach
    public void setUp() throws NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {
        upperList = new ArrayList<>();
        Constructor<ScopedArrayList> constructor = ScopedArrayList.class.getDeclaredConstructor(List.class);
        constructor.setAccessible(true);
        scopedArrayList = constructor.newInstance(upperList);
    }

    @Test
    public void testAddMethodThrowsUnsupportedOperationException() throws NoSuchMethodException, IllegalAccessException, InvocationTargetException {
        Method addMethod = ScopedArrayList.class.getDeclaredMethod("add", int.class, Object.class);
        addMethod.setAccessible(true);
        assertThrows(UnsupportedOperationException.class, () -> {
            addMethod.invoke(scopedArrayList, 0, new Object());
        });
    }
}
