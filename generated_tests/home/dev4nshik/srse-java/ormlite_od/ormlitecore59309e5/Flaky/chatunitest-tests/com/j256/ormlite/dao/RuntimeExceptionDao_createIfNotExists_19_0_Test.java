package com.j256.ormlite.dao;

import java.sql.SQLException;
import java.util.Objects;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.dao.RuntimeExceptionDao;
import com.j256.ormlite.misc.Supplier;
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
public class RuntimeExceptionDao_createIfNotExists_19_0_Test {

    private RuntimeExceptionDao<TestEntity, Integer> runtimeExceptionDao;

    private Dao<TestEntity, Integer> mockDao;

    private Supplier<TestEntity> entitySupplier;

    private TestEntity testEntity;

    @BeforeEach
    public void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
        entitySupplier = () -> new TestEntity(1, "Test");
        testEntity = new TestEntity(1, "Test");
    }

    @Test
    public void testCreateIfNotExistsSuccess() throws SQLException {
        when(mockDao.createIfNotExists(1, entitySupplier)).thenReturn(testEntity);
        TestEntity result = runtimeExceptionDao.createIfNotExists(1, entitySupplier);
        assertNotNull(result);
        assertEquals(testEntity, result);
        verify(mockDao, times(1)).createIfNotExists(1, entitySupplier);
    }

    @Test
    public void testCreateIfNotExistsThrowsSQLException() throws SQLException {
        when(mockDao.createIfNotExists(1, entitySupplier)).thenThrow(new SQLException("Error"));
        Exception exception = assertThrows(RuntimeException.class, () -> {
            runtimeExceptionDao.createIfNotExists(1, entitySupplier);
        });
        assertTrue(exception.getCause() instanceof SQLException);
        assertEquals("Error", exception.getCause().getMessage());
        verify(mockDao, times(1)).createIfNotExists(1, entitySupplier);
    }

    // Test entity class for testing purposes
    private static class TestEntity {

        private int id;

        private String name;

        public TestEntity(int id, String name) {
            this.id = id;
            this.name = name;
        }

        // equals and hashCode methods should be overridden for proper comparison in tests
        @Override
        public boolean equals(Object obj) {
            if (this == obj)
                return true;
            if (obj == null || getClass() != obj.getClass())
                return false;
            TestEntity that = (TestEntity) obj;
            return id == that.id && name.equals(that.name);
        }

        @Override
        public int hashCode() {
            return Objects.hash(id, name);
        }
    }
}
