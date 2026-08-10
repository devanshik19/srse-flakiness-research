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

public class RuntimeExceptionDao_executeRawNoArgs_59_0_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    private Dao<Object, Object> mockDao;

    @BeforeEach
    public void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testExecuteRawNoArgsSuccess() throws SQLException {
        String statement = "DELETE FROM table_name";
        when(mockDao.executeRawNoArgs(statement)).thenReturn(1);
        int result = runtimeExceptionDao.executeRawNoArgs(statement);
        assertEquals(1, result);
        verify(mockDao, times(1)).executeRawNoArgs(statement);
    }

    @Test
    public void testExecuteRawNoArgsThrowsSQLException() throws Exception {
        String statement = "DELETE FROM table_name";
        when(mockDao.executeRawNoArgs(statement)).thenThrow(new SQLException("SQL error"));
        SQLException thrownException = assertThrows(SQLException.class, () -> {
            runtimeExceptionDao.executeRawNoArgs(statement);
        });
        // Verify that the SQLException is wrapped in a RuntimeException
        try {
            runtimeExceptionDao.executeRawNoArgs(statement);
        } catch (RuntimeException e) {
            assertTrue(e.getCause() instanceof SQLException);
            assertEquals("SQL error", e.getCause().getMessage());
        }
        verify(mockDao, times(2)).executeRawNoArgs(statement);
    }
}
