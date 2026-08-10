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

class ScopedArrayList_indexOf_15_0_Test {

    private ScopedArrayList<String> scopedArrayList;

    private List<String> upperList;

    @BeforeEach
    void setUp() {
        upperList = new ArrayList<>();
        scopedArrayList = new ScopedArrayList<>(upperList);
    }

    @Test
    void testIndexOfThrowsUnsupportedOperationException() {
        try {
            Method indexOfMethod = ScopedArrayList.class.getDeclaredMethod("indexOf", Object.class);
            indexOfMethod.setAccessible(true);
            assertThrows(UnsupportedOperationException.class, () -> {
                indexOfMethod.invoke(scopedArrayList, "test");
            });
        } catch (Exception e) {
            fail("Exception should not have been thrown: " + e.getMessage());
        }
    }
}
