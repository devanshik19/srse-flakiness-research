package com.j256.ormlite.dao;

import java.sql.SQLException;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
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

@ExtendWith(MockitoExtension.class)
public class RuntimeExceptionDao_refresh_24_0_Test {

    private Dao<Object, Object> mockDao;

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testRefreshSuccess() throws Exception {
        Object data = new Object();
        when(mockDao.refresh(data)).thenReturn(1);
        int result = runtimeExceptionDao.refresh(data);
        assertEquals(1, result);
        verify(mockDao).refresh(data);
    }

    @Test
    public void testRefreshThrowsSQLException() throws Exception {
        Object data = new Object();
        SQLException sqlException = new SQLException("SQL error");
        when(mockDao.refresh(data)).thenThrow(sqlException);
        Exception exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.refresh(data);
        });
        assertEquals(sqlException, exception.getCause());
        Method logMethod = RuntimeExceptionDao.class.getDeclaredMethod("logMessage", Exception.class, String.class);
        logMethod.setAccessible(true);
        logMethod.invoke(runtimeExceptionDao, sqlException, "refresh threw exception on: " + data);
    }
}
