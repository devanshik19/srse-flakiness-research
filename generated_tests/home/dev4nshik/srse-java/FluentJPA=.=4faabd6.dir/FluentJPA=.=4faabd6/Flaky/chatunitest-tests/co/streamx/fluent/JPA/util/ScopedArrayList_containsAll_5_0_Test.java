package co.streamx.fluent.JPA.util;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import lombok.RequiredArgsConstructor;

public class ScopedArrayList_containsAll_5_0_Test {

    private ScopedArrayList<Object> scopedArrayList;

    private List<Object> upperList;

    @BeforeEach
    public void setUp() throws NoSuchFieldException, IllegalAccessException, NoSuchMethodException, InvocationTargetException, InstantiationException {
        upperList = new ArrayList<>();
        Constructor<ScopedArrayList> constructor = ScopedArrayList.class.getDeclaredConstructor(List.class);
        constructor.setAccessible(true);
        scopedArrayList = constructor.newInstance(upperList);
    }

    @Test
    public void testContainsAll_emptyCollection() {
        Collection<Object> collection = new ArrayList<>();
        assertThrows(UnsupportedOperationException.class, () -> scopedArrayList.containsAll(collection));
    }

    @Test
    public void testContainsAll_nonEmptyCollection() {
        Collection<Object> collection = Arrays.asList("item1", "item2");
        assertThrows(UnsupportedOperationException.class, () -> scopedArrayList.containsAll(collection));
    }

    @Test
    public void testGetUpper() throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        Method getUpperMethod = ScopedArrayList.class.getDeclaredMethod("getUpper");
        getUpperMethod.setAccessible(true);
        List<Object> result = (List<Object>) getUpperMethod.invoke(scopedArrayList);
        assertSame(upperList, result);
    }
}
