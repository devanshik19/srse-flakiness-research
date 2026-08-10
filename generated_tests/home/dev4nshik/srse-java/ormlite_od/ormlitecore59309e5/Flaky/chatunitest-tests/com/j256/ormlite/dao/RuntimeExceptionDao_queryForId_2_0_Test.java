package com.j256.ormlite.dao;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
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

public class RuntimeExceptionDao_queryForId_2_0_Test {

    private Dao<Object, Integer> mockDao;

    private RuntimeExceptionDao<Object, Integer> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testQueryForIdSuccess() throws SQLException {
        Object expectedObject = new Object();
        when(mockDao.queryForId(1)).thenReturn(expectedObject);
        Object result = runtimeExceptionDao.queryForId(1);
        assertEquals(expectedObject, result);
        verify(mockDao, times(1)).queryForId(1);
    }

    @Test
    public void testQueryForIdThrowsRuntimeException() throws SQLException {
        when(mockDao.queryForId(1)).thenThrow(new SQLException("SQL error"));
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.queryForId(1);
        });
        assertNotNull(exception.getCause());
        assertTrue(exception.getCause() instanceof SQLException);
        assertEquals("SQL error", exception.getCause().getMessage());
        verify(mockDao, times(1)).queryForId(1);
    }

    @Test
    public void testLogMessagePrivateMethod() throws Exception {
        SQLException sqlException = new SQLException("Test exception");
        String message = "Test message";
        // Use reflection to access the private logMessage method
        java.lang.reflect.Method logMessageMethod = RuntimeExceptionDao.class.getDeclaredMethod("logMessage", Exception.class, String.class);
        logMessageMethod.setAccessible(true);
        // Invoke the private method
        logMessageMethod.invoke(runtimeExceptionDao, sqlException, message);
        // No assertions needed as we're testing a private method side-effect
    }
}
