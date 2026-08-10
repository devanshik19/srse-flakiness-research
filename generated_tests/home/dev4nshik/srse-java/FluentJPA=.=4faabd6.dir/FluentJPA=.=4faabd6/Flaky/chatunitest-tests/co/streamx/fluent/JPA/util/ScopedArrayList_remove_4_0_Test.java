package co.streamx.fluent.JPA.util;

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

public class ScopedArrayList_remove_4_0_Test {

    @Test
    public void testRemove() {
        List<Object> upperList = new ArrayList<>();
        ScopedArrayList<Object> scopedArrayList = new ScopedArrayList<>(upperList);
        try {
            Method removeMethod = ScopedArrayList.class.getDeclaredMethod("remove", Object.class);
            removeMethod.setAccessible(true);
            UnsupportedOperationException exception = assertThrows(UnsupportedOperationException.class, () -> {
                removeMethod.invoke(scopedArrayList, new Object());
            });
            assertNotNull(exception);
        } catch (Exception e) {
            fail("Exception should not have been thrown: " + e.getMessage());
        }
    }
}
