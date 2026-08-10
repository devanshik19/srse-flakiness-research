package co.streamx.fluent.JPA.util;

import org.junit.jupiter.api.function.Executable;
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

public class ScopedArrayList_addAll_6_0_Test {

    @Test
    public void testAddAll_UnsupportedOperationException() throws NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {
        // Arrange
        Constructor<ScopedArrayList> constructor = ScopedArrayList.class.getDeclaredConstructor(List.class);
        constructor.setAccessible(true);
        List<Object> upperList = new ArrayList<>();
        ScopedArrayList scopedArrayList = constructor.newInstance(upperList);
        Method addAllMethod = ScopedArrayList.class.getDeclaredMethod("addAll", Collection.class);
        addAllMethod.setAccessible(true);
        Collection<Object> collectionToAdd = new ArrayList<>();
        // Act & Assert
        Executable executable = () -> addAllMethod.invoke(scopedArrayList, collectionToAdd);
        InvocationTargetException exception = assertThrows(InvocationTargetException.class, executable, "Expected InvocationTargetException due to UnsupportedOperationException");
        assertTrue(exception.getCause() instanceof UnsupportedOperationException, "Expected cause to be UnsupportedOperationException");
    }
}
