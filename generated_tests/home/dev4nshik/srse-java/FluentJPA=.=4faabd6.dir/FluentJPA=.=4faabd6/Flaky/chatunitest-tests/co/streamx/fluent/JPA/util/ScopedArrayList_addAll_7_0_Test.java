package co.streamx.fluent.JPA.util;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
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

public class ScopedArrayList_addAll_7_0_Test {

    private ScopedArrayList<Object> scopedArrayList;

    private List<Object> upperList;

    @BeforeEach
    public void setUp() throws NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {
        upperList = new ArrayList<>();
        Constructor<ScopedArrayList> constructor = ScopedArrayList.class.getDeclaredConstructor(List.class);
        constructor.setAccessible(true);
        scopedArrayList = constructor.newInstance(upperList);
    }

    @Test
    public void testAddAllWithUnsupportedOperationException() {
        Collection<Object> collection = new ArrayList<>();
        collection.add(new Object());
        assertThrows(UnsupportedOperationException.class, () -> {
            Method addAllMethod = ScopedArrayList.class.getDeclaredMethod("addAll", int.class, Collection.class);
            addAllMethod.setAccessible(true);
            addAllMethod.invoke(scopedArrayList, 0, collection);
        });
    }
}
