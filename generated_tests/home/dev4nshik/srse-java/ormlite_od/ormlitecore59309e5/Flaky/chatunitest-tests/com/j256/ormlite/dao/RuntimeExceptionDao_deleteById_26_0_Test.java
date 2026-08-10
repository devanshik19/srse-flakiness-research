package com.j256.ormlite.dao;

import java.sql.SQLException;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Callable;
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

public class RuntimeExceptionDao_deleteById_26_0_Test {

    private RuntimeExceptionDao<Object, Integer> runtimeExceptionDao;

    private Dao<Object, Integer> mockDao;

    @BeforeEach
    public void setUp() {
        mockDao = Mockito.mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testDeleteByIdSuccess() throws SQLException {
        Integer id = 1;
        when(mockDao.deleteById(id)).thenReturn(1);
        int result = runtimeExceptionDao.deleteById(id);
        assertEquals(1, result);
        verify(mockDao, times(1)).deleteById(id);
    }

    @Test
    public void testDeleteByIdThrowsSQLException() throws SQLException {
        Integer id = 1;
        when(mockDao.deleteById(id)).thenThrow(new SQLException("SQL Exception"));
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.deleteById(id);
        });
        assertEquals(SQLException.class, exception.getCause().getClass());
        verify(mockDao, times(1)).deleteById(id);
    }

    @Test
    public void testLogMessagePrivateMethod() throws Exception {
        // Access private method using reflection
        java.lang.reflect.Method method = RuntimeExceptionDao.class.getDeclaredMethod("logMessage", Exception.class, String.class);
        method.setAccessible(true);
        Exception exception = new Exception("Test Exception");
        String message = "Test message";
        // Invoke private method
        method.invoke(runtimeExceptionDao, exception, message);
        // Verify that the logger was called (mocking or verifying logger calls would require additional setup)
    }
}
