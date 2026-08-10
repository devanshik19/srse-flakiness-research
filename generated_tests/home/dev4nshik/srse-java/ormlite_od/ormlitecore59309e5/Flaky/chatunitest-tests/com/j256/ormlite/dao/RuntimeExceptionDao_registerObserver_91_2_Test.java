package com.j256.ormlite.dao;

import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.lang.reflect.Field;
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
import com.j256.ormlite.dao.Dao.DaoObserver;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
public class RuntimeExceptionDao_registerObserver_91_2_Test {

    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @Mock
    private Dao<Object, Object> mockDao;

    @Mock
    private DaoObserver mockObserver;

    @BeforeEach
    public void setUp() {
        // Instantiate RuntimeExceptionDao with the mock Dao
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testRegisterObserver() throws Exception {
        // Use reflection to set the private dao field
        Field daoField = RuntimeExceptionDao.class.getDeclaredField("dao");
        daoField.setAccessible(true);
        daoField.set(runtimeExceptionDao, mockDao);
        // Call the registerObserver method
        runtimeExceptionDao.registerObserver(mockObserver);
        // Verify that the registerObserver method on the mock Dao was called
        verify(mockDao).registerObserver(mockObserver);
    }
}
