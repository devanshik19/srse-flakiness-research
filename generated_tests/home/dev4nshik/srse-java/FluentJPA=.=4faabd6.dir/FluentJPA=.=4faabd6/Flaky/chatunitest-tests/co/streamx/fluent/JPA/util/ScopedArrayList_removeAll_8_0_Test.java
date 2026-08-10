package co.streamx.fluent.JPA.util;

import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import lombok.RequiredArgsConstructor;

public class ScopedArrayList_removeAll_8_0_Test {

    private ScopedArrayList scopedArrayList;

    @BeforeEach
    public void setUp() throws Exception {
        Constructor<?> constructor = ScopedArrayList.class.getDeclaredConstructor(List.class);
        constructor.setAccessible(true);
        scopedArrayList = (ScopedArrayList) constructor.newInstance(new ArrayList<>());
    }

    @Test
    public void testRemoveAllThrowsUnsupportedOperationException() throws Exception {
        Method removeAllMethod = ScopedArrayList.class.getDeclaredMethod("removeAll", Collection.class);
        removeAllMethod.setAccessible(true);
        assertThrows(UnsupportedOperationException.class, () -> {
            removeAllMethod.invoke(scopedArrayList, new ArrayList<>());
        });
    }
}
