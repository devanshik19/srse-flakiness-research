package com.j256.ormlite.dao;

import java.sql.SQLException;
import java.util.List;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import com.j256.ormlite.stmt.PreparedQuery;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.Arrays;
import java.util.Collection;
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
public class RuntimeExceptionDao_query_15_0_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    private Dao<Object, Object> mockDao;

    private PreparedQuery<Object> mockPreparedQuery;

    @BeforeEach
    public void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
        mockPreparedQuery = mock(PreparedQuery.class);
    }

    @Test
    public void testQuerySuccess() throws SQLException {
        List<Object> expectedList = Arrays.asList(new Object());
        when(mockDao.query(mockPreparedQuery)).thenReturn(expectedList);
        List<Object> result = runtimeExceptionDao.query(mockPreparedQuery);
        assertNotNull(result);
        assertEquals(expectedList, result);
        verify(mockDao, times(1)).query(mockPreparedQuery);
    }

    @Test
    public void testQueryThrowsSQLException() throws SQLException {
        when(mockDao.query(mockPreparedQuery)).thenThrow(new SQLException("Test SQLException"));
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.query(mockPreparedQuery);
        });
        assertNotNull(exception.getCause());
        assertTrue(exception.getCause() instanceof SQLException);
        assertEquals("Test SQLException", exception.getCause().getMessage());
        verify(mockDao, times(1)).query(mockPreparedQuery);
    }
}
