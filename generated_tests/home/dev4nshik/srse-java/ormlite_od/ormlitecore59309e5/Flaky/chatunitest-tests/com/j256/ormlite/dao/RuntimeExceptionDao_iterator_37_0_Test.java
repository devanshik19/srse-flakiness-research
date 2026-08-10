package com.j256.ormlite.dao;

import com.j256.ormlite.dao.CloseableIterator;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import com.j256.ormlite.stmt.PreparedQuery;
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
import com.j256.ormlite.stmt.PreparedUpdate;
import com.j256.ormlite.stmt.QueryBuilder;
import com.j256.ormlite.stmt.UpdateBuilder;
import com.j256.ormlite.support.ConnectionSource;
import com.j256.ormlite.support.DatabaseConnection;
import com.j256.ormlite.support.DatabaseResults;
import com.j256.ormlite.table.DatabaseTableConfig;
import com.j256.ormlite.table.ObjectFactory;
import com.j256.ormlite.table.TableInfo;

public class RuntimeExceptionDao_iterator_37_0_Test {

    private Dao<Object, Object> mockDao;

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        mockDao = Mockito.mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testIteratorSuccess() throws SQLException {
        PreparedQuery<Object> mockPreparedQuery = Mockito.mock(PreparedQuery.class);
        CloseableIterator<Object> mockIterator = Mockito.mock(CloseableIterator.class);
        when(mockDao.iterator(mockPreparedQuery, 0)).thenReturn(mockIterator);
        CloseableIterator<Object> result = runtimeExceptionDao.iterator(mockPreparedQuery, 0);
        verify(mockDao).iterator(mockPreparedQuery, 0);
        assertSame(mockIterator, result);
    }

    @Test
    public void testIteratorThrowsSQLException() throws SQLException {
        PreparedQuery<Object> mockPreparedQuery = Mockito.mock(PreparedQuery.class);
        when(mockDao.iterator(mockPreparedQuery, 0)).thenThrow(new SQLException("Test Exception"));
        assertThrows(RuntimeException.class, () -> runtimeExceptionDao.iterator(mockPreparedQuery, 0));
        verify(mockDao).iterator(mockPreparedQuery, 0);
    }
}
