package com.j256.ormlite.dao;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
// Corrected import
import com.j256.ormlite.dao.Dao.CreateOrUpdateStatus;
import java.sql.SQLException;
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
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class RuntimeExceptionDao_createOrUpdate_20_0_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    private Dao<Object, Object> mockDao;

    private Object testData;

    @BeforeEach
    void setUp() {
        mockDao = Mockito.mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
        testData = new Object();
    }

    @Test
    void testCreateOrUpdateSuccess() throws SQLException {
        CreateOrUpdateStatus expectedStatus = new CreateOrUpdateStatus(true, true, 1);
        when(mockDao.createOrUpdate(testData)).thenReturn(expectedStatus);
        CreateOrUpdateStatus actualStatus = runtimeExceptionDao.createOrUpdate(testData);
        assertEquals(expectedStatus, actualStatus);
        verify(mockDao, times(1)).createOrUpdate(testData);
    }

    @Test
    void testCreateOrUpdateThrowsSQLException() throws SQLException {
        when(mockDao.createOrUpdate(testData)).thenThrow(new SQLException("Test SQL Exception"));
        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.createOrUpdate(testData);
        });
        assertEquals("java.sql.SQLException: Test SQL Exception", exception.getCause().toString());
        verify(mockDao, times(1)).createOrUpdate(testData);
    }
}
