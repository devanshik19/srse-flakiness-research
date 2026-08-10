package com.j256.ormlite.dao;

import com.j256.ormlite.dao.Dao;
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

public class RuntimeExceptionDao_extractId_66_0_Test<T, ID> {

    private Dao<T, ID> mockDao;

    private RuntimeExceptionDao<T, ID> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        mockDao = Mockito.mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testExtractIdSuccess() throws SQLException {
        T data = (T) new Object();
        ID expectedId = (ID) new Object();
        when(mockDao.extractId(data)).thenReturn(expectedId);
        ID actualId = runtimeExceptionDao.extractId(data);
        assertEquals(expectedId, actualId);
        verify(mockDao, times(1)).extractId(data);
    }

    @Test
    public void testExtractIdThrowsSQLException() throws SQLException {
        T data = (T) new Object();
        when(mockDao.extractId(data)).thenThrow(new SQLException("Test SQLException"));
        Exception exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.extractId(data);
        });
        assertTrue(exception.getCause() instanceof SQLException);
        assertEquals("Test SQLException", exception.getCause().getMessage());
        verify(mockDao, times(1)).extractId(data);
    }
}
