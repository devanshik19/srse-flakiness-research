package com.j256.ormlite.dao;

import java.sql.SQLException;
import org.junit.jupiter.api.function.Executable;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
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

public class RuntimeExceptionDao_objectsEqual_65_0_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    private Dao<Object, Object> mockDao;

    @BeforeEach
    public void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testObjectsEqualTrue() throws SQLException {
        Object obj1 = new Object();
        Object obj2 = new Object();
        when(mockDao.objectsEqual(obj1, obj2)).thenReturn(true);
        boolean result = runtimeExceptionDao.objectsEqual(obj1, obj2);
        assertTrue(result);
        verify(mockDao).objectsEqual(obj1, obj2);
    }

    @Test
    public void testObjectsEqualFalse() throws SQLException {
        Object obj1 = new Object();
        Object obj2 = new Object();
        when(mockDao.objectsEqual(obj1, obj2)).thenReturn(false);
        boolean result = runtimeExceptionDao.objectsEqual(obj1, obj2);
        assertFalse(result);
        verify(mockDao).objectsEqual(obj1, obj2);
    }

    @Test
    public void testObjectsEqualThrowsRuntimeException() throws SQLException {
        Object obj1 = new Object();
        Object obj2 = new Object();
        when(mockDao.objectsEqual(obj1, obj2)).thenThrow(new SQLException("Test Exception"));
        Executable executable = () -> runtimeExceptionDao.objectsEqual(obj1, obj2);
        RuntimeException exception = assertThrows(RuntimeException.class, executable);
        assertEquals("java.sql.SQLException: Test Exception", exception.getMessage());
    }
}
