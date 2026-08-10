package com.j256.ormlite.dao;

import java.sql.SQLException;
import java.util.Arrays;
import java.util.Collection;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Callable;
import java.lang.reflect.InvocationTargetException;
import com.j256.ormlite.field.DataType;
import com.j256.ormlite.field.FieldType;
import com.j256.ormlite.logger.Level;
import com.j256.ormlite.logger.Logger;
import com.j256.ormlite.logger.LoggerFactory;
import com.j256.ormlite.misc.Supplier;
import com.j256.ormlite.stmt.ArgumentHolder;
import com.j256.ormlite.stmt.DeleteBuilder;
import com.j256.ormlite.stmt.GenericRowMapper;
import com.j256.ormlite.stmt.PreparedDelete;
import com.j256.ormlite.stmt.PreparedQuery;
import com.j256.ormlite.stmt.PreparedUpdate;
import com.j256.ormlite.stmt.QueryBuilder;
import com.j256.ormlite.stmt.UpdateBuilder;
import com.j256.ormlite.support.ConnectionSource;
import com.j256.ormlite.support.DatabaseConnection;
import com.j256.ormlite.support.DatabaseResults;
import com.j256.ormlite.table.DatabaseTableConfig;
import com.j256.ormlite.table.ObjectFactory;
import com.j256.ormlite.table.TableInfo;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
public class RuntimeExceptionDao_deleteIds_28_0_Test {

    private Dao<Object, Integer> mockDao;

    private RuntimeExceptionDao<Object, Integer> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testDeleteIdsSuccess() throws SQLException {
        Collection<Integer> ids = Arrays.asList(1, 2, 3);
        when(mockDao.deleteIds(ids)).thenReturn(3);
        int result = runtimeExceptionDao.deleteIds(ids);
        assertEquals(3, result);
        verify(mockDao, times(1)).deleteIds(ids);
    }

    @Test
    public void testDeleteIdsSQLException() throws SQLException {
        Collection<Integer> ids = Arrays.asList(1, 2, 3);
        when(mockDao.deleteIds(ids)).thenThrow(new SQLException("Delete failed"));
        Exception exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.deleteIds(ids);
        });
        assertTrue(exception.getCause() instanceof SQLException);
        assertEquals("Delete failed", exception.getCause().getMessage());
        // Use reflection to access the private logMessage method
        try {
            java.lang.reflect.Method logMessageMethod = RuntimeExceptionDao.class.getDeclaredMethod("logMessage", Exception.class, String.class);
            logMessageMethod.setAccessible(true);
            logMessageMethod.invoke(runtimeExceptionDao, exception.getCause(), "deleteIds threw exception on: " + ids);
        } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
            fail("Reflection failed: " + e.getMessage());
        }
    }
}
