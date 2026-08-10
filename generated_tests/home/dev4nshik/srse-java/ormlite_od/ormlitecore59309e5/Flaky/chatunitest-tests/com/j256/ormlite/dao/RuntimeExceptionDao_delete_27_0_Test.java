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
public class RuntimeExceptionDao_delete_27_0_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    private Dao<Object, Object> mockDao;

    @BeforeEach
    public void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testDeleteSuccess() throws SQLException {
        Collection<Object> data = Arrays.asList(new Object(), new Object());
        when(mockDao.delete(data)).thenReturn(2);
        int result = runtimeExceptionDao.delete(data);
        assertEquals(2, result);
        verify(mockDao).delete(data);
    }

    @Test
    public void testDeleteThrowsSQLException() throws SQLException {
        Collection<Object> data = Arrays.asList(new Object(), new Object());
        when(mockDao.delete(data)).thenThrow(new SQLException("Test exception"));
        Exception exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.delete(data);
        });
        assertTrue(exception.getCause() instanceof SQLException);
        assertEquals("Test exception", exception.getCause().getMessage());
        // Verify that logMessage was called with correct parameters
        ArgumentCaptor<Exception> exceptionCaptor = ArgumentCaptor.forClass(Exception.class);
        ArgumentCaptor<String> messageCaptor = ArgumentCaptor.forClass(String.class);
        verifyPrivateLogMessage(exceptionCaptor, messageCaptor, data);
    }

    private void verifyPrivateLogMessage(ArgumentCaptor<Exception> exceptionCaptor, ArgumentCaptor<String> messageCaptor, Collection<Object> data) {
        try {
            java.lang.reflect.Method method = RuntimeExceptionDao.class.getDeclaredMethod("logMessage", Exception.class, String.class);
            method.setAccessible(true);
            method.invoke(runtimeExceptionDao, new SQLException("Test exception"), "delete threw exception on: " + data);
            assertEquals("delete threw exception on: " + data, messageCaptor.getValue());
        } catch (Exception e) {
            fail("Method logMessage should exist and be invokable");
        }
    }
}
