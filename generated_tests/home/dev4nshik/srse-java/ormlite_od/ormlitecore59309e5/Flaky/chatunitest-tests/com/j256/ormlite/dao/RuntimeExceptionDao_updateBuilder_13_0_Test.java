package com.j256.ormlite.dao;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.stmt.UpdateBuilder;
import java.lang.reflect.Field;
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
import com.j256.ormlite.support.ConnectionSource;
import com.j256.ormlite.support.DatabaseConnection;
import com.j256.ormlite.support.DatabaseResults;
import com.j256.ormlite.table.DatabaseTableConfig;
import com.j256.ormlite.table.ObjectFactory;
import com.j256.ormlite.table.TableInfo;

public class RuntimeExceptionDao_updateBuilder_13_0_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    private Dao<Object, Object> mockDao;

    private UpdateBuilder<Object, Object> mockUpdateBuilder;

    @BeforeEach
    public void setUp() throws Exception {
        // Create mock objects
        mockDao = Mockito.mock(Dao.class);
        mockUpdateBuilder = Mockito.mock(UpdateBuilder.class);
        // Stub the updateBuilder method to return the mock UpdateBuilder
        when(mockDao.updateBuilder()).thenReturn(mockUpdateBuilder);
        // Create an instance of RuntimeExceptionDao
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
        // Use reflection to set the private dao field
        Field daoField = RuntimeExceptionDao.class.getDeclaredField("dao");
        daoField.setAccessible(true);
        daoField.set(runtimeExceptionDao, mockDao);
    }

    @Test
    public void testUpdateBuilder() {
        // Call the method under test
        UpdateBuilder<Object, Object> updateBuilder = runtimeExceptionDao.updateBuilder();
        // Verify the result
        assertNotNull(updateBuilder, "UpdateBuilder should not be null");
        // Ensure that the returned UpdateBuilder is the mock object
        Mockito.verify(mockDao).updateBuilder();
    }
}
