package com.j256.ormlite.dao;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import com.j256.ormlite.dao.Dao;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
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
public class RuntimeExceptionDao_queryForAll_4_0_Test {

    private Dao<Object, Object> mockDao;

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        mockDao = Mockito.mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testQueryForAllSuccess() throws SQLException {
        List<Object> expectedList = new ArrayList<>();
        when(mockDao.queryForAll()).thenReturn(expectedList);
        List<Object> result = runtimeExceptionDao.queryForAll();
        assertEquals(expectedList, result);
        verify(mockDao, times(1)).queryForAll();
    }

    @Test
    public void testQueryForAllSQLException() throws SQLException {
        when(mockDao.queryForAll()).thenThrow(new SQLException("SQL error"));
        Exception exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.queryForAll();
        });
        assertTrue(exception.getCause() instanceof SQLException);
        assertEquals("SQL error", exception.getCause().getMessage());
        verify(mockDao, times(1)).queryForAll();
    }
}
