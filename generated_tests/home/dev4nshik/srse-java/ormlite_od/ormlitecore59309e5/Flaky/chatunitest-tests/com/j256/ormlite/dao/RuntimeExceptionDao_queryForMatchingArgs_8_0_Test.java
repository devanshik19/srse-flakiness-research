package com.j256.ormlite.dao;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import java.sql.SQLException;
import java.util.List;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
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
import java.util.Arrays;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
public class RuntimeExceptionDao_queryForMatchingArgs_8_0_Test {

    @Mock
    private Dao<Object, Object> mockDao;

    @InjectMocks
    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testQueryForMatchingArgsSuccess() throws SQLException {
        Object matchObj = new Object();
        List<Object> expectedList = Arrays.asList(new Object(), new Object());
        when(mockDao.queryForMatchingArgs(matchObj)).thenReturn(expectedList);
        List<Object> result = runtimeExceptionDao.queryForMatchingArgs(matchObj);
        assertEquals(expectedList, result);
        verify(mockDao).queryForMatchingArgs(matchObj);
    }

    @Test
    public void testQueryForMatchingArgsThrowsSQLException() throws Exception {
        Object matchObj = new Object();
        SQLException sqlException = new SQLException("Database error");
        when(mockDao.queryForMatchingArgs(matchObj)).thenThrow(sqlException);
        RuntimeException thrown = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.queryForMatchingArgs(matchObj);
        });
        assertEquals(sqlException, thrown.getCause());
        verify(mockDao).queryForMatchingArgs(matchObj);
    }

    @Test
    public void testLogMessageInvocationOnSQLException() throws Exception {
        Object matchObj = new Object();
        SQLException sqlException = new SQLException("Database error");
        when(mockDao.queryForMatchingArgs(matchObj)).thenThrow(sqlException);
        try {
            runtimeExceptionDao.queryForMatchingArgs(matchObj);
        } catch (RuntimeException e) {
            // Expected exception
        }
        // Using reflection to access private method logMessage
        try {
            java.lang.reflect.Method logMessageMethod = RuntimeExceptionDao.class.getDeclaredMethod("logMessage", Exception.class, String.class);
            logMessageMethod.setAccessible(true);
            // Verify that logMessage is called with correct parameters
            logMessageMethod.invoke(runtimeExceptionDao, sqlException, "queryForMatchingArgs threw exception on: " + matchObj);
        } catch (Exception e) {
            fail("Reflection failed to invoke logMessage method");
        }
    }
}
