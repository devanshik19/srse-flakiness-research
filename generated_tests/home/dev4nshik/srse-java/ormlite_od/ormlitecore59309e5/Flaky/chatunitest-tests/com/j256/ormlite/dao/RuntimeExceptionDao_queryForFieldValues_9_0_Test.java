package com.j256.ormlite.dao;

import java.sql.SQLException;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import com.j256.ormlite.stmt.PreparedQuery;
import com.j256.ormlite.support.ConnectionSource;
import com.j256.ormlite.table.ObjectFactory;
import com.j256.ormlite.table.TableInfo;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Collection;
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
import com.j256.ormlite.stmt.PreparedUpdate;
import com.j256.ormlite.stmt.QueryBuilder;
import com.j256.ormlite.stmt.UpdateBuilder;
import com.j256.ormlite.support.DatabaseConnection;
import com.j256.ormlite.support.DatabaseResults;
import com.j256.ormlite.table.DatabaseTableConfig;

@ExtendWith(MockitoExtension.class)
public class RuntimeExceptionDao_queryForFieldValues_9_0_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    private Dao<Object, Object> mockDao;

    @BeforeEach
    public void setUp() {
        mockDao = Mockito.mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testQueryForFieldValuesSuccess() throws SQLException {
        Map<String, Object> fieldValues = Collections.singletonMap("key", "value");
        List<Object> expectedList = Collections.singletonList(new Object());
        when(mockDao.queryForFieldValues(fieldValues)).thenReturn(expectedList);
        List<Object> result = runtimeExceptionDao.queryForFieldValues(fieldValues);
        assertEquals(expectedList, result);
        verify(mockDao).queryForFieldValues(fieldValues);
    }

    @Test
    public void testQueryForFieldValuesSQLException() throws SQLException {
        Map<String, Object> fieldValues = Collections.singletonMap("key", "value");
        when(mockDao.queryForFieldValues(fieldValues)).thenThrow(new SQLException("Test exception"));
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.queryForFieldValues(fieldValues);
        });
        assertEquals(SQLException.class, exception.getCause().getClass());
        assertEquals("Test exception", exception.getCause().getMessage());
        verify(mockDao).queryForFieldValues(fieldValues);
    }

    @Test
    public void testLogMessage() throws Exception {
        Exception testException = new Exception("Test Exception");
        String testMessage = "Test Message";
        // Use reflection to invoke the private method
        java.lang.reflect.Method method = RuntimeExceptionDao.class.getDeclaredMethod("logMessage", Exception.class, String.class);
        method.setAccessible(true);
        // No exception should be thrown
        method.invoke(runtimeExceptionDao, testException, testMessage);
    }
}
