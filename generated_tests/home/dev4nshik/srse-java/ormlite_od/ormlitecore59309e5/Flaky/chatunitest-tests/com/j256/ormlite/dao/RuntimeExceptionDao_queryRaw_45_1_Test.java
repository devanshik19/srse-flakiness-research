package com.j256.ormlite.dao;

import java.sql.SQLException;
import org.junit.jupiter.api.function.Executable;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.GenericRawResults;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import com.j256.ormlite.stmt.ArgumentHolder;
import com.j256.ormlite.support.ConnectionSource;
import com.j256.ormlite.support.DatabaseConnection;
import com.j256.ormlite.support.DatabaseResults;
import com.j256.ormlite.table.DatabaseTableConfig;
import com.j256.ormlite.table.ObjectFactory;
import com.j256.ormlite.table.TableInfo;
// Assuming RawRowMapper is in the com.j256.ormlite.dao package
import com.j256.ormlite.dao.RawRowMapper;
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

@ExtendWith(MockitoExtension.class)
public class RuntimeExceptionDao_queryRaw_45_1_Test<T, ID> {

    @Mock
    private Dao<T, ID> mockDao;

    @Mock
    private RawRowMapper<T> mockMapper;

    @Mock
    private GenericRawResults<T> mockResults;

    private RuntimeExceptionDao<T, ID> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testQueryRawSuccess() throws SQLException {
        String query = "SELECT * FROM table";
        ArgumentHolder[] arguments = new ArgumentHolder[0];
        when(mockDao.queryRaw(query, mockMapper, arguments)).thenReturn(mockResults);
        GenericRawResults<T> results = runtimeExceptionDao.queryRaw(query, mockMapper, arguments);
        assertNotNull(results);
        assertEquals(mockResults, results);
        verify(mockDao).queryRaw(query, mockMapper, arguments);
    }

    @Test
    public void testQueryRawThrowsSQLException() throws SQLException {
        String query = "SELECT * FROM table";
        ArgumentHolder[] arguments = new ArgumentHolder[0];
        when(mockDao.queryRaw(query, mockMapper, arguments)).thenThrow(new SQLException("SQL Error"));
        Executable executable = () -> runtimeExceptionDao.queryRaw(query, mockMapper, arguments);
        RuntimeException exception = assertThrows(RuntimeException.class, executable);
        assertTrue(exception.getCause() instanceof SQLException);
        assertEquals("SQL Error", exception.getCause().getMessage());
        verify(mockDao).queryRaw(query, mockMapper, arguments);
    }
}
