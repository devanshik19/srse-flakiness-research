package co.streamx.fluent.JPA.util;

import java.lang.reflect.Constructor;
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

public class ScopedArrayList_remove_14_0_Test {

    private ScopedArrayList<Object> scopedArrayList;

    private List<Object> upperList;

    @BeforeEach
    public void setUp() throws Exception {
        upperList = new ArrayList<>();
        Constructor<ScopedArrayList> constructor = ScopedArrayList.class.getDeclaredConstructor(List.class);
        constructor.setAccessible(true);
        scopedArrayList = constructor.newInstance(upperList);
    }

    @Test
    public void testRemoveByIndex() {
        try {
            Method removeMethod = ScopedArrayList.class.getDeclaredMethod("remove", int.class);
            removeMethod.setAccessible(true);
            assertThrows(UnsupportedOperationException.class, () -> removeMethod.invoke(scopedArrayList, 0));
        } catch (Exception e) {
            fail("Exception occurred during reflection: " + e.getMessage());
        }
    }
}
