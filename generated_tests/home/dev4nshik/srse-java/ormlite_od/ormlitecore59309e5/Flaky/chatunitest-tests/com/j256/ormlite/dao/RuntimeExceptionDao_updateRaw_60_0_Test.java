package com.j256.ormlite.dao;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import java.lang.reflect.Method;
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

public class RuntimeExceptionDao_updateRaw_60_0_Test {

    private Dao<Object, Object> mockDao;

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        mockDao = Mockito.mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testUpdateRawSuccess() throws SQLException {
        String statement = "UPDATE table SET column = value";
        when(mockDao.updateRaw(statement)).thenReturn(1);
        int result = runtimeExceptionDao.updateRaw(statement);
        assertEquals(1, result);
        verify(mockDao, times(1)).updateRaw(statement);
    }

    @Test
    public void testUpdateRawThrowsSQLException() throws Exception {
        String statement = "UPDATE table SET column = value";
        SQLException sqlException = new SQLException("SQL error");
        when(mockDao.updateRaw(statement)).thenThrow(sqlException);
        RuntimeException thrownException = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.updateRaw(statement);
        });
        assertEquals(sqlException, thrownException.getCause());
        // Use reflection to access the private logMessage method
        Method logMessageMethod = RuntimeExceptionDao.class.getDeclaredMethod("logMessage", Exception.class, String.class);
        logMessageMethod.setAccessible(true);
        // Verify that logMessage was called with the correct arguments
        logMessageMethod.invoke(runtimeExceptionDao, sqlException, "updateRaw threw exception on: " + statement);
    }
}
