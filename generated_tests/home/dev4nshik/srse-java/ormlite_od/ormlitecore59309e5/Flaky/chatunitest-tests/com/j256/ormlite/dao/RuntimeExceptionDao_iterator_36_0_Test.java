package com.j256.ormlite.dao;

import java.sql.SQLException;
import org.junit.jupiter.api.function.Executable;
import com.j256.ormlite.dao.CloseableIterator;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import com.j256.ormlite.stmt.PreparedQuery;
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
import com.j256.ormlite.stmt.PreparedUpdate;
import com.j256.ormlite.stmt.QueryBuilder;
import com.j256.ormlite.stmt.UpdateBuilder;
import com.j256.ormlite.support.ConnectionSource;
import com.j256.ormlite.support.DatabaseConnection;
import com.j256.ormlite.support.DatabaseResults;
import com.j256.ormlite.table.DatabaseTableConfig;
import com.j256.ormlite.table.ObjectFactory;
import com.j256.ormlite.table.TableInfo;

class RuntimeExceptionDao_iterator_36_0_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    private Dao<Object, Object> mockDao;

    private PreparedQuery<Object> mockPreparedQuery;

    private CloseableIterator<Object> mockIterator;

    @BeforeEach
    void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
        mockPreparedQuery = mock(PreparedQuery.class);
        mockIterator = mock(CloseableIterator.class);
    }

    @Test
    void testIterator_success() throws SQLException {
        when(mockDao.iterator(mockPreparedQuery)).thenReturn(mockIterator);
        CloseableIterator<Object> result = runtimeExceptionDao.iterator(mockPreparedQuery);
        assertNotNull(result);
        assertEquals(mockIterator, result);
        verify(mockDao).iterator(mockPreparedQuery);
    }

    @Test
    void testIterator_throwsSQLException() throws SQLException {
        when(mockDao.iterator(mockPreparedQuery)).thenThrow(new SQLException("Test SQLException"));
        Executable executable = () -> runtimeExceptionDao.iterator(mockPreparedQuery);
        RuntimeException exception = assertThrows(RuntimeException.class, executable);
        assertEquals(SQLException.class, exception.getCause().getClass());
        assertEquals("Test SQLException", exception.getCause().getMessage());
        verify(mockDao).iterator(mockPreparedQuery);
    }
}
