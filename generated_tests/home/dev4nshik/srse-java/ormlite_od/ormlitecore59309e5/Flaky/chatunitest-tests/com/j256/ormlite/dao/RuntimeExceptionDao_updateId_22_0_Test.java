package com.j256.ormlite.dao;

import java.sql.SQLException;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
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
public class RuntimeExceptionDao_updateId_22_0_Test<T, ID> {

    @Mock
    private Dao<T, ID> mockDao;

    @InjectMocks
    private RuntimeExceptionDao<T, ID> runtimeExceptionDao;

    private T data;

    private ID newId;

    @BeforeEach
    public void setUp() {
        // Initialize data and newId with appropriate mock or dummy values
        data = (T) mock(Object.class);
        newId = (ID) mock(Object.class);
    }

    @Test
    public void testUpdateIdSuccess() throws SQLException {
        // Arrange
        int expectedUpdateCount = 1;
        when(mockDao.updateId(data, newId)).thenReturn(expectedUpdateCount);
        // Act
        int actualUpdateCount = runtimeExceptionDao.updateId(data, newId);
        // Assert
        assertEquals(expectedUpdateCount, actualUpdateCount);
        verify(mockDao, times(1)).updateId(data, newId);
    }

    @Test
    public void testUpdateIdThrowsRuntimeException() throws SQLException {
        // Arrange
        SQLException sqlException = new SQLException("SQL error");
        when(mockDao.updateId(data, newId)).thenThrow(sqlException);
        // Act & Assert
        RuntimeException thrown = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.updateId(data, newId);
        });
        assertEquals(sqlException, thrown.getCause());
        verify(mockDao, times(1)).updateId(data, newId);
    }
}
