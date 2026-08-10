package com.j256.ormlite.dao;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.GenericRawResults;
import com.j256.ormlite.dao.RawRowMapper;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import java.sql.SQLException;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
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

class RuntimeExceptionDao_queryRaw_46_1_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    private Dao<Object, Object> mockDao;

    private RawRowMapper<Object> mockMapper;

    @BeforeEach
    void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
        mockMapper = mock(RawRowMapper.class);
    }

    @Test
    void testQueryRawSuccess() throws SQLException {
        // Arrange
        GenericRawResults<Object> expectedResults = mock(GenericRawResults.class);
        when(mockDao.queryRaw(anyString(), any(RawRowMapper.class), any(String[].class))).thenReturn(expectedResults);
        // Act
        GenericRawResults<Object> results = runtimeExceptionDao.queryRaw("SELECT * FROM table", mockMapper, new String[] { "arg1", "arg2" });
        // Assert
        assertEquals(expectedResults, results);
        verify(mockDao, times(1)).queryRaw(anyString(), any(RawRowMapper.class), any(String[].class));
    }

    @Test
    void testQueryRawThrowsRuntimeException() throws SQLException {
        // Arrange
        when(mockDao.queryRaw(anyString(), any(RawRowMapper.class), any(String[].class))).thenThrow(new SQLException("SQL error"));
        // Act & Assert
        RuntimeException exception = assertThrows(RuntimeException.class, () -> runtimeExceptionDao.queryRaw("SELECT * FROM table", mockMapper, new String[] { "arg1", "arg2" }));
        assertEquals("java.sql.SQLException: SQL error", exception.getCause().toString());
        verify(mockDao, times(1)).queryRaw(anyString(), any(RawRowMapper.class), any(String[].class));
    }
}
