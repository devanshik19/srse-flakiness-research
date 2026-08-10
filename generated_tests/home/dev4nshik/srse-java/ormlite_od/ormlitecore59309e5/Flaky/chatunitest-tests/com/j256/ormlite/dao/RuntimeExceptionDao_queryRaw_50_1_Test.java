package com.j256.ormlite.dao;

import java.sql.SQLException;
import org.junit.jupiter.api.function.Executable;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.GenericRawResults;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import com.j256.ormlite.field.DataType;
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

public class RuntimeExceptionDao_queryRaw_50_1_Test {

    @Mock
    private Dao<Object, Object> mockDao;

    @Mock
    private GenericRawResults<Object[]> mockResults;

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testQueryRawSuccess() throws SQLException {
        String query = "SELECT * FROM table";
        DataType[] columnTypes = new DataType[] { DataType.STRING };
        when(mockDao.queryRaw(query, columnTypes)).thenReturn(mockResults);
        GenericRawResults<Object[]> results = runtimeExceptionDao.queryRaw(query, columnTypes);
        assertNotNull(results);
        assertEquals(mockResults, results);
        verify(mockDao, times(1)).queryRaw(query, columnTypes);
    }

    @Test
    public void testQueryRawThrowsSQLException() throws SQLException {
        String query = "SELECT * FROM table";
        DataType[] columnTypes = new DataType[] { DataType.STRING };
        when(mockDao.queryRaw(query, columnTypes)).thenThrow(new SQLException("SQL error"));
        Executable executable = () -> runtimeExceptionDao.queryRaw(query, columnTypes);
        RuntimeException exception = assertThrows(RuntimeException.class, executable);
        assertEquals(SQLException.class, exception.getCause().getClass());
        assertEquals("SQL error", exception.getCause().getMessage());
        verify(mockDao, times(1)).queryRaw(query, columnTypes);
    }
}
