package com.j256.ormlite.dao;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.stmt.ArgumentHolder;
import org.junit.jupiter.api.function.Executable;
import java.lang.reflect.Field;
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

public class RuntimeExceptionDao_queryRawValue_42_0_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    private Dao<Object, Object> mockDao;

    @BeforeEach
    public void setUp() throws Exception {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testQueryRawValueSuccess() throws Exception {
        String query = "SELECT * FROM table";
        ArgumentHolder[] arguments = new ArgumentHolder[] {};
        when(mockDao.queryRawValue(query, arguments)).thenReturn(42L);
        long result = runtimeExceptionDao.queryRawValue(query, arguments);
        assertEquals(42L, result);
        verify(mockDao, times(1)).queryRawValue(query, arguments);
    }

    @Test
    public void testQueryRawValueSQLException() throws Exception {
        String query = "SELECT * FROM table";
        ArgumentHolder[] arguments = new ArgumentHolder[] {};
        when(mockDao.queryRawValue(query, arguments)).thenThrow(new SQLException("SQL error"));
        Executable executable = () -> runtimeExceptionDao.queryRawValue(query, arguments);
        RuntimeException exception = assertThrows(RuntimeException.class, executable);
        assertEquals("java.sql.SQLException: SQL error", exception.getCause().toString());
        verify(mockDao, times(1)).queryRawValue(query, arguments);
    }
}
