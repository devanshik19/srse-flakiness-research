package com.j256.ormlite.dao;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.GenericRawResults;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import com.j256.ormlite.logger.Logger;
import com.j256.ormlite.logger.LoggerFactory;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
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

public class RuntimeExceptionDao_queryRaw_38_0_Test {

    private Dao<String, String> mockDao;

    private RuntimeExceptionDao<String, String> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testQueryRawSuccess() throws SQLException {
        String query = "SELECT * FROM table";
        GenericRawResults<String[]> mockResults = mock(GenericRawResults.class);
        when(mockDao.queryRaw(query)).thenReturn(mockResults);
        GenericRawResults<String[]> results = runtimeExceptionDao.queryRaw(query);
        assertNotNull(results);
        assertEquals(mockResults, results);
        verify(mockDao, times(1)).queryRaw(query);
    }

    private void invokePrivateMethod(Object target, String methodName, Object... args) throws Exception {
        Method method = target.getClass().getDeclaredMethod(methodName, Exception.class, String.class);
        method.setAccessible(true);
        method.invoke(target, args);
    }
}
