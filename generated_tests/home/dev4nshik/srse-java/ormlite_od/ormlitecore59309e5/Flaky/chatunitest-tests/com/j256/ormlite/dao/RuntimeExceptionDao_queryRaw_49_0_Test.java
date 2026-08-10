package com.j256.ormlite.dao;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.GenericRawResults;
import com.j256.ormlite.dao.RawRowObjectMapper;
import com.j256.ormlite.field.DataType;
import java.sql.SQLException;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.List;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Collection;
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

@ExtendWith(MockitoExtension.class)
public class RuntimeExceptionDao_queryRaw_49_0_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @Mock
    private Dao<Object, Object> mockDao;

    @BeforeEach
    public void setUp() {
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testQueryRawSuccess() throws SQLException {
        String query = "SELECT * FROM table";
        DataType[] columnTypes = new DataType[] { DataType.STRING };
        RawRowObjectMapper<Object> mapper = mock(RawRowObjectMapper.class);
        String[] arguments = new String[] { "arg1", "arg2" };
        GenericRawResults<Object> expectedResults = mock(GenericRawResults.class);
        when(mockDao.queryRaw(eq(query), eq(columnTypes), eq(mapper), eq(arguments))).thenReturn(expectedResults);
        GenericRawResults<Object> results = runtimeExceptionDao.queryRaw(query, columnTypes, mapper, arguments);
        assertNotNull(results);
        assertEquals(expectedResults, results);
        verify(mockDao).queryRaw(eq(query), eq(columnTypes), eq(mapper), eq(arguments));
    }

    @Test
    public void testQueryRawThrowsSQLException() throws SQLException {
        String query = "SELECT * FROM table";
        DataType[] columnTypes = new DataType[] { DataType.STRING };
        RawRowObjectMapper<Object> mapper = mock(RawRowObjectMapper.class);
        String[] arguments = new String[] { "arg1", "arg2" };
        when(mockDao.queryRaw(eq(query), eq(columnTypes), eq(mapper), eq(arguments))).thenThrow(new SQLException("SQL error"));
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.queryRaw(query, columnTypes, mapper, arguments);
        });
        assertNotNull(exception.getCause());
        assertTrue(exception.getCause() instanceof SQLException);
        verify(mockDao).queryRaw(eq(query), eq(columnTypes), eq(mapper), eq(arguments));
    }
}
