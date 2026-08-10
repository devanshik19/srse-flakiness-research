package co.streamx.fluent.JPA.util;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
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

public class ScopedArrayList_size_1_0_Test {

    private ScopedArrayList<String> scopedArrayList;

    private List<String> upperList;

    @BeforeEach
    public void setUp() throws Exception {
        upperList = new ArrayList<>();
        scopedArrayList = new ScopedArrayList<>(upperList);
        // Adding elements to the upper list
        upperList.add("element1");
        upperList.add("element2");
        // Using reflection to access the private 'upper' field
        Field upperField = ScopedArrayList.class.getDeclaredField("upper");
        upperField.setAccessible(true);
        upperField.set(scopedArrayList, upperList);
    }

    @Test
    public void testSize() {
        // Adding elements to the scopedArrayList
        scopedArrayList.add("element3");
        scopedArrayList.add("element4");
        // Expected size is the sum of elements in the upper list and scopedArrayList
        int expectedSize = upperList.size() + 2;
        assertEquals(expectedSize, scopedArrayList.size());
    }
}
