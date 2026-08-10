package com.j256.ormlite.dao;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collection;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
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
public class RuntimeExceptionDao_create_17_0_Test {

    @Mock
    private Dao<Object, Object> daoMock;

    @InjectMocks
    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    private Collection<Object> testCollection;

    @BeforeEach
    public void setUp() {
        testCollection = new ArrayList<>();
        testCollection.add(new Object());
    }

    @Test
    public void testCreateSuccessful() throws SQLException {
        when(daoMock.create(testCollection)).thenReturn(1);
        int result = runtimeExceptionDao.create(testCollection);
        assertEquals(1, result);
        verify(daoMock).create(testCollection);
    }

    @Test
    public void testCreateThrowsSQLException() throws Exception {
        when(daoMock.create(testCollection)).thenThrow(new SQLException("SQL Error"));
        Exception exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.create(testCollection);
        });
        assertTrue(exception.getCause() instanceof SQLException);
        assertEquals("SQL Error", exception.getCause().getMessage());
        verify(daoMock).create(testCollection);
    }
}
