package com.j256.ormlite.dao;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.GenericRawResults;
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

public class RuntimeExceptionDao_queryRaw_40_0_Test {

    @Mock
    private Dao<Object, Object> mockDao;

    @Mock
    private GenericRawResults<String[]> mockResults;

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testQueryRawSuccess() throws SQLException {
        String query = "SELECT * FROM table";
        String[] arguments = { "arg1", "arg2" };
        when(mockDao.queryRaw(query, arguments)).thenReturn(mockResults);
        GenericRawResults<String[]> result = runtimeExceptionDao.queryRaw(query, arguments);
        assertNotNull(result);
        assertEquals(mockResults, result);
        verify(mockDao, times(1)).queryRaw(query, arguments);
    }

    @Test
    public void testQueryRawThrowsSQLException() throws Exception {
        String query = "SELECT * FROM table";
        String[] arguments = { "arg1", "arg2" };
        when(mockDao.queryRaw(query, arguments)).thenThrow(new SQLException("SQL Exception"));
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.queryRaw(query, arguments);
        });
        assertEquals(SQLException.class, exception.getCause().getClass());
        assertEquals("SQL Exception", exception.getCause().getMessage());
        verify(mockDao, times(1)).queryRaw(query, arguments);
    }
}
