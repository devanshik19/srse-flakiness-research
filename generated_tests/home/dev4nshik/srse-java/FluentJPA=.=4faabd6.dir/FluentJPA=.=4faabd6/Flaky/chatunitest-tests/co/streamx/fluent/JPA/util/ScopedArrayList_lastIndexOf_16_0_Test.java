package co.streamx.fluent.JPA.util;

import java.lang.reflect.Field;
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

public class ScopedArrayList_lastIndexOf_16_0_Test {

    private ScopedArrayList<String> scopedArrayList;

    private List<String> upperList;

    @BeforeEach
    public void setUp() throws Exception {
        upperList = new ArrayList<>();
        upperList.add("first");
        upperList.add("second");
        upperList.add("third");
        scopedArrayList = new ScopedArrayList<>(upperList);
    }

    @Test
    public void testGetUpper() throws Exception {
        Method getUpperMethod = ScopedArrayList.class.getDeclaredMethod("getUpper");
        getUpperMethod.setAccessible(true);
        List<String> result = (List<String>) getUpperMethod.invoke(scopedArrayList);
        assertEquals(upperList, result);
    }
}
