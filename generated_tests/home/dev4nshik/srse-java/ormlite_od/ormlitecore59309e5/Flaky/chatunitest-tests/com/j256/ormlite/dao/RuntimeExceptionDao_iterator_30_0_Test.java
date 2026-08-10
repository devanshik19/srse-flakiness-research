package com.j256.ormlite.dao;

import com.j256.ormlite.dao.CloseableIterator;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.sql.SQLException;
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

public class RuntimeExceptionDao_iterator_30_0_Test {

    @Mock
    private Dao<Object, Object> mockDao;

    @Mock
    private CloseableIterator<Object> mockIterator;

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testIterator() {
        // Arrange
        when(mockDao.iterator()).thenReturn(mockIterator);
        // Act
        CloseableIterator<Object> result = runtimeExceptionDao.iterator();
        // Assert
        assertNotNull(result, "The iterator should not be null");
        assertEquals(mockIterator, result, "The iterator returned should match the mock iterator");
        verify(mockDao, times(1)).iterator();
    }
}
