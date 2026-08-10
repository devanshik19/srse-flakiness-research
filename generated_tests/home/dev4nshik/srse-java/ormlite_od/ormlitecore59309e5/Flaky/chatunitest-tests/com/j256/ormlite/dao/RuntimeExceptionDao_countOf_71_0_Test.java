package com.j256.ormlite.dao;

import java.sql.SQLException;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
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

class RuntimeExceptionDao_countOf_71_0_Test {

    private Dao<Object, Object> mockDao;

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @BeforeEach
    void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    void testCountOfSuccess() throws SQLException {
        // Arrange
        long expectedCount = 42L;
        when(mockDao.countOf()).thenReturn(expectedCount);
        // Act
        long actualCount = runtimeExceptionDao.countOf();
        // Assert
        assertEquals(expectedCount, actualCount);
        verify(mockDao, times(1)).countOf();
    }

    @Test
    void testCountOfSQLException() throws Exception {
        // Arrange
        SQLException sqlException = new SQLException("SQL error");
        when(mockDao.countOf()).thenThrow(sqlException);
        // Act & Assert
        RuntimeException thrown = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.countOf();
        });
        assertSame(sqlException, thrown.getCause());
        verify(mockDao, times(1)).countOf();
    }

    @Test
    void testLogMessagePrivateMethod() throws Exception {
        // Arrange
        SQLException sqlException = new SQLException("SQL error");
        String logMessage = "countOf threw exception";
        // Act
        try {
            runtimeExceptionDao.countOf();
        } catch (RuntimeException e) {
            // Expected
        }
        // Use reflection to invoke the private logMessage method
        java.lang.reflect.Method method = RuntimeExceptionDao.class.getDeclaredMethod("logMessage", Exception.class, String.class);
        method.setAccessible(true);
        // Assert
        method.invoke(runtimeExceptionDao, sqlException, logMessage);
    }
}
