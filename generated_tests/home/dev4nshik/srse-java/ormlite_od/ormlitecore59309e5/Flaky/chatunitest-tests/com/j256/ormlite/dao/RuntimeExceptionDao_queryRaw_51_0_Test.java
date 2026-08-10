package com.j256.ormlite.dao;

import java.sql.SQLException;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.GenericRawResults;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import com.j256.ormlite.field.DataType;
import com.j256.ormlite.stmt.ArgumentHolder;
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
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class RuntimeExceptionDao_queryRaw_51_0_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @Mock
    private Dao<Object, Object> mockDao;

    @Mock
    private GenericRawResults<Object[]> mockResults;

    @BeforeEach
    void setUp() {
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    void testQueryRawSuccess() throws SQLException {
        String query = "SELECT * FROM table";
        DataType[] columnTypes = new DataType[] { DataType.STRING };
        ArgumentHolder[] arguments = new ArgumentHolder[] {};
        when(mockDao.queryRaw(query, columnTypes, arguments)).thenReturn(mockResults);
        GenericRawResults<Object[]> results = runtimeExceptionDao.queryRaw(query, columnTypes, arguments);
        assertNotNull(results);
        verify(mockDao).queryRaw(query, columnTypes, arguments);
    }

    @Test
    void testQueryRawThrowsSQLException() throws SQLException {
        String query = "SELECT * FROM table";
        DataType[] columnTypes = new DataType[] { DataType.STRING };
        ArgumentHolder[] arguments = new ArgumentHolder[] {};
        when(mockDao.queryRaw(query, columnTypes, arguments)).thenThrow(new SQLException("SQL error"));
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.queryRaw(query, columnTypes, arguments);
        });
        assertEquals("SQL error", exception.getCause().getMessage());
        verify(mockDao).queryRaw(query, columnTypes, arguments);
    }
}
