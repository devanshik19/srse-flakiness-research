package net.snowflake.client.jdbc;

import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.InputStream;
import java.io.Reader;
import java.math.BigDecimal;
import java.net.URL;
import net.snowflake.client.log.SFLogger;
import net.snowflake.client.log.SFLoggerFactory;
import net.snowflake.client.util.VariableTypeArray;
import net.snowflake.common.core.SFBinary;
import net.snowflake.common.core.SqlState;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import java.sql.*;
import java.util.*;
import net.snowflake.client.core.*;

@ExtendWith(MockitoExtension.class)
public class SnowflakePreparedStatementV1_execute_26_1_Test {

    @Mock
    private SnowflakeConnectionV1 connection;

    @Mock
    private SFLogger logger;

    @Mock
    private SFStatementMetaData statementMetaData;

    @InjectMocks
    private SnowflakePreparedStatementV1 preparedStatement;

    private String sql = "SELECT * FROM DUAL";

    @BeforeEach
    public void setUp() throws SQLException, NoSuchFieldException, IllegalAccessException {
        preparedStatement = new SnowflakePreparedStatementV1(connection, sql, false, ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY, ResultSet.CLOSE_CURSORS_AT_COMMIT);
        // Use reflection to set the private field statementMetaData
        java.lang.reflect.Field field = SnowflakePreparedStatementV1.class.getDeclaredField("statementMetaData");
        field.setAccessible(true);
        field.set(preparedStatement, statementMetaData);
    }

    @Test
    public void testExecute() throws SQLException {
        // Arrange
        doNothing().when(logger).debug(anyString(), any(Object[].class));
        // Act
        boolean result = preparedStatement.execute();
        // Assert
        assertTrue(result);
        verify(logger).debug(eq("execute: {}"), eq(new Object[] { sql }));
    }

    // Use reflection to test the private method executeInternal
    @Test
    public void testExecuteInternal() throws Exception {
        // Arrange
        doNothing().when(logger).debug(anyString(), any(Object[].class));
        // Use reflection to access the private method
        java.lang.reflect.Method method = SnowflakePreparedStatementV1.class.getDeclaredMethod("executeInternal", String.class, Map.class);
        method.setAccessible(true);
        // Act
        boolean result = (boolean) method.invoke(preparedStatement, sql, preparedStatement.getParameterBindings());
        // Assert
        assertTrue(result);
    }
}
