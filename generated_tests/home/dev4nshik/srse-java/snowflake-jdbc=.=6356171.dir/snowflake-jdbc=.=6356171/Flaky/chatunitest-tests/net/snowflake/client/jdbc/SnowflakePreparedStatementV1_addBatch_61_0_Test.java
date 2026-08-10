package net.snowflake.client.jdbc;

import net.snowflake.client.jdbc.SnowflakePreparedStatementV1;
import net.snowflake.client.jdbc.SnowflakeSQLException;
import net.snowflake.client.jdbc.ErrorCode;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.InputStream;
import java.io.Reader;
import java.math.BigDecimal;
import java.net.URL;
import java.sql.*;
import java.util.*;
import net.snowflake.client.core.*;
import net.snowflake.client.log.SFLogger;
import net.snowflake.client.log.SFLoggerFactory;
import net.snowflake.client.util.VariableTypeArray;
import net.snowflake.common.core.SFBinary;
import net.snowflake.common.core.SqlState;

public class SnowflakePreparedStatementV1_addBatch_61_0_Test {

    @Test
    public void testAddBatchThrowsSQLException() {
        try {
            // Use reflection to create an instance of SnowflakePreparedStatementV1
            Constructor<SnowflakePreparedStatementV1> constructor = SnowflakePreparedStatementV1.class.getDeclaredConstructor(net.snowflake.client.jdbc.SnowflakeConnectionV1.class, String.class, boolean.class, int.class, int.class, int.class);
            constructor.setAccessible(true);
            // Assuming null for connection as it's not used in addBatch
            SnowflakePreparedStatementV1 // Assuming null for connection as it's not used in addBatch
            preparedStatement = // Assuming null for connection as it's not used in addBatch
            constructor.newInstance(null, "SELECT * FROM DUAL", false, ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY, ResultSet.HOLD_CURSORS_OVER_COMMIT);
            // Invoke the addBatch method and expect an exception
            SQLException exception = assertThrows(SnowflakeSQLException.class, () -> {
                preparedStatement.addBatch("SELECT * FROM DUAL");
            });
            // Verify the exception details
            assertEquals(ErrorCode.UNSUPPORTED_STATEMENT_TYPE_IN_EXECUTION_API.getMessageCode(), exception.getErrorCode());
            assertTrue(exception.getMessage().contains(StmtUtil.truncateSQL("SELECT * FROM DUAL")));
        } catch (NoSuchMethodException | InstantiationException | IllegalAccessException | InvocationTargetException e) {
            fail("Failed to create instance of SnowflakePreparedStatementV1 using reflection: " + e.getMessage());
        }
    }
}
